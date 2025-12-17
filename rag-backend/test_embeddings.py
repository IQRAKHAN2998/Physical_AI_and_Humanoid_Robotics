#!/usr/bin/env python3
"""
Test script to verify the embedding functionality works correctly
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the rag-backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Import the functions by running the api.py file to get access to the functions
import importlib.util
spec = importlib.util.spec_from_file_location("api", "api.py")
api_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_module)

convert_to_text = api_module.convert_to_text
split_into_chunks = api_module.split_into_chunks
generate_embedding = api_module.generate_embedding
embed_documents = api_module.embed_documents
ensure_collection_exists = api_module.ensure_collection_exists
qdrant_client = api_module.qdrant_client
logger = api_module.logger
COLLECTION_NAME = api_module.COLLECTION_NAME

def test_text_conversion():
    """Test the text conversion function with a sample markdown file"""
    print("Testing text conversion...")

    # Find a sample markdown file from the docs directory
    docs_path = Path("D:/4_quarter4_AIDD/Physical_AI_and_Humanoid_Robotics/docs")
    sample_md_file = next(docs_path.rglob("*.md"), None)

    if sample_md_file:
        print(f"Converting file: {sample_md_file}")
        try:
            text = convert_to_text(str(sample_md_file))
            print(f"Successfully converted {sample_md_file.name}")
            print(f"Text length: {len(text)} characters")
            print(f"First 100 chars: {text[:100]}...")
            return True
        except Exception as e:
            print(f"Error converting {sample_md_file}: {e}")
            return False
    else:
        print("No markdown files found to test with")
        return False

def test_chunking():
    """Test the chunking function"""
    print("\nTesting chunking...")

    sample_text = "This is a sample text. " * 200  # Create a longer text
    chunks = split_into_chunks(sample_text, min_words=50, max_words=100)

    print(f"Split into {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:2]):  # Show first 2 chunks
        print(f"Chunk {i+1}: {len(chunk)} characters")

    return len(chunks) > 0

def test_embedding():
    """Test the embedding function with a sample text"""
    print("\nTesting embedding generation...")

    sample_text = "This is a test sentence for embedding."
    try:
        embedding = generate_embedding(sample_text)
        print(f"Generated embedding with {len(embedding)} dimensions")
        print(f"First 5 values: {embedding[:5]}")
        return len(embedding) > 0
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return False

def test_collection_ensure():
    """Test the collection creation function"""
    print("\nTesting collection ensure...")
    try:
        asyncio.run(ensure_collection_exists())
        print("Collection check completed successfully")
        return True
    except Exception as e:
        print(f"Error checking collection: {e}")
        return False

def test_full_embedding_process():
    """Test the full embedding process (this might take a while)"""
    print("\nTesting full embedding process...")
    try:
        asyncio.run(embed_documents())
        print("Full embedding process completed successfully")
        return True
    except Exception as e:
        print(f"Error in full embedding process: {e}")
        return False

if __name__ == "__main__":
    print("Running embedding functionality tests...\n")

    # Check if environment variables are set
    if not os.getenv("GEMINI_API_KEY") and not os.getenv("GEMINI_KEY"):
        print("⚠️  WARNING: GEMINI_API_KEY or GEMINI_KEY environment variable not set!")
        print("Embedding tests will likely fail without a valid API key.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(1)

    results = []

    # Run tests
    results.append(("Text conversion", test_text_conversion()))
    results.append(("Chunking", test_chunking()))
    results.append(("Embedding generation", test_embedding()))
    results.append(("Collection ensure", test_collection_ensure()))

    # Summary
    print("\n" + "="*50)
    print("TEST RESULTS SUMMARY:")
    print("="*50)

    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Please check the output above.")