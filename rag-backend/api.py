from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import logging
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
from google.generativeai import GenerativeModel, configure
import google.generativeai as genai
import dotenv
from database import db_manager

# Load environment variables
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Query API",
    description="API for retrieving and generating answers from documentation using vector search",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY or GEMINI_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)
# Try to initialize with gemini-pro, fallback if needed
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception:
    # Fallback to a different model if gemini-pro is not available
    model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Qdrant client
if QDRANT_API_KEY:
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
else:
    qdrant_client = QdrantClient(
        host='localhost',
        port=6333
    )

COLLECTION_NAME = "docusaurus-rag"

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    max_context_length: Optional[int] = 2000
    selected_text: Optional[str] = None  # User-selected/highlighted text


class RelevantDoc(BaseModel):
    text: str
    source: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    relevant_docs: List[RelevantDoc]


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "RAG Query API is running"}


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Query the RAG system to get an answer based on the documentation.

    Args:
        request: QueryRequest containing the user query and optional parameters

    Returns:
        QueryResponse containing the answer and relevant documents
    """
    try:
        logger.info(f"Processing query: {request.query}")

        # Create a new session for this query
        session_id = await db_manager.create_session()
        if session_id is None:
            logger.warning("Could not create session - database not initialized")

        # Check if selected text is provided (Selected Text Mode)
        if request.selected_text and request.selected_text.strip():
            logger.info("SELECTED TEXT MODE: Activated - bypassing Qdrant completely, using only user-provided text")

            # In selected text mode, we don't query Qdrant at all (STRICT REQUIREMENT)
            # We only use the selected text as context
            context = request.selected_text.strip()
            answer = generate_answer(request.query, context)

            # Create a RelevantDoc from the selected text
            relevant_docs = [RelevantDoc(
                text=request.selected_text,
                source="user_selected_text",
                score=1.0  # Perfect score for user-provided text
            )]

            # Log the selected text in the database
            if session_id:
                await db_manager.save_selected_text(session_id, request.selected_text)
                # Save the message with is_selection_based=True and source_type='selected_text'
                await db_manager.save_message(
                    session_id,
                    request.query,
                    answer,
                    is_selection_based=True,
                    source_type='selected_text'
                )

            logger.info("ANSWER GENERATED: Source = user-selected text")

            return QueryResponse(
                answer=answer,
                relevant_docs=relevant_docs
            )
        else:
            logger.info("QDRANT MODE: Activated - performing vector search in Qdrant for relevant documents")

            # Generate embedding for the query
            query_embedding = generate_query_embedding(request.query)

            # Search in Qdrant for relevant chunks
            search_results = qdrant_client.query_points(
                collection_name=COLLECTION_NAME,
                query=query_embedding,
                limit=request.top_k,
                with_payload=True
            )

            # Extract relevant documents
            relevant_docs = []
            context_parts = []

            # Handle different result formats depending on Qdrant client version
            for result in search_results:
                # Check if result has payload attribute (newer versions)
                if hasattr(result, 'payload') and result.payload:
                    doc = RelevantDoc(
                        text=result.payload.get("text", ""),
                        source=result.payload.get("source", ""),
                        score=getattr(result, 'score', 0.0)  # Use getattr to handle different result formats
                    )
                # For older versions or different result formats
                elif isinstance(result, dict) and 'payload' in result:
                    doc = RelevantDoc(
                        text=result['payload'].get("text", ""),
                        source=result['payload'].get("source", ""),
                        score=result.get('score', 0.0)
                    )
                else:
                    continue  # Skip if we can't extract the payload properly

                relevant_docs.append(doc)

                # Add to context for LLM, limiting the total context length
                if len(" ".join(context_parts)) + len(doc.text) <= request.max_context_length:
                    context_parts.append(doc.text)

            if not relevant_docs:
                logger.warning("No relevant documents found for the query")
                answer = "I couldn't find any relevant information in the documentation to answer your query."
                relevant_docs = []

                # Save the message with source_type='qdrant' even when no docs found
                if session_id:
                    await db_manager.save_message(
                        session_id,
                        request.query,
                        answer,
                        is_selection_based=False,
                        source_type='qdrant'
                    )

                return QueryResponse(
                    answer=answer,
                    relevant_docs=relevant_docs
                )

            # Generate answer using the LLM with context
            context = "\n\n".join(context_parts)
            answer = generate_answer(request.query, context)

            logger.info(f"ANSWER GENERATED: Source = Qdrant retrieved documents. Found {len(relevant_docs)} relevant documents")

            # Save retrieval logs for each relevant document
            if session_id:
                message_id = await db_manager.save_message(
                    session_id,
                    request.query,
                    answer,
                    is_selection_based=False,
                    source_type='qdrant'
                )

                for doc in relevant_docs:
                    await db_manager.save_retrieval_log(
                        session_id,
                        message_id,
                        None,  # chunk_id could be added if available in payload
                        doc.score,
                        doc.source,
                        doc.text
                    )

            return QueryResponse(
                answer=answer,
                relevant_docs=relevant_docs
            )

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


def generate_query_embedding(query: str) -> List[float]:
    """
    Generate embedding for the input query using Gemini API.

    Args:
        query: The input query string

    Returns:
        List of floats representing the embedding vector
    """
    try:
        import google.generativeai as genai
        result = genai.embed_content(
            model="models/embedding-001",
            content=query
        )
        return result['embedding']
    except Exception as e:
        logger.error(f"Error generating query embedding: {str(e)}")
        # Provide a fallback with mock embeddings if API fails (for testing purposes)
        # In production, you might want to handle this differently
        import numpy as np
        # Generate random embeddings with the correct dimensions (768 for our Qdrant setup)
        return np.random.random(768).astype(np.float32).tolist()


def generate_answer(query: str, context: str) -> str:
    """
    Generate an answer using the LLM based on the query and context.

    Args:
        query: The user's query
        context: Retrieved context from the documentation or user-selected text

    Returns:
        Generated answer string
    """
    try:
        # Create a prompt with the query and context
        prompt = f"""
        You are a helpful assistant that answers questions based on provided documentation.
        Use only the information in the context below to answer the question.
        If the context doesn't contain enough information to answer the question, say so.

        Context:
        {context}

        Question: {query}

        Answer:
        """

        # Generate response using the Gemini model
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1024,
            }
        )

        # Return the generated text
        return response.text if response.text else "I couldn't generate an answer based on the provided context."

    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        # Fallback response if API call fails
        return f"Due to an API error, I couldn't generate a full response. Error: {str(e)[:100]}..."


@app.get("/test-connection")
async def test_connection():
    """
    Test endpoint to verify connection to Qdrant collection and get collection details.

    Returns:
        JSON with collection status, number of vectors, and vector dimensions.
    """
    try:
        # Test connection to Qdrant and get collection info
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)

        # Extract collection details
        collection_status = "available"
        vector_count = collection_info.points_count
        vector_dimensions = None

        # Get vector configuration to determine dimensions
        if hasattr(collection_info, 'config') and collection_info.config:
            # For newer Qdrant client versions
            if hasattr(collection_info.config, 'params') and collection_info.config.params:
                vector_config = collection_info.config.params.vectors
                if hasattr(vector_config, 'size'):
                    vector_dimensions = vector_config.size
                elif isinstance(vector_config, dict) and 'size' in vector_config:
                    vector_dimensions = vector_config['size']
                elif hasattr(vector_config, '__dict__') and 'size' in vector_config.__dict__:
                    # Handle different vector config structures
                    vector_dimensions = getattr(vector_config, 'size', None)

        # Fallback: try to get vector dimensions from the first point if collection config is not available
        if vector_dimensions is None:
            try:
                # Get one point to determine vector dimensions
                sample_points = qdrant_client.retrieve(
                    collection_name=COLLECTION_NAME,
                    ids=[0] if vector_count > 0 else []
                ) if vector_count > 0 else []

                if sample_points:
                    first_point = sample_points[0]
                    if hasattr(first_point, 'vector') and first_point.vector:
                        vector_dimensions = len(first_point.vector)
                    elif isinstance(first_point, dict) and 'vector' in first_point and first_point['vector']:
                        vector_dimensions = len(first_point['vector'])
            except:
                # If we can't determine vector dimensions, set to unknown
                vector_dimensions = "unknown"

        return {
            "collection_status": collection_status,
            "collection_name": COLLECTION_NAME,
            "vector_count": vector_count,
            "vector_dimensions": vector_dimensions,
            "qdrant_url": QDRANT_URL,
            "connection_status": "success"
        }
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Connection to Qdrant failed",
                "message": str(e),
                "collection_name": COLLECTION_NAME,
                "connection_status": "failed"
            }
        )


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the service is running and can connect to dependencies"""
    try:
        # Test connection to Qdrant
        qdrant_client.get_collection(COLLECTION_NAME)
        return {"status": "healthy", "qdrant": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service not ready")


@app.on_event("startup")
async def startup_event():
    """Initialize database connection when the app starts."""
    await db_manager.init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection when the app shuts down."""
    await db_manager.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
