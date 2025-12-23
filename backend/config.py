"""Configuration management using Pydantic Settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

class AgentConfig(BaseSettings):
    gemini_api_key: str = Field(..., description="Gemini API key")
    model_name: str = Field(default="models/gemini-flash-latest")

    model_config = SettingsConfigDict(
        case_sensitive=False,
        protected_namespaces=(),
        extra="ignore"
    )

class QdrantConfig(BaseSettings):
    """Qdrant vector database configuration."""

    url: str = Field(..., description="Qdrant Cloud cluster URL")
    api_key: str = Field(..., description="Qdrant API key")
    collection_name: str = Field(default="book_chunks", description="Qdrant collection name")

    class Config:
        env_file = ".env"
        env_prefix = "QDRANT_"
        case_sensitive = False


class ServerConfig(BaseSettings):
    """FastAPI server configuration."""

    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Debug mode")

    class Config:
        env_file = ".env"
        env_prefix = "SERVER_"
        case_sensitive = False


class RAGConfig(BaseSettings):
    """RAG system configuration."""

    chunk_size: int = Field(default=500, ge=100, le=1000, description="Target token count per chunk")
    chunk_overlap: int = Field(default=50, ge=0, le=200, description="Overlap tokens between chunks")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of chunks to retrieve")
    book_content_path: str = Field(default="../docs", description="Path to book markdown files")

    class Config:
        env_file = ".env"
        env_prefix = "RAG_"
        case_sensitive = False


class AppConfig:
    """Complete application configuration."""

    def __init__(self):
        self.agent = AgentConfig()
        self.qdrant = QdrantConfig()
        self.server = ServerConfig()
        self.rag = RAGConfig()


def load_config() -> AppConfig:
    """Load and validate all configuration from environment variables."""
    try:
        config = AppConfig()
        return config
    except Exception as e:
        raise ValueError(f"Configuration error: {str(e)}. Please check your .env file.")
