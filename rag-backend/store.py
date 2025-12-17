"""
store.py - Store embeddings in Qdrant
"""
import os
import logging
import dotenv
from qdrant_client import QdrantClient
from typing import List, Dict

# Load environment variables
dotenv.load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "docusaurus-rag"

# Initialize Qdrant client
if QDRANT_API_KEY:
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    qdrant_client = QdrantClient(host="localhost", port=6333)


async def create_collection():
    """
    Creates a Qdrant collection if it doesn't exist
    """
    try:
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)
        logger.info(f"Collection '{COLLECTION_NAME}' already exists.")
    except Exception:
        # Collection doesn't exist, create it
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config={
                "size": 768,  # Adjust size based on your embedding model output
                "distance": "Cosine"
            },
        )
        logger.info(f"Collection '{COLLECTION_NAME}' created.")


async def store_embeddings(embeddings: List[Dict]):
    """
    Store embeddings in Qdrant collection
    """
    await create_collection()

    # Prepare points for insertion
    points = []
    for idx, data in enumerate(embeddings):
        point = {
            "id": idx,
            "vector": data["embedding"],
            "payload": {
                "text": data["text"],
                "source": data["source"]
            }
        }
        points.append(point)

    # Batch insert for performance
    BATCH_SIZE = 100
    for i in range(0, len(points), BATCH_SIZE):
        batch = points[i:i + BATCH_SIZE]
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch,
        )

    logger.info(f"Stored {len(embeddings)} embeddings in collection '{COLLECTION_NAME}'.")


async def search_embeddings(query_embedding: List[float], limit: int = 3) -> List[Dict]:
    """
    Search for similar embeddings in Qdrant
    """
    search_results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        with_payload=True
    )

    # Handle the QueryResponse object - check if it has points attribute
    if hasattr(search_results, 'points'):
        points = search_results.points
    else:
        # Fallback for different response structure
        points = search_results

    results = []
    # Process results with maximum defensive coding
    if isinstance(points, (list, tuple)):
        for result in points:
            try:
                # Handle different possible structures of result
                # Check if result is a tuple (which would cause the original error)
                if isinstance(result, tuple):
                    logger.warning(f"Received tuple result in search_embeddings: {type(result)}, skipping")
                    continue

                # Check if result has the expected attributes
                if not hasattr(result, 'payload'):
                    logger.warning(f"Result missing payload attribute in search_embeddings: {type(result)}, skipping")
                    continue

                # Access payload with try-catch
                try:
                    payload = getattr(result, 'payload', None)

                    if payload:
                        results.append(payload)

                except AttributeError:
                    logger.warning(f"Error accessing payload attribute in search_embeddings, skipping result")
                    continue

            except Exception as e:
                logger.error(f"Error processing individual result in search_embeddings: {e}")
                continue  # Skip this result and continue with others
    else:
        # Handle case where points is not a list/tuple
        logger.error("Unexpected search results format in search_embeddings")
        raise Exception("Unexpected search results format from Qdrant in search_embeddings")

    return results


def test_connection():
    """
    Test connection to Qdrant
    """
    try:
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)
        logger.info(f"✅ Successfully connected to Qdrant collection '{COLLECTION_NAME}'")
        logger.info(f"Collection has {collection_info.points_count} vectors")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to connect to Qdrant: {e}")
        return False


if __name__ == "__main__":
    import asyncio
    success = test_connection()
    if success:
        print("Qdrant connection test passed!")
    else:
        print("Qdrant connection test failed!")