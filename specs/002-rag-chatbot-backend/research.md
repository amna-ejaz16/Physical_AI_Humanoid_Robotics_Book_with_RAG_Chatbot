# Research: RAG Chatbot Backend Technology Choices

**Feature**: RAG Chatbot Backend
**Branch**: 002-rag-chatbot-backend
**Date**: 2025-12-09

## Overview

This document captures research findings and technology decisions for implementing the RAG chatbot backend. All decisions are based on requirements from spec.md and validated against industry best practices, official documentation, and proven patterns.

---

## 1. Gemini API + OpenAI Agents SDK Integration

### Decision
Use Google's `google-generativeai` Python SDK directly instead of OpenAI Agents SDK, as Gemini API has native Python support and OpenAI Agents SDK does not natively support Gemini.

### Rationale
- **Direct Support**: Google provides an official `google-generativeai` package optimized for Gemini models
- **API Compatibility**: Gemini API does not follow OpenAI's API format exactly; using the native SDK avoids compatibility issues
- **Feature Parity**: Native SDK provides full access to Gemini's embedding and generation capabilities
- **Documentation**: Comprehensive official documentation and examples available
- **Maintenance**: First-party SDK is actively maintained by Google

### Alternatives Considered
1. **OpenAI Python SDK with custom base_url**
   - **Rejected**: Gemini API endpoints and request/response formats differ from OpenAI
   - Would require significant custom wrappers and error-prone mapping

2. **LangChain**
   - **Rejected**: Adds unnecessary complexity for simple RAG use case
   - Overkill for single-model, single-task implementation
   - Larger dependency footprint

3. **Custom HTTP client**
   - **Rejected**: Reinventing the wheel; native SDK handles auth, retries, error handling

### Implementation Details
```python
# Installation
pip install google-generativeai

# Usage
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Embedding
embedding_model = "models/text-embedding-004"
result = genai.embed_content(
    model=embedding_model,
    content="text to embed"
)

# Text generation
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("prompt")
```

### References
- [Google AI Python SDK Documentation](https://ai.google.dev/gemini-api/docs/python-sdk)
- [Gemini API Embedding Guide](https://ai.google.dev/gemini-api/docs/embeddings)

---

## 2. Qdrant Cloud Free Tier Setup

### Decision
Use Qdrant Cloud Free Tier with Python client library for vector storage and search.

### Rationale
- **Zero Infrastructure**: Fully managed cloud service eliminates setup overhead
- **Free Tier Sufficiency**: 1GB storage + 1M vectors far exceeds project needs (~90 chunks ≈ 277KB)
- **Performance**: Optimized for sub-100ms search latency
- **Python Client**: Official `qdrant-client` package with comprehensive API
- **API Key Authentication**: Simple, secure authentication via environment variables

### Alternatives Considered
1. **Self-hosted Qdrant**
   - **Rejected**: Requires Docker/infrastructure setup; adds operational complexity
   - Not beginner-friendly per spec requirements

2. **Pinecone**
   - **Rejected**: Free tier has more restrictive limits; less generous than Qdrant
   - Commercial focus may lead to unexpected pricing changes

3. **Weaviate**
   - **Rejected**: More complex setup; GraphQL API adds learning curve

4. **ChromaDB**
   - **Rejected**: Less mature cloud offering; primarily designed for local/embedded use

### Setup Requirements
1. Create Qdrant Cloud account at [cloud.qdrant.io](https://cloud.qdrant.io)
2. Create a cluster (Free Tier)
3. Generate API key from cluster settings
4. Note cluster URL (format: `https://<cluster-id>.qdrant.io`)

### Implementation Details
```python
# Installation
pip install qdrant-client

# Connection
from qdrant_client import QdrantClient

client = QdrantClient(
    url=os.environ["QDRANT_URL"],
    api_key=os.environ["QDRANT_API_KEY"]
)

# Create collection
client.create_collection(
    collection_name="book_chunks",
    vectors_config={
        "size": 768,  # Gemini text-embedding-004 dimension
        "distance": "Cosine"
    }
)

# Search
results = client.search(
    collection_name="book_chunks",
    query_vector=query_embedding,
    limit=3
)
```

### Free Tier Limits
- Storage: 1GB
- Vectors: 1M
- Memory: Shared
- Expected Usage: ~90 chunks × 768 dimensions × 4 bytes = ~277KB (0.027% of limit)

### References
- [Qdrant Cloud Documentation](https://qdrant.tech/documentation/cloud/)
- [Qdrant Python Client](https://qdrant.tech/documentation/quickstart-python/)

---

## 3. Text Chunking Strategy

### Decision
Token-based chunking with 500-token target size and 50-token overlap (10%).

### Rationale
- **Token Accuracy**: Using `tiktoken` ensures accurate token counting for Gemini API limits
- **Context Preservation**: 50-token overlap maintains continuity across chunk boundaries
- **Retrieval Granularity**: 500 tokens (~375 words) provides focused, relevant chunks without excessive fragmentation
- **API Efficiency**: Fits well within Gemini's context limits while allowing 3-chunk retrieval

### Alternatives Considered
1. **Fixed Character Length**
   - **Rejected**: Inaccurate for token counting; can break words/sentences awkwardly

2. **Semantic Chunking** (sentence/paragraph boundaries)
   - **Rejected**: More complex; requires NLP parsing; variable chunk sizes complicate retrieval

3. **No Overlap**
   - **Rejected**: Risk of losing context at chunk boundaries; may miss relevant information

### Chunking Algorithm
1. Read markdown content
2. Strip YAML front matter (lines between `---` markers)
3. Remove code blocks (```...```) and metadata
4. Tokenize using `tiktoken` (cl100k_base encoder)
5. Create chunks:
   - Target size: 500 tokens
   - Overlap: 50 tokens
   - Slide window by 450 tokens (500 - 50)
6. Store chunk metadata (source file, chunk index, character offsets)

### Implementation Details
```python
import tiktoken

encoder = tiktoken.get_encoding("cl100k_base")  # Matches Gemini tokenization

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    tokens = encoder.encode(text)
    chunks = []

    for i in range(0, len(tokens), chunk_size - overlap):
        chunk_tokens = tokens[i:i + chunk_size]
        chunk_text = encoder.decode(chunk_tokens)
        chunks.append({
            "content": chunk_text,
            "start_token": i,
            "token_count": len(chunk_tokens)
        })

    return chunks
```

### References
- [tiktoken GitHub Repository](https://github.com/openai/tiktoken)
- [Text Chunking Best Practices](https://www.pinecone.io/learn/chunking-strategies/)

---

## 4. Embedding Model Selection

### Decision
Use Gemini `text-embedding-004` model for generating embeddings.

### Rationale
- **Latest Model**: Most recent embedding model from Google (as of 2024)
- **Optimized for Retrieval**: Specifically tuned for semantic search use cases
- **Dimension**: 768-dimensional vectors (balance between quality and storage)
- **Performance**: Competitive with state-of-the-art embedding models
- **Cost**: Free tier available via Google AI Studio

### Alternatives Considered
1. **text-embedding-001/002/003**
   - **Rejected**: Older versions; superseded by 004

2. **OpenAI text-embedding-ada-002**
   - **Rejected**: Requires OpenAI API key; project spec specifies Gemini

3. **Open-source models** (sentence-transformers)
   - **Rejected**: Requires local GPU/CPU inference; adds complexity

### Model Specifications
- **Model ID**: `models/text-embedding-004`
- **Dimension**: 768
- **Max Input Tokens**: 2048
- **Output**: Single vector per input text

### Implementation Details
```python
import google.generativeai as genai

def generate_embedding(text: str) -> list[float]:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"  # For indexing
    )
    return result['embedding']

def generate_query_embedding(query: str) -> list[float]:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=query,
        task_type="retrieval_query"  # For search
    )
    return result['embedding']
```

### References
- [Gemini Embedding Models](https://ai.google.dev/gemini-api/docs/models/gemini#text-embedding)
- [Embedding Task Types](https://ai.google.dev/gemini-api/docs/embeddings#task-types)

---

## 5. Book Content Parsing

### Decision
Read markdown files directly from `docs/` folder using Python filesystem operations and basic text processing.

### Rationale
- **Simplicity**: Direct file reading is straightforward and reliable
- **No Build Dependency**: Doesn't require building Docusaurus site
- **Filtering**: Can easily strip YAML front matter, code blocks, and MDX components
- **Flexibility**: Easy to customize parsing rules for edge cases

### Alternatives Considered
1. **Parse Built HTML**
   - **Rejected**: Requires building Docusaurus site; HTML parsing is more complex; loses semantic structure

2. **Use Markdown Parser Library** (e.g., `markdown-it-py`)
   - **Rejected**: Overkill for simple text extraction; adds unnecessary dependency

3. **MDX Parser**
   - **Rejected**: Docusaurus uses MDX, but parsing React components is complex; text extraction sufficient for RAG

### Parsing Algorithm
1. Discover markdown files: `glob.glob("docs/**/*.md", recursive=True)`
2. For each file:
   - Read full content
   - Strip YAML front matter (between `---` markers)
   - Remove code blocks (```` ```...``` ````)
   - Remove inline code (`` `...` ``)
   - Remove HTML comments (`<!-- ... -->`)
   - Extract plain text
3. Pass cleaned text to chunking function

### Implementation Details
```python
import glob
import re
from pathlib import Path

def parse_markdown_file(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove YAML front matter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

    # Remove inline code
    content = re.sub(r'`[^`]+`', '', content)

    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Remove extra whitespace
    content = re.sub(r'\n\s*\n', '\n\n', content)

    return {
        "source_file": file_path,
        "content": content.strip()
    }

def discover_book_content(docs_path: str = "../docs") -> list[dict]:
    markdown_files = glob.glob(f"{docs_path}/**/*.md", recursive=True)
    return [parse_markdown_file(f) for f in markdown_files]
```

### References
- [Python pathlib](https://docs.python.org/3/library/pathlib.html)
- [Python glob](https://docs.python.org/3/library/glob.html)

---

## 6. Error Handling Patterns

### Decision
Use FastAPI's built-in exception handling with custom exception handlers and Pydantic validation.

### Rationale
- **Centralized**: Custom exception handlers provide consistent error responses across all endpoints
- **Automatic Validation**: Pydantic models automatically validate request bodies and return 422 errors
- **Type Safety**: Pydantic ensures runtime type checking
- **Standard HTTP Status Codes**: FastAPI follows HTTP conventions (400, 422, 500)
- **Request IDs**: Easy to add middleware for request tracking

### Implementation Details
```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uuid

app = FastAPI()

# Custom exception classes
class APIError(Exception):
    def __init__(self, message: str, error_code: str, status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

# Global exception handler
@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "error_code": exc.error_code,
            "request_id": str(uuid.uuid4())
        }
    )

# Pydantic validation error handler
@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation failed",
            "error_code": "VALIDATION_ERROR",
            "request_id": str(uuid.uuid4()),
            "detail": exc.errors()
        }
    )

# Generic exception handler
@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "error_code": "SERVICE_UNAVAILABLE",
            "request_id": str(uuid.uuid4())
        }
    )
```

### Error Code Mapping
| Error Type | HTTP Status | Error Code |
|------------|-------------|------------|
| Empty question | 400 | QUESTION_EMPTY |
| Question too long | 400 | QUESTION_TOO_LONG |
| Invalid JSON | 400 | VALIDATION_ERROR |
| Gemini API failure | 500 | API_ERROR |
| Qdrant failure | 500 | SEARCH_ERROR |
| Unknown error | 500 | SERVICE_UNAVAILABLE |

### References
- [FastAPI Error Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Pydantic Validation](https://docs.pydantic.dev/latest/concepts/validators/)

---

## 7. Deployment Considerations

### Decision
Deploy to **Render** or **Railway** as a long-running Python web service (not serverless).

### Rationale
- **Persistent Connections**: Qdrant client benefits from connection pooling; not ideal for serverless cold starts
- **FastAPI Compatibility**: Both platforms natively support ASGI servers (uvicorn)
- **Free Tier Available**: Render and Railway offer free tiers sufficient for initial deployment
- **Simple Setup**: Git-based deployment with automatic builds
- **Environment Variables**: Easy configuration management via platform UI

### Alternatives Considered
1. **Vercel Serverless Functions**
   - **Rejected**: Cold start latency for Qdrant connections; 10-second timeout limit; Python support limited

2. **AWS Lambda**
   - **Rejected**: Complex setup for beginners; requires API Gateway configuration; cold starts

3. **Heroku**
   - **Rejected**: Free tier discontinued; paid tiers more expensive than alternatives

4. **Google Cloud Run**
   - **Possible**: Serverless containers with longer timeouts; more complex setup than Render/Railway

### Render Deployment Steps
1. Connect GitHub repository to Render
2. Create new Web Service
3. Configure:
   - Environment: Python 3.11
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables (GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY)
5. Deploy

### Railway Deployment Steps
1. Connect GitHub repository to Railway
2. Create new project
3. Configure:
   - Root Directory: `/backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables
5. Deploy

### Performance Considerations
- **Cold Start**: N/A (long-running service)
- **Scaling**: Both platforms support horizontal scaling (paid tiers)
- **Monitoring**: Built-in logs and metrics dashboards

### References
- [Render Python Documentation](https://render.com/docs/deploy-fastapi)
- [Railway Python Guide](https://docs.railway.app/guides/python)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)

---

## Summary of Technology Stack

| Component | Technology | Version | Rationale |
|-----------|------------|---------|-----------|
| **Language** | Python | 3.11+ | Modern features, type hints, async support |
| **Web Framework** | FastAPI | 0.109+ | Async, automatic validation, OpenAPI docs |
| **AI/LLM** | Google Gemini | 1.5-flash | Free tier, good performance, native SDK |
| **Embeddings** | Gemini text-embedding-004 | Latest | Optimized for retrieval, 768-dim vectors |
| **Vector DB** | Qdrant Cloud | Free Tier | Managed, generous limits, Python client |
| **Validation** | Pydantic | 2.5+ | Type safety, automatic validation |
| **Configuration** | Pydantic Settings | 2.1+ | Environment variable management |
| **Tokenization** | tiktoken | 0.5+ | Accurate token counting |
| **ASGI Server** | uvicorn | 0.27+ | Production-ready, supports FastAPI |
| **Deployment** | Render/Railway | N/A | Easy setup, free tier, long-running service |

---

## Next Steps

1. ✅ Research complete - all technology choices validated
2. → Proceed to Phase 1: Generate data-model.md
3. → Proceed to Phase 1: Generate contracts/openapi.yaml
4. → Proceed to Phase 1: Generate quickstart.md
5. → Update agent context with new technologies
6. → Generate tasks.md via `/sp.tasks` command
