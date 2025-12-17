# Running the Chatbot Application

## Prerequisites
- Node.js and npm installed
- Python 3.8+ installed
- Qdrant vector database running
- Google Gemini API key configured

## Environment Setup
Make sure your `.env` file contains the required configuration:

```
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
REACT_APP_RAG_API_URL=http://127.0.0.1:8000/query
```

## Running the Application

### 1. Start the Backend API
```bash
cd rag-backend
pip install -r requirements.txt
python api.py
```
The backend will start on `http://127.0.0.1:8000`

### 2. Start the Frontend
In a separate terminal:
```bash
npm install
npm start
```
The frontend will start on `http://localhost:3000`

### 3. Using the Chatbot
Once both services are running, you can use the chatbot by clicking the chat icon 💬 on the website and asking questions. The chatbot will connect to the backend API to process your queries using the RAG system.

## Troubleshooting
- If you see "Failed to fetch" errors, ensure the backend API is running on `http://127.0.0.1:8000`
- Check that your Qdrant database is accessible and contains the required collection
- Verify that your GEMINI_API_KEY is valid and has sufficient quota