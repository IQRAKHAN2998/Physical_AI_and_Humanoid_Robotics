"""
embed.py - Generate embeddings from the book content in docs folder
"""
import os
import logging
import dotenv
import google.generativeai as genai
from pathlib import Path
import re
import html
import PyPDF2
import time
from typing import List

# Load environment variables
dotenv.load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY or GEMINI_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)

def convert_to_text(file_path: str) -> str:
    """
    Converts various file formats to plain text
    """
    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == '.md':
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown = f.read()
            # Simple markdown to text conversion (remove basic markdown syntax)
            text = re.sub(r'#{1,6}\s*', '', markdown)  # Remove headers
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold
            text = re.sub(r'\*(.*?)\*', r'\1', text)  # Remove italic
            text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Remove links
            text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # Remove images
            text = re.sub(r'`{1,3}[^`]*`{1,3}', '', text)  # Remove code blocks
            text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)  # Remove list markers
            text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)  # Remove numbered list markers
            return text.strip()
    elif ext == '.html':
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            # Simple HTML to text conversion (basic tag removal)
            text = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html_content, flags=re.IGNORECASE)  # Remove script tags
            text = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', text, flags=re.IGNORECASE)  # Remove style tags
            text = re.sub(r'<[^>]+>', ' ', text)  # Remove all other tags
            text = text.replace('&nbsp;', ' ')  # Replace non-breaking spaces
            text = html.unescape(text)  # Handle HTML entities
            text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
            return text.strip()
    elif ext == '.pdf':
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


def split_into_chunks(text: str, min_words: int = 500, max_words: int = 800) -> List[str]:
    """
    Splits text into chunks of 500-800 words
    """
    words = text.split()
    chunks = []
    start_index = 0

    while start_index < len(words):
        end_index = min(start_index + max_words, len(words))

        # If we're near the end, make sure we don't go over max_words
        if end_index - start_index <= max_words and end_index == len(words):
            chunks.append(' '.join(words[start_index:end_index]))
            break

        # If the chunk is too small, extend it
        if end_index - start_index < min_words:
            end_index = min(start_index + min_words, len(words))

        chunks.append(' '.join(words[start_index:end_index]))
        start_index = end_index

    return chunks


def generate_embedding(text: str) -> List[float]:
    """
    Generates embeddings using Gemini API
    """
    try:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
        )
        logger.info(f"Embedding length: {len(result['embedding'])}")  # Debug line
        return result['embedding']
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise e


def get_all_files(dir_path: str, supported_extensions: List[str]) -> List[str]:
    """
    Reads all files from the docs directory with supported extensions
    """
    dir_path = Path(dir_path)
    files = []

    for file_path in dir_path.rglob('*'):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext in supported_extensions:
                files.append(str(file_path))

    return files


def embed_documents(docs_path: str = "D:/4_quarter4_AIDD/Physical_AI_and_Humanoid_Robotics/docs"):
    """
    Main embedding function to convert docs to embeddings
    Returns list of embeddings with metadata
    """
    logger.info('🚀 Starting document embedding process...')

    SUPPORTED_EXTENSIONS = ['.md', '.txt', '.pdf', '.html']

    # Get all files to process
    files = get_all_files(docs_path, SUPPORTED_EXTENSIONS)
    logger.info(f'📁 Found {len(files)} files to process')

    if len(files) == 0:
        logger.info('⚠️ No supported files found in the docs directory')
        return []

    embeddings_data = []

    for file_path in files:
        logger.info(f'\n📄 Processing file: {file_path}')

        try:
            # Convert file to text
            text = convert_to_text(file_path)

            if not text.strip():
                logger.info(f'⚠️ Skipping empty file: {file_path}')
                continue

            # Split into chunks
            chunks = split_into_chunks(text)
            logger.info(f'✂️  Split into {len(chunks)} chunks')

            # Process each chunk
            for i, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue  # Skip empty chunks

                # Generate embedding
                vector = generate_embedding(chunk)

                # Add to results
                embeddings_data.append({
                    'embedding': vector,
                    'text': chunk[:10000],  # Limit text length to avoid payload size issues
                    'source': file_path,
                    'chunk_index': i
                })

                logger.info(f'✅ Chunk {i + 1}/{len(chunks)} processed')

            logger.info(f'✅ Completed processing: {file_path}')
        except Exception as error:
            logger.error(f'❌ Error processing file {file_path}: {error}')
            continue  # Continue with next file

    logger.info(f'\n📈 Summary: {len(embeddings_data)} embeddings generated')
    logger.info('✅ Embedding Generation Finished')
    return embeddings_data


if __name__ == "__main__":
    # Generate embeddings for all documents
    embeddings = embed_documents()
    print(f"Generated {len(embeddings)} embeddings from the book content")