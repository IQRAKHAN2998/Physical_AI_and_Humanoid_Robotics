# RAG Chatbot System Architecture

## System Components

### 1. Qdrant Vector Database
- **Responsibility**: Vector embeddings and similarity search
- **Function**: Stores document chunks with their vector representations
- **Operation**: Performs semantic search to find relevant documents based on user queries
- **Technology**: Qdrant vector database with cosine similarity search

### 2. Neon Serverless Postgres
- **Responsibility**: Chat history, user-selected text, and retrieval metadata storage
- **Tables**:
  - `chat_sessions`: Tracks conversation sessions
  - `chat_messages`: Stores user queries and LLM responses with metadata
  - `user_selected_text`: Stores user-highlighted/selected text for context
  - `retrieval_logs`: Logs details of document retrieval operations
- **Operation**: Persists all conversation data and retrieval metadata

### 3. LLM (Google Gemini)
- **Responsibility**: Response generation only
- **Function**: Generates answers based on provided context
- **Operation**: Takes user queries and context to produce human-readable responses
- **Technology**: Google Gemini Pro model

## Selected Text Mode (STRICT)

### Behavior
- **Activation**: When user provides selected/highlighted text in the request
- **Bypass**: Completely bypasses Qdrant vector search
- **Context**: Uses ONLY the user-selected text as context
- **Response**: Generates answer solely from the provided selected text
- **Fallback**: If answer cannot be found in selected text, LLM indicates this limitation

### Flow Control
```
User Query + Selected Text → Selected Text Mode Activated → LLM with Selected Text Context → Response
User Query Only → Qdrant Mode Activated → Vector Search → LLM with Retrieved Context → Response
```

## Data Flow

### Standard Qdrant Mode
1. User submits query
2. Query embedding generated using Gemini embedding model
3. Vector search performed in Qdrant collection
4. Relevant documents retrieved and ranked by similarity
5. Context built from top-k most relevant documents
6. LLM generates response based on query + retrieved context
7. All data persisted to Neon Postgres:
   - Chat session created
   - Query and response saved to chat_messages table
   - Retrieval logs saved to retrieval_logs table

### Selected Text Mode
1. User submits query with selected text
2. **Qdrant search is completely skipped**
3. Selected text used directly as context
4. LLM generates response based on query + selected text
5. All data persisted to Neon Postgres:
   - Chat session created
   - Query and response saved to chat_messages table (with is_selection_based=True)
   - Selected text saved to user_selected_text table
   - Source type marked as 'selected_text'

## Database Schema

### chat_sessions
- `id`: SERIAL PRIMARY KEY
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE

### chat_messages
- `id`: SERIAL PRIMARY KEY
- `session_id`: INTEGER REFERENCES chat_sessions(id)
- `user_query`: TEXT NOT NULL
- `llm_response`: TEXT NOT NULL
- `timestamp`: TIMESTAMP WITH TIME ZONE
- `is_selection_based`: BOOLEAN DEFAULT FALSE
- `source_type`: VARCHAR(20) DEFAULT 'qdrant' ('qdrant' or 'selected_text')

### user_selected_text
- `id`: SERIAL PRIMARY KEY
- `session_id`: INTEGER REFERENCES chat_sessions(id)
- `selected_text`: TEXT NOT NULL
- `timestamp`: TIMESTAMP WITH TIME ZONE

### retrieval_logs
- `id`: SERIAL PRIMARY KEY
- `session_id`: INTEGER REFERENCES chat_sessions(id)
- `message_id`: INTEGER REFERENCES chat_messages(id)
- `chunk_id`: VARCHAR(255)
- `similarity_score`: FLOAT
- `source`: TEXT
- `retrieved_text`: TEXT
- `timestamp`: TIMESTAMP WITH TIME ZONE

## Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key for LLM and embeddings
- `QDRANT_URL`: URL for Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant (if required)
- `NEON_DATABASE_URL`: Connection string for Neon Serverless Postgres

## API Endpoints

- `GET /`: Health check
- `POST /query`: Main query endpoint supporting both standard and selected text modes
- `GET /test-connection`: Qdrant connection test
- `GET /health`: Overall health check

## Logging

- Clear distinction between QDRANT MODE and SELECTED TEXT MODE operations
- Logs indicate source of answer (Qdrant retrieved documents vs user-selected text)
- Error logging for debugging purposes