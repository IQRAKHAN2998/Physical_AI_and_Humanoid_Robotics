import requests
import json

# Test the API endpoints
BASE_URL = "http://127.0.0.1:8004"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print("Health check:", response.json())

def test_query():
    """Test query endpoint with standard mode"""
    query_data = {
        "query": "What is the purpose of this RAG system?",
        "top_k": 3
    }

    response = requests.post(f"{BASE_URL}/query", json=query_data)
    print("Standard query response:", response.json())

def test_selected_text_mode():
    """Test query endpoint with selected text mode"""
    query_data = {
        "query": "What is Python?",
        "selected_text": "Python is a high-level programming language. It is easy to learn and widely used for various applications.",
        "top_k": 3
    }

    response = requests.post(f"{BASE_URL}/query", json=query_data)
    print("Selected text mode response:", response.json())

if __name__ == "__main__":
    print("Testing RAG API endpoints...")
    test_health()
    print()

    print("Testing standard query mode...")
    test_query()
    print()

    print("Testing selected text mode...")
    test_selected_text_mode()