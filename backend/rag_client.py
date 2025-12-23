"""RAG system components: chunking, parsing, Qdrant management, and RAG pipeline."""

import os
import re
import uuid
import tiktoken
import logging
from typing import List, Dict, Tuple
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from config import QdrantConfig, RAGConfig
from agent_client import GeminiClient

logger = logging.getLogger(__name__)


class TextChunker:
    """Handles text chunking using token-based splitting."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """Initialize text chunker with tiktoken encoder."""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoder = tiktoken.get_encoding("cl100k_base")
        logger.info(f"Initialized TextChunker (size={chunk_size}, overlap={chunk_overlap})")

    def chunk_text(self, text: str, source_file: str) -> List[Dict]:
        """
        Split text into chunks of approximately chunk_size tokens with overlap.

        Args:
            text: Text to chunk
            source_file: Source file path for metadata

        Returns:
            List of chunk dictionaries with content and metadata
        """
        tokens = self.encoder.encode(text)
        chunks = []
        stride = self.chunk_size - self.chunk_overlap

        for i in range(0, len(tokens), stride):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.encoder.decode(chunk_tokens)

            module = source_file.split("/")[-2] if len(source_file.split("/")) >= 2 else ""
            chapter = source_file.split("/")[-1]

            chunks.append({
                "content": chunk_text,
                "source_file": source_file,
                "module": module,
                "chapter": chapter,
                "chunk_index": len(chunks),
                "start_token": i,
                "token_count": len(chunk_tokens)
            })

            if i + self.chunk_size >= len(tokens):
                break

        logger.info(f"Created {len(chunks)} chunks from {source_file}")
        return chunks


class MarkdownParser:
    """Handles markdown and MDX file parsing and cleaning."""

    @staticmethod
    def parse_markdown(file_path: str) -> Dict[str, str]:
        """
        Parse markdown/MDX file and clean content.

        Args:
            file_path: Path to markdown or MDX file

        Returns:
            Dict with source_file and cleaned content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove YAML front matter
            content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)

            # Remove import/export lines (MDX)
            content = re.sub(r'^(import|export).*$',
                             '',
                             content,
                             flags=re.MULTILINE)

            # Remove JSX tags but keep text
            content = re.sub(r'<[^>]+>', '', content)

            # Remove code blocks
            content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

            # Remove inline code
            content = re.sub(r'`[^`]+`', '', content)

            # Remove HTML comments
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

            # Normalize whitespace
            content = re.sub(r'\n{2,}', '\n\n', content)

            return {
                "source_file": file_path,
                "content": content.strip()
            }

        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {str(e)}")
            raise


class QdrantManager:
    """Manages Qdrant vector database operations."""

    def __init__(self, config: QdrantConfig):
        """Initialize Qdrant client."""
        self.config = config
        self.client = QdrantClient(
            url=config.url,
            api_key=config.api_key,
            timeout=10.0
        )
        self.collection_name = config.collection_name
        logger.info(f"Initialized Qdrant client: {config.url}")

    def create_collection(self, vector_size: int = 384):
        """
        Create Qdrant collection for storing embeddings.

        Args:
            vector_size: Dimension of embedding vectors
        """
        try:
            collections = self.client.get_collections().collections
            if any(c.name == self.collection_name for c in collections):
                logger.info(f"Collection '{self.collection_name}' already exists")
                return

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            logger.info(f"Created collection: {self.collection_name}")

        except Exception as e:
            logger.error(f"Failed to create collection: {str(e)}")
            raise

    def upload_chunks(self, chunks: List[Dict], embeddings: List[List[float]]):
        """
        Upload chunks and embeddings to Qdrant.

        Args:
            chunks: List of chunk dicts with metadata
            embeddings: List of embedding vectors
        """
        try:
            points = []
            for chunk, embedding in zip(chunks, embeddings):
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=chunk
                )
                points.append(point)

            batch_size = 100
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch
                )

            logger.info(f"Uploaded {len(points)} points to Qdrant")

        except Exception as e:
            logger.error(f"Failed to upload chunks: {str(e)}")
            raise

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        """
        Search for similar chunks using query embedding.

        Args:
            query_embedding: Embedding vector for the query
            top_k: Number of results to return

        Returns:
            List of retrieved chunks with scores
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )

            chunks = []
            for result in results:
                chunks.append({
                    "content": result.payload["content"],
                    "source_file": result.payload["source_file"],
                    "score": result.score
                })

            logger.info(f"Retrieved {len(chunks)} chunks from Qdrant")
            return chunks

        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise

    def health_check(self) -> bool:
        """Check if Qdrant connection is healthy."""
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {str(e)}")
            return False


class RAGPipeline:
    """Orchestrates the RAG question-answering pipeline."""

    def __init__(self, gemini_client: GeminiClient, qdrant_manager: QdrantManager, top_k: int = 3):
        self.gemini_client = gemini_client
        self.qdrant_manager = qdrant_manager
        self.top_k = top_k
        logger.info("Initialized RAG pipeline")

    def ask(self, question: str) -> Tuple[str, List[str]]:
        try:
            query_embedding = self.gemini_client.generate_embedding(
                question,
                task_type="retrieval_query"
            )

            chunks = self.qdrant_manager.search(query_embedding, self.top_k)

            if not chunks:
                return "I couldn't find any relevant information in the book to answer your question.", []

            context_chunks = [chunk["content"] for chunk in chunks]

            # Extract clean source names (unique chapter/file names)
            source_files = []
            for chunk in chunks:
                source_file = chunk["source_file"]
                # Extract readable name from path
                chapter_name = source_file.split("/")[-1].replace(".md", "").replace(".mdx", "")
                # Clean up the name for display
                clean_name = chapter_name.replace("-", " ").replace("_", " ").title()
                if clean_name not in source_files:
                    source_files.append(clean_name)

            answer = self.gemini_client.generate_answer(question, context_chunks)

            return answer, source_files

        except Exception as e:
            logger.error(f"RAG pipeline failed: {str(e)}")
            raise


def discover_markdown_files(docs_path: str) -> List[str]:
    """
    Discover all markdown and MDX files in docs directory.

    Args:
        docs_path: Path to docs folder

    Returns:
        List of markdown/mdx file paths
    """
    files = []
    for root, _, filenames in os.walk(docs_path):
        for filename in filenames:
            if filename.lower().endswith((".md", ".mdx")):
                files.append(os.path.join(root, filename))

    logger.info(f"Discovered {len(files)} markdown/mdx files in {docs_path}")
    return files

