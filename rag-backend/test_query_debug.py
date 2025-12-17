#!/usr/bin/env python3
"""
Test script to simulate the exact query process and identify where the error occurs
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'rag-backend'))

import dotenv
import asyncio
from qdrant_client import QdrantClient
import google.generativeai as genai
from pydantic import BaseModel
from typing import List

# Load environment
dotenv.load_dotenv()

# Configuration (copied from api.py)
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_KEY")
COLLECTION_NAME = "docusaurus-rag"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY or GEMINI_KEY is required")

# Initialize clients
genai.configure(api_key=GEMINI_API_KEY)
try:
    llm_model = genai.GenerativeModel("gemini-pro")
except Exception:
    llm_model = genai.GenerativeModel("gemini-1.5-flash")

if QDRANT_API_KEY:
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    qdrant_client = QdrantClient(host="localhost", port=6333)

# Test the query embedding generation function
def generate_query_embedding(query: str):
    """
    Generate embedding for the input query using Gemini API
    """
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
        )
        print(f"Generated query embedding with length: {len(result['embedding'])}")
        return result["embedding"]
    except Exception as e:
        print(f"Error generating query embedding: {e}")
        import numpy as np
        # Generate random embeddings with the correct dimensions (768 for our Qdrant setup)
        fallback_embedding = np.random.random(768).astype(np.float32).tolist()
        print(f"Using fallback embedding of length: {len(fallback_embedding)}")
        return fallback_embedding

# Test the exact process from the query endpoint
async def test_query_process():
    print("Testing the exact query process that happens in the API...")

    # Step 1: Generate query embedding
    query = "What is this course about?"
    print(f"Step 1: Generating embedding for query: '{query}'")
    query_embedding = generate_query_embedding(query)
    print(f"Query embedding generated: {len(query_embedding)} dimensions")

    # Step 2: Query Qdrant
    print("Step 2: Querying Qdrant with query_points")
    try:
        search_results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=3,
            with_payload=True
        )
        print(f"Search results type: {type(search_results)}")
        print(f"Has 'points' attribute: {hasattr(search_results, 'points')}")

        if hasattr(search_results, 'points'):
            points = search_results.points
            print(f"Points type: {type(points)}")
            print(f"Points length: {len(points) if hasattr(points, '__len__') else 'N/A'}")

            # Step 3: Process results (this is where the error might occur)
            print("Step 3: Processing results (this is where error might occur)")

            # This is the exact code from the fixed api.py
            # Handle the QueryResponse object - check if it has points attribute
            if hasattr(search_results, 'points'):
                points = search_results.points
            else:
                # Fallback for different response structure
                points = search_results

            relevant_docs = []
            context_parts = []

            # Ensure points is iterable and process results
            if isinstance(points, (list, tuple)):
                print(f"Iterating over {len(points)} points...")
                for i, result in enumerate(points):
                    print(f"Processing result {i}: type = {type(result)}")

                    # Handle case where result might be a tuple or different structure
                    if hasattr(result, 'payload') and hasattr(result, 'score'):
                        print(f"  Result has payload and score attributes")
                        try:
                            if not result.payload:
                                print(f"  Result payload is empty, skipping")
                                continue

                            text = result.payload.get("text", "")
                            source = result.payload.get("source", "")
                            print(f"  Extracted text length: {len(text)}, source: {source}")
                        except AttributeError as e:
                            print(f"  AttributeError when accessing payload: {e}")
                            # If there's still an attribute error, skip this result
                            continue
                    else:
                        print(f"  Result doesn't have expected attributes: payload={hasattr(result, 'payload')}, score={hasattr(result, 'score')}")
                        # Handle other potential structures if needed
                        continue

                    if not text.strip():
                        print(f"  Text is empty, skipping")
                        continue

                    # Create a simple RelevantDoc-like structure for testing
                    doc = {
                        "text": text,
                        "source": source,
                        "score": result.score,
                    }
                    relevant_docs.append(doc)
                    print(f"  Added doc to relevant_docs, total: {len(relevant_docs)}")

                    # This is just for testing, not the actual limit check
                    if len(" ".join(context_parts)) + len(text) <= 2000:  # max_context_length
                        context_parts.append(text)
            else:
                print("Points is not iterable")

            print(f"Final: {len(relevant_docs)} relevant docs found")
            return relevant_docs

    except Exception as e:
        print(f"Error in query process: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("Running exact simulation of the query process...")
    result = asyncio.run(test_query_process())
    if result is not None:
        print(f"Success! Found {len(result)} relevant documents")
    else:
        print("Failed to process query")