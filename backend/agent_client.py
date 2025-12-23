"""Gemini API client for text generation and Sentence Transformers for embeddings."""

import google.generativeai as genai
from typing import List
from config import AgentConfig
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Gemini API for text generation and Sentence Transformers for embeddings."""

    def __init__(self, config: AgentConfig):
        """Initialize Gemini client with configuration."""
        self.config = config
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel(config.model_name)

        # Initialize Sentence Transformer for embeddings
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        logger.info(f"Initialized Gemini client with model: {config.model_name}")
        logger.info(f"Initialized Sentence Transformer: all-MiniLM-L6-v2")

    def generate_embedding(self, text: str, task_type: str = "retrieval_document") -> List[float]:
        """
        Generate embedding for text using Sentence Transformers.

        Args:
            text: Text to embed
            task_type: Type of embedding task (kept for API compatibility, not used by Sentence Transformers)

        Returns:
            List of floats representing the embedding vector

        Raises:
            Exception: If embedding generation fails
        """
        try:
            # Generate embedding using Sentence Transformer
            embedding = self.embedding_model.encode(text, convert_to_tensor=False)
            # Convert numpy array to list
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            raise Exception(f"Failed to generate embedding: {str(e)}")

    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        """
        Generate answer based on question and retrieved context chunks.

        Args:
            question: User's question
            context_chunks: List of retrieved text chunks from the book

        Returns:
            Generated answer as string

        Raises:
            Exception: If answer generation fails
        """
        try:
            # Combine chunks into context
            context = "\n\n".join(context_chunks)

            # Create prompt for natural, conversational answers
            prompt = f"""You are an expert AI assistant helping users understand Physical AI and Humanoid Robotics.

Use the following information from the book to answer the user's question:

{context}

Question: {question}

Instructions:
- Provide a clear, concise, and natural answer
- Write in a friendly, conversational tone
- Don't mention "excerpts", "provided information", or "the text above"
- Answer as if you're explaining the concept directly
- If the information doesn't fully answer the question, provide what you can without explicitly saying the information is limited
- Keep your answer focused and relevant

Answer:"""

            # Generate answer
            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            logger.error(f"Answer generation failed: {str(e)}")
            raise Exception(f"Failed to generate answer: {str(e)}")
