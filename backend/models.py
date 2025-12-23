"""Pydantic models for API request/response and error handling."""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any, Union
import uuid


# Error code constants
VALIDATION_ERROR = "VALIDATION_ERROR"
QUESTION_EMPTY = "QUESTION_EMPTY"
QUESTION_TOO_LONG = "QUESTION_TOO_LONG"
API_ERROR = "API_ERROR"
EMBEDDING_ERROR = "EMBEDDING_ERROR"
SEARCH_ERROR = "SEARCH_ERROR"
SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"


class ChatRequest(BaseModel):
    """User input for the /ask endpoint."""

    question: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="User's question about the book content"
    )

    @field_validator('question')
    @classmethod
    def question_not_empty(cls, v: str) -> str:
        """Validate that question is not empty or whitespace-only."""
        if not v.strip():
            raise ValueError('Question cannot be empty or whitespace-only')
        return v.strip()


class ChatResponse(BaseModel):
    """Successful response from the /ask endpoint."""

    answer: str = Field(..., description="Generated answer based on retrieved book content")
    request_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for this request"
    )
    sources: Optional[List[str]] = Field(
        default=None,
        description="List of source chapter/file names"
    )


class ErrorResponse(BaseModel):
    """Error response from any endpoint."""

    error: str = Field(..., description="Human-readable error message")
    error_code: str = Field(..., description="Machine-readable error code")
    request_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this request"
    )
    detail: Optional[Union[str, Dict[str, Any]]] = Field(
        default=None,
        description="Optional additional error details"
    )


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Overall health status")
    qdrant_connected: bool = Field(..., description="Qdrant connection status")
    gemini_api_available: Optional[bool] = Field(
        default=None,
        description="Gemini API availability (optional check)"
    )
    error: Optional[str] = Field(default=None, description="Error message if unhealthy")
