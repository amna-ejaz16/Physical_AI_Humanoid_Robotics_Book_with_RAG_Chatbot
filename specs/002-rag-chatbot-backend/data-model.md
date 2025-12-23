# Data Model: RAG Chatbot Backend

**Feature**: RAG Chatbot Backend
**Branch**: 002-rag-chatbot-backend
**Date**: 2025-12-09

## Overview

This document defines all data entities, their structures, relationships, validation rules, and state transitions for the RAG chatbot backend system.

---

## Entity Definitions

### 1. TextChunk

**Purpose**: Represents a segment of book content with its vector embedding for semantic search.

**Storage**: Qdrant vector database collection `book_chunks`

**Fields**:

| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| `id` | UUID (string) | Yes | Unique identifier for the chunk |
| `vector` | List[float] | Yes | 768-dimensional embedding vector from Gemini text-embedding-004 |
| `content` | String | Yes | Raw text content (~500 tokens) |
| `source_file` | String | Yes | Relative path to source markdown file (e.g., "docs/chapters/01-introduction.md") |
| `chunk_index` | Integer | Yes | Sequential position within source file (0-indexed) |
| `start_char` | Integer | Yes | Character offset where chunk starts in source file |
| `end_char` | Integer | Yes | Character offset where chunk ends in source file |
| `token_count` | Integer | Yes | Number of tokens in content (for validation) |

**Payload Structure** (in Qdrant):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "vector": [0.123, 0.456, ..., 0.789],  // 768 floats
  "payload": {
    "content": "Physical AI refers to artificial intelligence systems...",
    "source_file": "docs/chapters/01-introduction.md",
    "chunk_index": 0,
    "start_char": 0,
    "end_char": 1250,
    "token_count": 498
  }
}
```

**Validation Rules**:
- `id`: Must be valid UUID v4 format
- `vector`: Must have exactly 768 dimensions (matching embedding model)
- `content`: Must be non-empty; length should correspond to ~500 tokens
- `token_count`: Must be between 1 and 600 (allowing slight variance from target 500)
- `chunk_index`: Must be non-negative
- `start_char` < `end_char`

**Relationships**: None (flat collection structure in vector database)

**State Transitions**:
1. **Created** (during indexing): Generated from book content with embedding
2. **Indexed** (in Qdrant): Stored in vector database collection
3. **Retrieved** (during search): Fetched based on similarity to query embedding
4. **Immutable**: Once created, chunks are never modified (re-indexing creates new chunks)

**Indexing Strategy**:
- Qdrant collection uses Cosine distance for similarity
- No additional indexes beyond vector index
- Metadata stored in payload for filtering (future enhancement)

---

### 2. ChatRequest

**Purpose**: User input for the `/ask` endpoint.

**Storage**: Not persisted (request-only)

**Pydantic Model**:
```python
from pydantic import BaseModel, Field, validator

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="User's question about the book content"
    )

    @validator('question')
    def question_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Question cannot be empty or whitespace-only')
        return v.strip()
```

**Fields**:

| Field Name | Type | Required | Constraints | Description |
|------------|------|----------|-------------|-------------|
| `question` | String | Yes | 1-4000 characters, non-empty, non-whitespace | User's natural language question |

**Validation Rules**:
- Must be valid UTF-8 string
- After stripping whitespace, length must be ≥ 1 character
- Maximum length: 4000 characters (prevents abuse and API overload)
- No special format required (free-form natural language)

**Example Valid Requests**:
```json
{
  "question": "What is physical AI?"
}
```

```json
{
  "question": "Explain how reinforcement learning is used in humanoid robotics, particularly for locomotion tasks."
}
```

**Example Invalid Requests**:
```json
{
  "question": ""
}
// Error: QUESTION_EMPTY
```

```json
{
  "question": "   "
}
// Error: QUESTION_EMPTY (whitespace-only)
```

```json
{
  "question": "a" * 5000
}
// Error: QUESTION_TOO_LONG
```

---

### 3. ChatResponse

**Purpose**: Successful response from the `/ask` endpoint.

**Storage**: Not persisted (response-only)

**Pydantic Model**:
```python
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class ChatResponse(BaseModel):
    answer: str = Field(
        ...,
        description="Generated answer based on retrieved book content"
    )
    request_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this request"
    )
    sources: Optional[List[str]] = Field(
        default=None,
        description="List of source file paths used to generate answer"
    )
```

**Fields**:

| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| `answer` | String | Yes | AI-generated answer synthesized from retrieved chunks |
| `request_id` | UUID (string) | Yes | Unique identifier for request tracing and debugging |
| `sources` | List[String] | No | Optional list of source markdown files used (for transparency) |

**Example Response**:
```json
{
  "answer": "Physical AI refers to artificial intelligence systems that are embodied in physical robots or agents. Unlike purely software-based AI, physical AI must interact with the real world through sensors and actuators. The book discusses how physical AI systems must handle uncertainty, sensor noise, and real-time constraints that don't exist in simulated environments.",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "sources": [
    "docs/chapters/01-introduction.md",
    "docs/chapters/02-embodied-intelligence.md"
  ]
}
```

**Business Rules**:
- `answer` should synthesize information from multiple chunks (not verbatim copy)
- `sources` should list unique file paths (no duplicates)
- `request_id` must be included in error responses as well for correlation

---

### 4. ErrorResponse

**Purpose**: Error response from any endpoint when something goes wrong.

**Storage**: Not persisted (response-only)

**Pydantic Model**:
```python
from pydantic import BaseModel, Field
from typing import Optional, Union, Dict, Any
import uuid

class ErrorResponse(BaseModel):
    error: str = Field(
        ...,
        description="Human-readable error message"
    )
    error_code: str = Field(
        ...,
        description="Machine-readable error code"
    )
    request_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this request"
    )
    detail: Optional[Union[str, Dict[str, Any]]] = Field(
        default=None,
        description="Optional additional error details"
    )
```

**Fields**:

| Field Name | Type | Required | Description |
|------------|------|----------|-------------|
| `error` | String | Yes | Human-readable error message for display to users |
| `error_code` | String | Yes | Machine-readable error code for programmatic handling |
| `request_id` | UUID (string) | Yes | Unique identifier for request tracing |
| `detail` | String or Object | No | Optional additional context (validation errors, stack traces in debug mode) |

**Error Code Taxonomy**:

| Error Code | HTTP Status | Description | Example Scenario |
|------------|-------------|-------------|------------------|
| `VALIDATION_ERROR` | 400 | Generic validation failure | Invalid JSON structure |
| `QUESTION_EMPTY` | 400 | Question is empty or whitespace-only | `{"question": ""}` |
| `QUESTION_TOO_LONG` | 400 | Question exceeds 4000 characters | Very long input |
| `API_ERROR` | 500 | Gemini API request failed | Rate limit, API key invalid, network error |
| `EMBEDDING_ERROR` | 500 | Failed to generate embedding | Gemini embedding API failure |
| `SEARCH_ERROR` | 500 | Qdrant search failed | Vector DB connection issue |
| `SERVICE_UNAVAILABLE` | 500 | General server error | Unexpected exception |

**Example Error Responses**:

```json
{
  "error": "Question cannot be empty",
  "error_code": "QUESTION_EMPTY",
  "request_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901"
}
```

```json
{
  "error": "Gemini API request failed",
  "error_code": "API_ERROR",
  "request_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "detail": "Rate limit exceeded. Please retry after 60 seconds."
}
```

```json
{
  "error": "Validation failed",
  "error_code": "VALIDATION_ERROR",
  "request_id": "d4e5f6a7-b8c9-0123-def1-234567890123",
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### 5. Configuration Entities

**Purpose**: Environment-based settings for application configuration.

**Storage**: Environment variables (`.env` file) loaded via Pydantic Settings

#### 5.1 AgentConfig

**Pydantic Settings Model**:
```python
from pydantic_settings import BaseSettings
from pydantic import Field

class AgentConfig(BaseSettings):
    gemini_api_key: str = Field(
        ...,
        description="Gemini API key from Google AI Studio"
    )
    model_name: str = Field(
        default="gemini-1.5-flash",
        description="Gemini model for text generation"
    )
    embedding_model: str = Field(
        default="models/text-embedding-004",
        description="Gemini embedding model"
    )

    class Config:
        env_prefix = "GEMINI_"
        case_sensitive = False
```

**Fields**:

| Field Name | Environment Variable | Type | Required | Default | Description |
|------------|---------------------|------|----------|---------|-------------|
| `gemini_api_key` | `GEMINI_API_KEY` | String | Yes | - | API key for Gemini |
| `model_name` | `GEMINI_MODEL` | String | No | `gemini-1.5-flash` | Model for text generation |
| `embedding_model` | `GEMINI_EMBEDDING_MODEL` | String | No | `models/text-embedding-004` | Model for embeddings |

---

#### 5.2 QdrantConfig

**Pydantic Settings Model**:
```python
class QdrantConfig(BaseSettings):
    url: str = Field(
        ...,
        description="Qdrant Cloud cluster URL"
    )
    api_key: str = Field(
        ...,
        description="Qdrant API key"
    )
    collection_name: str = Field(
        default="book_chunks",
        description="Qdrant collection name"
    )

    class Config:
        env_prefix = "QDRANT_"
        case_sensitive = False
```

**Fields**:

| Field Name | Environment Variable | Type | Required | Default | Description |
|------------|---------------------|------|----------|---------|-------------|
| `url` | `QDRANT_URL` | String | Yes | - | Qdrant Cloud cluster URL |
| `api_key` | `QDRANT_API_KEY` | String | Yes | - | Qdrant API key |
| `collection_name` | `QDRANT_COLLECTION` | String | No | `book_chunks` | Collection name for vectors |

---

#### 5.3 ServerConfig

**Pydantic Settings Model**:
```python
class ServerConfig(BaseSettings):
    host: str = Field(
        default="0.0.0.0",
        description="Server host"
    )
    port: int = Field(
        default=8000,
        description="Server port"
    )
    debug: bool = Field(
        default=False,
        description="Debug mode"
    )

    class Config:
        env_prefix = "SERVER_"
        case_sensitive = False
```

**Fields**:

| Field Name | Environment Variable | Type | Required | Default | Description |
|------------|---------------------|------|----------|---------|-------------|
| `host` | `SERVER_HOST` | String | No | `0.0.0.0` | Server bind host |
| `port` | `SERVER_PORT` | Integer | No | `8000` | Server port |
| `debug` | `SERVER_DEBUG` | Boolean | No | `False` | Enable debug mode |

---

#### 5.4 RAGConfig

**Pydantic Settings Model**:
```python
class RAGConfig(BaseSettings):
    chunk_size: int = Field(
        default=500,
        ge=100,
        le=1000,
        description="Target token count per chunk"
    )
    chunk_overlap: int = Field(
        default=50,
        ge=0,
        le=200,
        description="Overlap tokens between chunks"
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of chunks to retrieve"
    )
    book_content_path: str = Field(
        default="../docs",
        description="Path to book markdown files"
    )

    class Config:
        env_prefix = "RAG_"
        case_sensitive = False
```

**Fields**:

| Field Name | Environment Variable | Type | Required | Default | Constraints | Description |
|------------|---------------------|------|----------|---------|-------------|-------------|
| `chunk_size` | `RAG_CHUNK_SIZE` | Integer | No | `500` | 100-1000 | Target tokens per chunk |
| `chunk_overlap` | `RAG_CHUNK_OVERLAP` | Integer | No | `50` | 0-200 | Overlap tokens |
| `top_k` | `RAG_TOP_K` | Integer | No | `3` | 1-10 | Chunks to retrieve |
| `book_content_path` | `RAG_BOOK_CONTENT_PATH` | String | No | `../docs` | - | Path to markdown files |

---

## Data Flow Diagrams

### Indexing Flow

```
Book Content (markdown files)
    ↓
Parse & Clean
    ↓
Chunk Text (500 tokens, 50 overlap)
    ↓
Generate Embeddings (Gemini API)
    ↓
Store in Qdrant
    ↓
TextChunk entities in vector DB
```

### Query Flow

```
User Question (ChatRequest)
    ↓
Validate Input (Pydantic)
    ↓
Generate Query Embedding (Gemini API)
    ↓
Search Qdrant (top 3 chunks)
    ↓
Retrieved TextChunk entities
    ↓
Combine chunks + question → prompt
    ↓
Generate Answer (Gemini API)
    ↓
ChatResponse (with sources)
```

---

## Validation Summary

| Entity | Validation Method | Error Handling |
|--------|------------------|----------------|
| `ChatRequest` | Pydantic model validation | Return 400 with `VALIDATION_ERROR` |
| `TextChunk` | Schema validation during indexing | Log error, skip chunk, continue indexing |
| `Configuration` | Pydantic Settings with env vars | Fail fast on startup if required vars missing |
| `ChatResponse` | Auto-generated (no user input) | N/A (server-side only) |
| `ErrorResponse` | Auto-generated (no user input) | N/A (server-side only) |

---

## State Machine: Request Lifecycle

```
[Incoming Request]
    ↓
[Validate ChatRequest] → [Invalid] → [Return ErrorResponse 400]
    ↓ [Valid]
[Generate Query Embedding]
    ↓
[Search Qdrant] → [Search Fails] → [Return ErrorResponse 500]
    ↓ [Success]
[Generate Answer from Chunks] → [API Fails] → [Return ErrorResponse 500]
    ↓ [Success]
[Return ChatResponse 200]
```

---

## Storage Estimates

**Qdrant Collection**:
- Number of chunks: ~90 (estimated for 25k-45k word book)
- Vector dimension: 768 floats
- Storage per chunk: 768 × 4 bytes (float32) = 3,072 bytes = 3 KB
- Total vector storage: 90 × 3 KB = 270 KB
- Metadata per chunk: ~500 bytes (text content + metadata fields)
- Total metadata storage: 90 × 500 bytes = 45 KB
- **Total estimated storage**: ~315 KB (well within 1GB free tier limit)

---

## Next Steps

1. ✅ Data model defined with all entities, fields, and validation rules
2. → Proceed to generate API contracts (OpenAPI spec)
3. → Generate quickstart.md for developer setup
4. → Update agent context with new models and entities
