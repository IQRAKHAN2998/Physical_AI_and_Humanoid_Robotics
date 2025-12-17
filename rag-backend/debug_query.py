#!/usr/bin/env python3
"""
Debug script to test Qdrant query functionality
"""
import os
import dotenv
import numpy as np
from qdrant_client import QdrantClient

# Load environment
dotenv.load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "docusaurus-rag"

# Initialize Qdrant client
if QDRANT_API_KEY:
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    qdrant_client = QdrantClient(host="localhost", port=6333)

def test_query_points():
    """Test the query_points method directly"""
    print("Testing query_points method...")

    # Create a simple test embedding (768 dimensions like our system)
    test_embedding = np.random.random(768).astype(np.float32).tolist()

    try:
        # Test the query_points call
        result = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=test_embedding,
            limit=3,
            with_payload=True
        )

        print(f"Result type: {type(result)}")
        print(f"Has 'points' attribute: {hasattr(result, 'points')}")

        if hasattr(result, 'points'):
            points = result.points
            print(f"Points type: {type(points)}")
            print(f"Points length: {len(points) if hasattr(points, '__len__') else 'N/A'}")

            if isinstance(points, (list, tuple)) and len(points) > 0:
                first_point = points[0]
                print(f"First point type: {type(first_point)}")
                print(f"First point has 'payload': {hasattr(first_point, 'payload')}")
                print(f"First point has 'score': {hasattr(first_point, 'score')}")

                if hasattr(first_point, 'payload'):
                    print(f"First point payload type: {type(first_point.payload)}")
                    print(f"First point payload content: {first_point.payload}")

        else:
            print("Result does not have 'points' attribute")
            # Print all attributes to understand the structure
            attrs = [attr for attr in dir(result) if not attr.startswith('_')]
            print(f"Result attributes: {attrs}")

    except Exception as e:
        print(f"Error in query_points: {e}")
        import traceback
        traceback.print_exc()

def test_old_search_method():
    """Test if the old search method still works"""
    print("\nTesting old search method...")

    # Create a simple test embedding
    test_embedding = np.random.random(768).astype(np.float32).tolist()

    try:
        # Test the old search call (for comparison)
        result = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=test_embedding,
            limit=3,
            with_payload=True
        )

        print(f"Old search result type: {type(result)}")
        print(f"Old search result length: {len(result) if isinstance(result, (list, tuple)) else 'N/A'}")

        if isinstance(result, (list, tuple)) and len(result) > 0:
            first_point = result[0]
            print(f"Old search first point type: {type(first_point)}")
            print(f"Old search first point has 'payload': {hasattr(first_point, 'payload')}")
            print(f"Old search first point has 'score': {hasattr(first_point, 'score')}")

    except Exception as e:
        print(f"Old search method error (expected): {e}")

if __name__ == "__main__":
    print("Debugging Qdrant client response structure...")
    test_query_points()
    test_old_search_method()