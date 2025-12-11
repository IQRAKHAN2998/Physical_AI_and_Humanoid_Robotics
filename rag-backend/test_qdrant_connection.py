import asyncio
import os
from qdrant_client import QdrantClient

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "docusaurus-rag"

def test_qdrant_connection():
    """Test the Qdrant connection directly"""
    try:
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

        print(f"Testing connection to Qdrant at: {QDRANT_URL}")
        print(f"Collection name: {COLLECTION_NAME}")

        # Test connection and get collection info
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)

        print("SUCCESS: Connection successful!")
        print(f"Collection status: available")
        print(f"Vector count: {collection_info.points_count}")

        # Try to get vector dimensions
        vector_dimensions = None
        if hasattr(collection_info, 'config') and collection_info.config:
            if hasattr(collection_info.config, 'params') and collection_info.config.params:
                vector_config = collection_info.config.params.vectors
                if hasattr(vector_config, 'size'):
                    vector_dimensions = vector_config.size
                elif isinstance(vector_config, dict) and 'size' in vector_config:
                    vector_dimensions = vector_config['size']

        print(f"Vector dimensions: {vector_dimensions}")

        return True

    except Exception as e:
        print(f"ERROR: Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_qdrant_connection()