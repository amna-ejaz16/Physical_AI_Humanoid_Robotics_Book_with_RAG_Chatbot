# Implementation Plan: RAG Chatbot Backend

**Branch**: `002-rag-chatbot-backend` | **Date**: 2025-12-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-rag-chatbot-backend/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a Retrieval-Augmented Generation (RAG) chatbot backend for the Physical AI & Humanoid Robotics book. The system will enable readers to ask questions about book content and receive accurate, contextual answers generated from retrieved text chunks. The backend will be completely isolated in a `/backend` folder, using FastAPI for the API layer, Gemini API via OpenAI Agents SDK for embeddings and text generation, and Qdrant Free Tier for vector storage. The implementation prioritizes modularity, beginner-friendly setup, and production-ready error handling while maintaining complete independence from the existing Docusaurus frontend.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.109+, OpenAI Agents SDK (openai-agents 1.0+), Qdrant Client 1.7+, Pydantic 2.5+, Pydantic Settings 2.1+, python-dotenv 1.0+, tiktoken 0.5+ (token counting), uvicorn 0.27+ (ASGI server)
**Storage**: Qdrant Cloud Free Tier (vector database for embeddings), filesystem (for book content markdown files)
**Testing**: Manual API testing via curl/Postman/httpie (automated testing out of scope per spec)
**Target Platform**: Linux/macOS/Windows development environment; Cloud deployment (Vercel, Render, Railway, or similar Python-supporting platforms)
**Project Type**: Web backend (API service) - isolated `/backend` folder
**Performance Goals**: <5 seconds response time for 95% of queries; support 100 concurrent requests without degradation
**Constraints**: Must not modify existing Docusaurus frontend; Gemini API rate limits (requests per minute); Qdrant Free Tier limits (1GB storage, 1M vectors); 500-token chunk size for embeddings
**Scale/Scope**: Single book content (estimated 25,000-45,000 words = 50-90 chunks @ 500 tokens each); Expected query volume: <1000 queries/day initially

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Alignment with Project Constitution

**✅ Technical Accuracy**: RAG architecture is industry-standard for Q&A systems over document collections. Gemini API and Qdrant are proven technologies with documented APIs.

**✅ Engineering Clarity**: Implementation plan targets beginner-friendly setup with step-by-step instructions, modular code structure, and clear separation of concerns.

**✅ Modular Documentation**: Backend is completely isolated in `/backend` folder. README.md, .env.example, and quickstart.md will provide comprehensive setup and usage documentation.

**✅ Reproducibility & Transparency**: All dependencies will be pinned in requirements.txt. Configuration will be explicit via .env. API contracts will be documented via OpenAPI (FastAPI auto-generates this).

**✅ Safety & Ethics Awareness**: RAG ensures responses are grounded in book content, reducing hallucination risk. Error handling prevents crashes and provides clear feedback.

**✅ Consistency with Spec-Kit Plus**: This plan follows SDD methodology: spec → plan → tasks → implementation. All phases are structured and verifiable.

### Constitution Gates: PASS ✅

- **No conflicts** with existing content structure (backend is isolated)
- **Traceable to credible sources**: FastAPI, OpenAI SDK, Qdrant, and Gemini API are all well-documented
- **Modular and maintainable**: Clear file separation (main.py, agent_client.py, rag_client.py, config.py, models.py)
- **Deployable**: Follows standard Python web service patterns compatible with modern cloud platforms

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-chatbot-backend/
├── spec.md              # Feature requirements (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output: Technology choices and patterns
├── data-model.md        # Phase 1 output: Entity definitions and relationships
├── quickstart.md        # Phase 1 output: Developer setup and usage guide
├── contracts/           # Phase 1 output: API contracts
│   └── openapi.yaml     # OpenAPI 3.0 specification for /ask endpoint
├── checklists/          # Quality validation
│   └── requirements.md  # Spec validation (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/                     # Isolated backend folder (does not touch Docusaurus)
├── main.py                  # FastAPI application entry point, /ask endpoint
├── agent_client.py          # Gemini API integration via OpenAI Agents SDK
├── rag_client.py            # RAG logic: embeddings, Qdrant, retrieval
├── config.py                # Configuration management (Pydantic BaseSettings)
├── models.py                # Pydantic models: ChatRequest, ChatResponse, ErrorResponse
├── indexer.py               # Script to index book content into Qdrant
├── requirements.txt         # Python dependencies (pinned versions)
├── .env.example             # Template for environment variables
├── .env                     # Actual environment variables (gitignored)
├── .gitignore               # Ignore .env, __pycache__, .venv
└── README.md                # Setup, run, test, and deployment instructions

.venv/                       # Virtual environment (gitignored)

docs/                        # Existing Docusaurus book (NOT MODIFIED)
├── chapters/
├── diagrams/
└── ...

(root files: package.json, docusaurus.config.js, etc. remain untouched)
```

**Structure Decision**: Selected **Web backend (API service)** pattern since this is a standalone FastAPI backend that will serve the Docusaurus frontend via API calls. The `/backend` folder is completely isolated from the existing Docusaurus site, ensuring no conflicts or modifications to the book content structure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All choices align with project constitution and industry best practices for RAG systems.

---

## Phase 0: Research & Technology Validation

### Research Questions to Resolve

1. **Gemini API + OpenAI Agents SDK Integration**: How to configure OpenAI Agents SDK to use Gemini API instead of OpenAI API?
2. **Qdrant Free Tier Setup**: What are the authentication methods, connection parameters, and limits for Qdrant Cloud Free Tier?
3. **Text Chunking Strategy**: What overlap percentage and chunking method (character-based, token-based, semantic) works best for 500-token chunks?
4. **Embedding Model Selection**: Which Gemini embedding model (e.g., `models/embedding-001`) is optimal for semantic search?
5. **Book Content Parsing**: How to read and parse Docusaurus markdown files (front matter, MDX components, code blocks)?
6. **Error Handling Patterns**: Best practices for FastAPI error handling with Pydantic validation and external API failures?
7. **Deployment Considerations**: How to deploy FastAPI with Qdrant client to Vercel/Render/Railway (serverless vs. long-running process)?

### Research Output: research.md

**To be generated in Phase 0** - This file will document:

- **Decision**: Gemini API integration approach via OpenAI SDK
  - **Rationale**: Use `openai` Python package with custom `base_url` and `api_key` configuration
  - **Alternatives**: Direct Google AI Python SDK (less compatible with existing patterns)

- **Decision**: Qdrant Cloud authentication and connection
  - **Rationale**: API key authentication via environment variables; gRPC or HTTP client
  - **Alternatives**: Self-hosted Qdrant (requires infrastructure)

- **Decision**: Chunking strategy - token-based with 50-token overlap
  - **Rationale**: Maintains context at chunk boundaries; uses tiktoken for accurate token counting
  - **Alternatives**: Fixed character length (less precise), semantic chunking (more complex)

- **Decision**: Embedding model - Gemini `text-embedding-004` (or latest available)
  - **Rationale**: Optimized for retrieval tasks; 768-dimensional vectors
  - **Alternatives**: Older embedding models with different dimensions

- **Decision**: Book content parsing - read markdown files directly from `docs/` folder
  - **Rationale**: Simple filesystem access; filter out front matter and code blocks for cleaner chunks
  - **Alternatives**: Parse built HTML (adds complexity)

- **Decision**: Error handling - FastAPI exception handlers with Pydantic validation
  - **Rationale**: Centralized error responses; consistent JSON error format
  - **Alternatives**: Try-except blocks in each endpoint (duplicated logic)

- **Decision**: Deployment - long-running server on Render/Railway
  - **Rationale**: FastAPI + Qdrant client requires persistent connections; not ideal for serverless cold starts
  - **Alternatives**: Vercel serverless (requires connection pooling and cold start optimization)

---

## Phase 1: Data Model & API Contracts

### Entities & Data Model (data-model.md)

**To be generated in Phase 1** - Key entities:

#### 1. TextChunk
**Purpose**: Represents a segment of book content for vector search

**Fields**:
- `id`: Unique identifier (UUID or sequential integer)
- `content`: Raw text content (string, ~500 tokens)
- `embedding`: Vector representation (list of floats, dimension = embedding model dimension)
- `metadata`: Additional information
  - `source_file`: Path to original markdown file (e.g., "docs/chapters/01-introduction.md")
  - `chunk_index`: Position within source file (integer)
  - `start_char`: Character offset in source file (integer)
  - `end_char`: Character offset in source file (integer)
  - `token_count`: Number of tokens in content (integer)

**Relationships**: None (flat structure in Qdrant)

**State Transitions**: Created during indexing → Retrieved during search → Immutable

---

#### 2. ChatRequest
**Purpose**: User input for the `/ask` endpoint

**Fields**:
- `question`: User's question (string, 1-4000 characters, non-empty)

**Validation Rules**:
- Must be a string (Pydantic type validation)
- Length: 1 ≤ len(question) ≤ 4000 characters
- Must not be empty or whitespace-only (strip and check length)

**Example**:
```json
{
  "question": "What is reinforcement learning in robotics?"
}
```

---

#### 3. ChatResponse
**Purpose**: Successful response from the `/ask` endpoint

**Fields**:
- `answer`: Generated answer based on retrieved book content (string)
- `request_id`: Unique identifier for this request (UUID string)
- `sources`: Optional list of source file paths used (list of strings) - for transparency

**Example**:
```json
{
  "answer": "Reinforcement learning in robotics is...",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "sources": ["docs/chapters/05-reinforcement-learning.md"]
}
```

---

#### 4. ErrorResponse
**Purpose**: Error response from any endpoint

**Fields**:
- `error`: Human-readable error message (string)
- `error_code`: Machine-readable error code (string, e.g., "VALIDATION_ERROR", "API_ERROR", "SERVICE_UNAVAILABLE")
- `request_id`: Unique identifier for this request (UUID string)
- `detail`: Optional additional error details (string or dict, optional)

**Error Codes**:
- `VALIDATION_ERROR`: Invalid input (HTTP 400)
- `QUESTION_EMPTY`: Empty question string (HTTP 400)
- `QUESTION_TOO_LONG`: Question exceeds 4000 characters (HTTP 400)
- `API_ERROR`: Gemini API failure (HTTP 500)
- `SEARCH_ERROR`: Qdrant search failure (HTTP 500)
- `SERVICE_UNAVAILABLE`: General server error (HTTP 500)

**Example**:
```json
{
  "error": "Question cannot be empty",
  "error_code": "QUESTION_EMPTY",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

---

#### 5. Configuration (config.py entities)
**Purpose**: Environment-based settings for the application

**AgentConfig**:
- `gemini_api_key`: Gemini API key (string, required, from env var `GEMINI_API_KEY`)
- `model_name`: Gemini model for text generation (string, default "gemini-1.5-flash", from env var `GEMINI_MODEL`)
- `embedding_model`: Gemini embedding model (string, default "text-embedding-004", from env var `GEMINI_EMBEDDING_MODEL`)
- `base_url`: API base URL for Gemini (string, default "https://generativelanguage.googleapis.com/v1beta", from env var `GEMINI_BASE_URL`)

**QdrantConfig**:
- `url`: Qdrant Cloud URL (string, required, from env var `QDRANT_URL`)
- `api_key`: Qdrant API key (string, required, from env var `QDRANT_API_KEY`)
- `collection_name`: Qdrant collection name (string, default "book_chunks", from env var `QDRANT_COLLECTION`)

**ServerConfig**:
- `host`: Server host (string, default "0.0.0.0", from env var `SERVER_HOST`)
- `port`: Server port (integer, default 8000, from env var `SERVER_PORT`)
- `debug`: Debug mode (boolean, default False, from env var `DEBUG`)

**RAGConfig**:
- `chunk_size`: Target token count per chunk (integer, default 500, from env var `CHUNK_SIZE`)
- `chunk_overlap`: Overlap tokens between chunks (integer, default 50, from env var `CHUNK_OVERLAP`)
- `top_k`: Number of chunks to retrieve (integer, default 3, from env var `TOP_K`)
- `book_content_path`: Path to book markdown files (string, default "../docs", from env var `BOOK_CONTENT_PATH`)

---

### API Contracts (contracts/openapi.yaml)

**To be generated in Phase 1** - OpenAPI 3.0 specification:

#### Endpoint: POST /ask

**Request**:
- **Content-Type**: application/json
- **Body**: ChatRequest schema

**Responses**:
- **200 OK**: ChatResponse schema
- **400 Bad Request**: ErrorResponse schema (validation errors)
- **500 Internal Server Error**: ErrorResponse schema (API/service errors)

**Example Request**:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain reinforcement learning in robotics from this book."}'
```

**Example Success Response (200)**:
```json
{
  "answer": "Reinforcement learning in robotics involves agents learning optimal behaviors through trial and error. The book discusses how robots use reward signals to improve task performance, with applications in navigation, manipulation, and human-robot interaction.",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "sources": ["docs/chapters/05-reinforcement-learning.md", "docs/chapters/08-learning-algorithms.md"]
}
```

**Example Error Response (400)**:
```json
{
  "error": "Question cannot be empty",
  "error_code": "QUESTION_EMPTY",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Example Error Response (500)**:
```json
{
  "error": "Gemini API request failed",
  "error_code": "API_ERROR",
  "request_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "detail": "Rate limit exceeded. Please try again later."
}
```

---

#### Endpoint: GET /health (Bonus - for deployment monitoring)

**Request**: None

**Responses**:
- **200 OK**: `{"status": "healthy", "qdrant_connected": true}`
- **503 Service Unavailable**: `{"status": "unhealthy", "qdrant_connected": false}`

---

### Quickstart Guide (quickstart.md)

**To be generated in Phase 1** - Developer setup instructions:

1. **Prerequisites**
   - Python 3.11+
   - Gemini API key (from Google AI Studio)
   - Qdrant Cloud account (Free Tier)

2. **Setup Steps**
   - Clone repository
   - Navigate to `/backend` folder
   - Create virtual environment: `uv venv` or `python -m venv .venv`
   - Activate virtual environment
   - Install dependencies: `pip install -r requirements.txt`
   - Copy `.env.example` to `.env` and fill in API keys
   - Run indexer: `python indexer.py` (one-time setup to index book content)
   - Run server: `uvicorn main:app --reload`

3. **Testing the API**
   - Example curl command
   - Example Postman collection
   - Expected responses

4. **Deployment**
   - Render deployment instructions
   - Environment variable configuration
   - Health check endpoint setup

---

## Phase 2: Task Breakdown

**NOT INCLUDED IN THIS PLAN** - Will be generated by `/sp.tasks` command.

The tasks.md file will break down the implementation into concrete, testable tasks based on the user stories and functional requirements defined in spec.md, using the architecture and contracts defined in this plan.

---

## Architectural Decision Records (ADRs)

### Significant Decisions Requiring Documentation

Based on the three-part test (Impact + Alternatives + Scope):

#### 1. Gemini API via OpenAI Agents SDK
- **Impact**: Long-term dependency on SDK compatibility; affects all AI interactions
- **Alternatives**: Direct Google AI SDK, custom HTTP client, LangChain
- **Scope**: Cross-cutting (affects embedding, text generation, error handling)

📋 **Architectural decision detected**: Using OpenAI Agents SDK with Gemini API instead of native Google AI SDK - Document reasoning and tradeoffs? Run `/sp.adr "Gemini API Integration via OpenAI SDK"`

#### 2. Qdrant Cloud Free Tier for Vector Storage
- **Impact**: Long-term dependency on cloud service; affects scalability and cost
- **Alternatives**: Self-hosted Qdrant, Pinecone, Weaviate, ChromaDB
- **Scope**: Cross-cutting (affects indexing, retrieval, deployment)

📋 **Architectural decision detected**: Using Qdrant Cloud Free Tier for vector storage instead of self-hosted or alternative vector databases - Document reasoning and tradeoffs? Run `/sp.adr "Qdrant Cloud for Vector Storage"`

#### 3. Backend Isolation Strategy
- **Impact**: Long-term deployment model; affects frontend-backend integration
- **Alternatives**: Integrated Docusaurus plugin, static site generation with embeddings, serverless functions
- **Scope**: System design (affects deployment, API contracts, CORS)

📋 **Architectural decision detected**: Complete backend isolation in /backend folder instead of Docusaurus integration - Document reasoning and tradeoffs? Run `/sp.adr "Isolated Backend Architecture"`

---

## Next Steps

1. **Complete Phase 0**: Generate `research.md` with detailed technology validation
2. **Complete Phase 1**: Generate `data-model.md`, `contracts/openapi.yaml`, and `quickstart.md`
3. **Update Agent Context**: Run `.specify/scripts/bash/update-agent-context.sh claude` to add FastAPI, Qdrant, and Gemini API to project context
4. **Re-evaluate Constitution Check**: Verify all design decisions align with project principles
5. **Generate ADRs** (optional but recommended): Document the three significant architectural decisions
6. **Proceed to `/sp.tasks`**: Create task breakdown for implementation

---

## Implementation Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Gemini API rate limits during indexing | High: Cannot index book content | Implement exponential backoff; batch requests; use caching |
| Qdrant Free Tier storage limits (1GB) | Medium: Cannot store all embeddings | Estimate: 90 chunks × 768 dims × 4 bytes = ~277KB (well within limit) |
| OpenAI SDK + Gemini compatibility issues | High: Core functionality broken | Validate with small proof-of-concept before full implementation |
| Cold start latency in serverless deployment | Medium: Poor user experience | Deploy to long-running server (Render/Railway) instead of serverless |
| Book content format inconsistencies | Low: Indexing errors | Robust markdown parsing with error handling; skip unparseable content |
| Concurrent request handling | Low: Performance degradation | FastAPI handles this natively; test with load testing tools |

---

## Performance & Scalability Considerations

**Expected Load**:
- Initial: <1000 queries/day (~0.01 QPS)
- Peak: 100 concurrent requests (per SC-007)

**Bottlenecks**:
1. Gemini API latency (network + inference time)
2. Qdrant vector search (optimized for <100ms)
3. Token counting overhead (tiktoken is fast but not instant)

**Optimizations** (if needed in future):
- Cache frequent questions (Redis/in-memory)
- Pre-compute embeddings for common queries
- Implement request queuing for rate limit management
- Add CDN/caching layer for static responses

---

## Security Considerations

**Secrets Management**:
- All API keys in `.env` file (gitignored)
- Never log or expose keys in error messages
- Use environment variables in deployment

**Input Validation**:
- Pydantic validates all inputs
- Question length limited to 4000 characters (prevent abuse)
- No SQL injection risk (vector DB, not SQL)

**CORS**:
- Configure for Docusaurus frontend domain
- Restrict in production (not open to all origins)

**Rate Limiting** (out of scope for MVP, but future consideration):
- Client-side: User-based quotas
- Server-side: IP-based rate limiting

---

## Monitoring & Observability

**Logging**:
- Request IDs for traceability
- Error logs with context (no sensitive data)
- Performance metrics (response time per request)

**Health Checks**:
- `/health` endpoint for deployment monitoring
- Qdrant connection status
- Gemini API reachability (optional)

**Metrics** (future):
- Query volume
- Average response time
- Error rate by type
- Top queries (for optimization)

---

## Deployment Checklist

- [ ] Environment variables configured in deployment platform
- [ ] Book content indexed into Qdrant (run `indexer.py`)
- [ ] Health check endpoint responding
- [ ] CORS configured for frontend domain
- [ ] Error logging enabled
- [ ] API documentation accessible (FastAPI auto-generates at `/docs`)
- [ ] README.md deployment section verified

---

**Plan Status**: Phase 0 and Phase 1 ready to execute
**Ready for**: `/sp.tasks` command to generate task breakdown
