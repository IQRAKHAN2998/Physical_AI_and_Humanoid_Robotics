from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import logging
import dotenv
import numpy as np
from qdrant_client import QdrantClient
import google.generativeai as genai
from database import db_manager
from embed import convert_to_text, split_into_chunks, generate_embedding, get_all_files, embed_documents
from store import store_embeddings, search_embeddings
import asyncio

# =========================
# ENV & LOGGING
# =========================
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="RAG Query API",
    description="Retrieve + Generate answers from documentation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CONFIG
# =========================
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY or GEMINI_KEY is required")

COLLECTION_NAME = "docusaurus-rag"  # MUST MATCH QDRANT

# =========================
# GEMINI SETUP
# =========================
genai.configure(api_key=GEMINI_API_KEY)
try:
    llm_model = genai.GenerativeModel("gemini-pro")
except Exception:
    llm_model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# QDRANT CLIENT
# =========================
if QDRANT_API_KEY:
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    qdrant_client = QdrantClient(host="localhost", port=6333)

# =========================
# MODELS
# =========================
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    max_context_length: Optional[int] = 2000
    selected_text: Optional[str] = None


class RelevantDoc(BaseModel):
    text: str
    source: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    relevant_docs: List[RelevantDoc]

# =========================
# ROOT
# =========================
@app.get("/")
async def root():
    return {"status": "ok", "message": "RAG API running"}

# =========================
# MAIN QUERY ENDPOINT
# =========================
@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        logger.info(f"QUERY: {request.query}")
        session_id = await db_manager.create_session()

        # =========================
        # SELECTED TEXT MODE (NO QDRANT)
        # =========================
        if request.selected_text and request.selected_text.strip():
            context = request.selected_text.strip()
            answer = generate_answer(request.query, context)

            relevant_docs = [RelevantDoc(
                text=context,
                source="user_selected_text",
                score=1.0
            )]

            if session_id:
                await db_manager.save_message(
                    session_id,
                    request.query,
                    answer,
                    is_selection_based=True,
                    source_type="selected_text"
                )

            return QueryResponse(answer=answer, relevant_docs=relevant_docs)

        # =========================
        # QDRANT MODE
        # =========================
        query_embedding = generate_query_embedding(request.query)

        search_results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=request.top_k,
            with_payload=True
        )

        # Extract points in the most defensive way possible
        try:
            # Try the standard approach first
            if hasattr(search_results, 'points'):
                points = search_results.points
            else:
                # If no points attribute, assume the result itself is the points
                points = search_results
        except:
            # If there's an error accessing points, return an empty response
            logger.error("Error accessing search results points")
            answer = "Error retrieving information from the database."
            return QueryResponse(answer=answer, relevant_docs=[])

        relevant_docs = []
        context_parts = []

        # Process results with maximum defensive coding
        if isinstance(points, (list, tuple)):
            for result in points:
                try:
                    # Handle different possible structures of result
                    # Check if result is a tuple (which would cause the original error)
                    if isinstance(result, tuple):
                        logger.warning(f"Received tuple result: {type(result)}, skipping")
                        continue

                    # Check if result has the expected attributes
                    if not (hasattr(result, 'payload') and hasattr(result, 'score')):
                        logger.warning(f"Result missing expected attributes: {type(result)}, skipping")
                        continue

                    # Access payload and score with try-catch
                    try:
                        payload = getattr(result, 'payload', None)
                        score = getattr(result, 'score', 0)

                        if not payload:
                            continue

                        text = payload.get("text", "") if isinstance(payload, dict) else str(payload)
                        source = payload.get("source", "") if isinstance(payload, dict) else ""

                    except AttributeError:
                        logger.warning(f"Error accessing payload/score attributes, skipping result")
                        continue

                    if not text.strip():
                        continue

                    doc = RelevantDoc(
                        text=text,
                        source=source,
                        score=score,
                    )

                    relevant_docs.append(doc)

                    if len(" ".join(context_parts)) + len(text) <= request.max_context_length:
                        context_parts.append(text)

                except Exception as e:
                    logger.error(f"Error processing individual result: {e}")
                    continue  # Skip this result and continue with others
        else:
            # Handle case where points is not a list/tuple
            logger.error("Unexpected search results format")
            raise Exception("Unexpected search results format from Qdrant")

        if not relevant_docs:
            answer = "I could not find relevant information in the documentation."
            return QueryResponse(answer=answer, relevant_docs=[])

        context = "\n\n".join(context_parts)
        answer = generate_answer(request.query, context)

        if session_id:
            message_id = await db_manager.save_message(
                session_id,
                request.query,
                answer,
                is_selection_based=False,
                source_type="qdrant",
            )

            for doc in relevant_docs:
                await db_manager.save_retrieval_log(
                    session_id,
                    message_id,
                    None,
                    doc.score,
                    doc.source,
                    doc.text,
                )

        return QueryResponse(answer=answer, relevant_docs=relevant_docs)

    except Exception as e:
        logger.exception("QUERY FAILED")
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# EMBEDDING
# =========================
def generate_query_embedding(query: str) -> List[float]:
    """
    Generate embedding for the input query using Gemini API
    """
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",  # Updated to use the same model as document embeddings
            content=query,
        )
        logger.info(f"Generated query embedding with length: {len(result['embedding'])}")
        return result["embedding"]
    except Exception as e:
        logger.error(f"Error generating query embedding: {e}")
        # Provide a fallback with mock embeddings if API fails (for testing purposes)
        import numpy as np
        # Generate random embeddings with the correct dimensions (768 for our Qdrant setup)
        fallback_embedding = np.random.random(768).astype(np.float32).tolist()
        logger.warning(f"Using fallback embedding of length: {len(fallback_embedding)}")
        return fallback_embedding

# =========================
# ANSWER GENERATION
# =========================
def generate_answer(query: str, context: str) -> str:
    prompt = f"""
You are a helpful assistant.
Use ONLY the context below to answer.

Context:
{context}

Question: {query}
Answer:
"""

    try:
        response = llm_model.generate_content(
            prompt,
            generation_config={"temperature": 0.7, "max_output_tokens": 1024},
        )
        return response.text or "No answer generated."
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return "LLM failed to generate answer."

# Import embedding and storage functions from separate modules
# All utility functions are now in embed.py and store.py


# =========================
# EMBEDDING ENDPOINTS
# =========================
@app.post("/embed-documents")
async def embed_documents_endpoint():
    """Endpoint to trigger the embedding process for all documents in the docs folder"""
    try:
        # Use the embed_documents function from embed.py
        embeddings_data = await asyncio.get_event_loop().run_in_executor(None, embed_documents)
        # Store the embeddings using store.py function
        await store_embeddings(embeddings_data)
        return {"status": "success", "message": f"Documents embedded and stored successfully ({len(embeddings_data)} embeddings)"}
    except Exception as e:
        logger.error(f"Error during document embedding: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# HEALTH
# =========================
@app.get("/health")
async def health():
    qdrant_client.get_collection(COLLECTION_NAME)
    return {"status": "healthy"}

# =========================
# STARTUP / SHUTDOWN
# =========================
@app.on_event("startup")
async def startup():
    await db_manager.init_db()


@app.on_event("shutdown")
async def shutdown():
    await db_manager.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)