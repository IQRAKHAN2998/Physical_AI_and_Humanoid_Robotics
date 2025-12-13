"""
Database module for Neon Serverless Postgres integration.
This module handles all database operations for the RAG chatbot system.
"""

import os
import asyncpg
import logging
from typing import List, Optional
from datetime import datetime
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

# Database configuration
NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")

class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def init_db(self):
        """Initialize the database connection pool and create tables if they don't exist."""
        if not NEON_DATABASE_URL:
            logger.warning("NEON_DATABASE_URL not set, database operations will be disabled")
            return

        try:
            # Create connection pool
            self.pool = await asyncpg.create_pool(
                NEON_DATABASE_URL,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            logger.info("Database connection pool created successfully")

            # Create tables
            await self.create_tables()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise

    async def create_tables(self):
        """Create all required tables for the RAG system."""
        if not self.pool:
            return

        async with self.pool.acquire() as conn:
            # Create chat_sessions table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Create chat_messages table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id SERIAL PRIMARY KEY,
                    session_id INTEGER REFERENCES chat_sessions(id) ON DELETE CASCADE,
                    user_query TEXT NOT NULL,
                    llm_response TEXT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    is_selection_based BOOLEAN DEFAULT FALSE,
                    source_type VARCHAR(20) DEFAULT 'qdrant'  -- 'qdrant' or 'selected_text'
                );
            """)

            # Create user_selected_text table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_selected_text (
                    id SERIAL PRIMARY KEY,
                    session_id INTEGER REFERENCES chat_sessions(id) ON DELETE CASCADE,
                    selected_text TEXT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Create retrieval_logs table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS retrieval_logs (
                    id SERIAL PRIMARY KEY,
                    session_id INTEGER REFERENCES chat_sessions(id) ON DELETE CASCADE,
                    message_id INTEGER REFERENCES chat_messages(id) ON DELETE CASCADE,
                    chunk_id VARCHAR(255),
                    similarity_score FLOAT,
                    source TEXT,
                    retrieved_text TEXT,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)

            logger.info("All tables created successfully")

    async def create_session(self) -> int:
        """Create a new chat session and return its ID."""
        if not self.pool:
            return None

        async with self.pool.acquire() as conn:
            result = await conn.fetchval(
                "INSERT INTO chat_sessions DEFAULT VALUES RETURNING id"
            )
            return result

    async def save_message(self, session_id: int, user_query: str, llm_response: str,
                          is_selection_based: bool = False, source_type: str = 'qdrant') -> int:
        """Save a chat message to the database and return its ID."""
        if not self.pool:
            return None

        async with self.pool.acquire() as conn:
            result = await conn.fetchval(
                """
                INSERT INTO chat_messages
                (session_id, user_query, llm_response, is_selection_based, source_type)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING id
                """,
                session_id, user_query, llm_response, is_selection_based, source_type
            )
            return result

    async def save_selected_text(self, session_id: int, selected_text: str) -> int:
        """Save user selected text to the database."""
        if not self.pool:
            return None

        async with self.pool.acquire() as conn:
            result = await conn.fetchval(
                """
                INSERT INTO user_selected_text
                (session_id, selected_text)
                VALUES ($1, $2)
                RETURNING id
                """,
                session_id, selected_text
            )
            return result

    async def save_retrieval_log(self, session_id: int, message_id: int, chunk_id: str,
                                similarity_score: float, source: str, retrieved_text: str) -> int:
        """Save retrieval log to the database."""
        if not self.pool:
            return None

        async with self.pool.acquire() as conn:
            result = await conn.fetchval(
                """
                INSERT INTO retrieval_logs
                (session_id, message_id, chunk_id, similarity_score, source, retrieved_text)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
                """,
                session_id, message_id, chunk_id, similarity_score, source, retrieved_text
            )
            return result

    async def close(self):
        """Close the database connection pool."""
        if self.pool:
            await self.pool.close()

# Global database manager instance
db_manager = DatabaseManager()