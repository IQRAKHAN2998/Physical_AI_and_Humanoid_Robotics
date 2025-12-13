# RAG Chatbot with Neon Postgres Integration

This is a Retrieval-Augmented Generation (RAG) chatbot system that integrates Qdrant vector search with Neon Serverless Postgres for comprehensive chat history and metadata management.

## Features

- **Qdrant Vector Search**: Semantic search in documentation using vector embeddings
- **Neon Serverless Postgres**: Persistent storage for chat sessions, messages, and retrieval logs
- **Selected Text Mode**: Special mode that bypasses vector search and uses user-provided text only
- **Google Gemini Integration**: For both embeddings and response generation
- **Session Management**: Complete conversation history tracking

## Architecture

### System Components

1. **Qdrant Vector Database**: Handles vector embeddings and similarity search
2. **Neon Serverless Postgres**: Stores chat history, user-selected text, and retrieval metadata
3. **Google Gemini**: Generates responses based on provided context

### Selected Text Mode (STRICT)

When a user provides selected/highlighted text:
- Qdrant search is completely bypassed
- Only the selected text is used as context for the LLM
- The system will respond based solely on the provided text
- If the answer cannot be found in the selected text, the LLM indicates this limitation

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key  # if required
   NEON_DATABASE_URL=your_neon_database_url
   ```

3. Run the application:
   ```bash
   python api.py
   ```

## API Endpoints

- `GET /` - Health check
- `POST /query` - Query the RAG system
  - Accepts: `{ "query": "your question", "selected_text": "optional selected text", "top_k": 5 }`
- `GET /test-connection` - Test Qdrant connection
- `GET /health` - Health check

## Database Schema

The system creates and uses the following tables:

- `chat_sessions`: Tracks conversation sessions
- `chat_messages`: Stores user queries and LLM responses
- `user_selected_text`: Stores user-highlighted text when in Selected Text Mode
- `retrieval_logs`: Logs retrieval operations from Qdrant

## Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key
- `QDRANT_URL`: Qdrant instance URL
- `QDRANT_API_KEY`: Qdrant API key (optional, for secured instances)
- `NEON_DATABASE_URL`: Neon Postgres connection string