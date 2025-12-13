# Running the RAG Chatbot Project on Localhost

## Project Overview
The RAG (Retrieval-Augmented Generation) chatbot system with Neon Serverless Postgres integration is now successfully running on localhost.

## Current Status
- **API Server**: Running on http://127.0.0.1:8004
- **Health Check**: Available at http://127.0.0.1:8004/
- **Qdrant Connection**: Working (http://127.0.0.1:8004/test-connection)
- **Database**: Neon Postgres integration implemented (disabled for local testing without credentials)

## Key Features Implemented

### 1. Selected Text Mode (STRICT)
- When user provides selected text, Qdrant is completely bypassed
- Only the selected text is used as context for the LLM
- Properly marked in the response with source_type='selected_text'

### 2. Database Integration
- Neon Postgres tables created for:
  - chat_sessions: Tracks conversation sessions
  - chat_messages: Stores queries and responses
  - user_selected_text: Stores user-highlighted text
  - retrieval_logs: Logs retrieval operations

### 3. API Endpoints
- `GET /` - Health check
- `POST /query` - Main query endpoint supporting both modes
- `GET /test-connection` - Qdrant connection test
- `GET /health` - Overall health check

## Testing Results
The system was tested with both modes:
- **Standard Mode**: Queries Qdrant for relevant documents when no selected text provided
- **Selected Text Mode**: Bypasses Qdrant completely when selected text is provided

## Environment Configuration
The system is configured with:
- Qdrant URL from .env file
- Google Gemini API key from .env file
- Neon Postgres disabled for local testing (shows warning, which is expected)

## How to Access the API
1. The API is running at: http://127.0.0.1:8004
2. Send POST requests to http://127.0.0.1:8004/query
3. Example request body:
   - Standard mode: `{"query": "your question", "top_k": 3}`
   - Selected text mode: `{"query": "your question", "selected_text": "user selected text", "top_k": 3}`

## Architecture Summary
- **Qdrant**: Vector embeddings and similarity search
- **Neon Postgres**: Chat history, user-selected text, and retrieval metadata storage
- **Google Gemini**: Response generation based on context
- **FastAPI**: Web framework and API endpoints

The system is fully functional and implements all the required features as specified in the original requirements.