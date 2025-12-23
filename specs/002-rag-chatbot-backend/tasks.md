# Implementation Tasks: RAG Chatbot Backend

**Feature**: RAG Chatbot Backend
**Branch**: `002-rag-chatbot-backend`
**Created**: 2025-12-09
**Status**: Ready for Implementation

## Overview

This document provides a complete, actionable task breakdown for implementing the RAG chatbot backend. Tasks are organized by user story to enable independent implementation and testing of each feature increment.

**User Stories** (from spec.md):
- **US1** (P1): Basic Question Answering - Core RAG functionality
- **US2** (P2): Input Validation and Error Handling
- **US3** (P1): Book Content Indexing
- **US4** (P2): System Configuration and Environment Setup

**Implementation Strategy**: MVP-first approach focusing on P1 stories (US1 + US3) for immediate value delivery.

---

## Task Format Legend

```
- [ ] T### [P] [US#] Task description in file/path
```

- **T###**: Sequential task ID
- **[P]**: Parallelizable (can be done concurrently with other [P] tasks)
- **[US#]**: User story label (US1, US2, US3, US4)
- **Description**: Clear action with file path

---

## Phase 1: Project Setup & Infrastructure

**Goal**: Initialize backend project structure and install foundational dependencies

**Tasks**:

- [ ] T001 Create `/backend` directory at repository root
- [ ] T002 Create `.gitignore` in `/backend` with entries: `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `*.egg-info/`
- [ ] T003 Create `requirements.txt` in `/backend` with pinned dependencies: `fastapi==0.109.0`, `uvicorn[standard]==0.27.0`, `google-generativeai==0.3.0`, `qdrant-client==1.7.0`, `pydantic==2.5.0`, `pydantic-settings==2.1.0`, `python-dotenv==1.0.0`, `tiktoken==0.5.2`
- [ ] T004 Create Python virtual environment: `cd backend && python -m venv .venv`
- [ ] T005 Install dependencies: `source .venv/bin/activate && pip install -r requirements.txt`

**Acceptance Criteria**:
- `/backend` directory exists with `.gitignore` and `requirements.txt`
- Virtual environment created and dependencies installed successfully
- Can run `python --version` and see Python 3.11+

---

## Phase 2: Configuration Management (US4)

**User Story**: System Configuration and Environment Setup (Priority: P2)

**Goal**: Enable secure, environment-based configuration without hardcoded secrets

**Independent Test**: Provide `.env` file with valid values → backend loads configuration successfully → missing values cause clear error messages

**Tasks**:

- [ ] T006 [US4] Create `.env.example` in `/backend` with template: `GEMINI_API_KEY=your_gemini_key_here`, `GEMINI_MODEL=gemini-1.5-flash`, `GEMINI_EMBEDDING_MODEL=models/text-embedding-004`, `QDRANT_URL=https://your-cluster.qdrant.io`, `QDRANT_API_KEY=your_qdrant_key_here`, `QDRANT_COLLECTION=book_chunks`, `SERVER_HOST=0.0.0.0`, `SERVER_PORT=8000`, `SERVER_DEBUG=False`, `RAG_CHUNK_SIZE=500`, `RAG_CHUNK_OVERLAP=50`, `RAG_TOP_K=3`, `RAG_BOOK_CONTENT_PATH=../docs`
- [ ] T007 [P] [US4] Create `config.py` in `/backend` with `AgentConfig` class using Pydantic BaseSettings: fields `gemini_api_key` (required), `model_name` (default "gemini-1.5-flash"), `embedding_model` (default "models/text-embedding-004"), env_prefix "GEMINI_"
- [ ] T008 [P] [US4] Add `QdrantConfig` class to `config.py`: fields `url` (required), `api_key` (required), `collection_name` (default "book_chunks"), env_prefix "QDRANT_"
- [ ] T009 [P] [US4] Add `ServerConfig` class to `config.py`: fields `host` (default "0.0.0.0"), `port` (default 8000), `debug` (default False), env_prefix "SERVER_"
- [ ] T010 [P] [US4] Add `RAGConfig` class to `config.py`: fields `chunk_size` (default 500, range 100-1000), `chunk_overlap` (default 50, range 0-200), `top_k` (default 3, range 1-10), `book_content_path` (default "../docs"), env_prefix "RAG_"
- [ ] T011 [US4] Create main config loader function `load_config()` in `config.py` that returns all four config objects and validates required fields are present

**Acceptance Criteria**:
- `.env.example` provides clear template for all required configuration
- All four Pydantic Settings classes load from environment variables
- Missing required env vars (GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY) cause validation errors with clear messages
- Config can be loaded via `from config import load_config; config = load_config()`

---

## Phase 3: Data Models (Foundational)

**Goal**: Define Pydantic models for API request/response and error handling (used by multiple user stories)

**Tasks**:

- [ ] T012 [P] Create `models.py` in `/backend` with `ChatRequest` model: field `question` (str, min_length=1, max_length=4000), custom validator to reject whitespace-only strings
- [ ] T013 [P] Add `ChatResponse` model to `models.py`: fields `answer` (str), `request_id` (UUID, auto-generated), `sources` (Optional[List[str]])
- [ ] T014 [P] Add `ErrorResponse` model to `models.py`: fields `error` (str), `error_code` (str), `request_id` (UUID, auto-generated), `detail` (Optional[Union[str, Dict[str, Any]]])
- [ ] T015 [P] Add error code constants to `models.py`: `VALIDATION_ERROR`, `QUESTION_EMPTY`, `QUESTION_TOO_LONG`, `API_ERROR`, `EMBEDDING_ERROR`, `SEARCH_ERROR`, `SERVICE_UNAVAILABLE`

**Acceptance Criteria**:
- All Pydantic models defined with correct field types and validation rules
- ChatRequest rejects empty/whitespace-only questions
- ChatResponse and ErrorResponse generate UUIDs automatically
- Error codes available as module-level constants

---

## Phase 4: Book Content Indexing (US3 - P1)

**User Story**: Book Content Indexing (Priority: P1)

**Goal**: Ingest Docusaurus book content, chunk text, generate embeddings, and store in Qdrant

**Independent Test**: Run indexer script → book content split into ~500-token chunks → embeddings generated via Gemini → stored in Qdrant → test retrieval succeeds

**Tasks**:

- [ ] T016 [US3] Create `rag_client.py` in `/backend` with `QdrantManager` class: initialize Qdrant client using QdrantConfig, method `create_collection()` to create collection with 768-dim vectors and Cosine distance
- [ ] T017 [P] [US3] Add `TextChunker` class to `rag_client.py`: method `chunk_text(text, chunk_size, overlap)` using tiktoken (cl100k_base encoder) to split text into token-based chunks with specified overlap
- [ ] T018 [P] [US3] Add `MarkdownParser` class to `rag_client.py`: method `parse_markdown(file_path)` to read markdown, strip YAML front matter (between `---` markers), remove code blocks (```...```), return cleaned text and source path
- [ ] T019 [P] [US3] Create `agent_client.py` in `/backend` with `GeminiClient` class: initialize with AgentConfig, method `generate_embedding(text)` using `google.generativeai.embed_content()` with model "models/text-embedding-004" and task_type "retrieval_document"
- [ ] T020 [US3] Add `discover_markdown_files(docs_path)` function to `rag_client.py` using `glob.glob()` to recursively find all `*.md` files in docs folder
- [ ] T021 [US3] Create `indexer.py` in `/backend` as executable script: parse command-line args (`--force` flag to recreate collection), load configs, discover markdown files, parse each file, chunk text, generate embeddings, upload to Qdrant with metadata (source_file, chunk_index, start_char, end_char, token_count)
- [ ] T022 [US3] Add progress logging to `indexer.py`: print "Processing: {file}" for each file, "Created {n} chunks" after chunking, "Total chunks: {total}", "Uploading to Qdrant...", "Successfully indexed {count} chunks"
- [ ] T023 [US3] Add error handling to `indexer.py`: catch Gemini API errors (rate limits, auth failures), Qdrant errors (connection, upload), file parsing errors, continue processing other files on individual failures, log errors clearly

**Acceptance Criteria**:
- `indexer.py` can be run as: `python indexer.py` (or `python indexer.py --force` to recreate collection)
- Book markdown files discovered and parsed (YAML front matter and code blocks removed)
- Text split into ~500-token chunks with 50-token overlap
- Each chunk generates 768-dim embedding via Gemini API
- All chunks stored in Qdrant with complete metadata
- Progress logged for each file processed
- Errors handled gracefully without stopping entire indexing process
- Final summary shows total chunks indexed

---

## Phase 5: RAG Retrieval & Answer Generation (US1 - P1)

**User Story**: Basic Question Answering (Priority: P1)

**Goal**: Accept user questions, retrieve relevant book chunks, generate AI answers

**Independent Test**: POST to `/ask` with question → system retrieves top 3 chunks from Qdrant → generates answer using Gemini → returns JSON with answer and sources within 5 seconds

**Tasks**:

- [ ] T024 [US1] Add `search(query_text, top_k)` method to `QdrantManager` in `rag_client.py`: generate query embedding (task_type "retrieval_query"), search Qdrant collection, return list of TextChunk results with scores
- [ ] T025 [P] [US1] Add `generate_answer(question, context_chunks)` method to `GeminiClient` in `agent_client.py`: combine chunks into context string, create prompt "Based on the following book content, answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:", call Gemini generate_content(), return answer text
- [ ] T026 [US1] Create `RAGPipeline` class in `rag_client.py`: initialize with GeminiClient and QdrantManager, method `ask(question)` that (1) searches Qdrant for top_k chunks, (2) generates answer using GeminiClient, (3) returns answer + source files
- [ ] T027 [US1] Create `main.py` in `/backend` with FastAPI app initialization: import FastAPI, create app instance, load configs on startup, initialize RAGPipeline, add CORS middleware (allow all origins for development)
- [ ] T028 [US1] Add POST `/ask` endpoint to `main.py`: accept ChatRequest body, call RAGPipeline.ask(), return ChatResponse with answer and sources, handle errors and return ErrorResponse
- [ ] T029 [US1] Add GET `/health` endpoint to `main.py`: check Qdrant connection, check Gemini API availability (optional), return `{"status": "healthy", "qdrant_connected": true}` or 503 if unhealthy

**Acceptance Criteria**:
- RAGPipeline successfully retrieves top 3 relevant chunks for a query
- Gemini generates coherent answer based on retrieved chunks
- POST `/ask` endpoint returns JSON with answer and source file paths
- GET `/health` endpoint returns 200 when services are healthy
- Response time under 5 seconds for typical queries
- Answers synthesize information from multiple chunks (not verbatim copy)

---

## Phase 6: Error Handling & Validation (US2 - P2)

**User Story**: Input Validation and Error Handling (Priority: P2)

**Goal**: Validate inputs, handle errors gracefully, return actionable error messages

**Independent Test**: Send invalid requests (empty question, non-string, very long) → receive HTTP 400 with clear error codes → simulate service failures → receive HTTP 500 with error details

**Tasks**:

- [ ] T030 [US2] Create custom exception classes in `main.py`: `APIError(message, error_code, status_code)`, `EmbeddingError`, `SearchError`, `ServiceUnavailableError`
- [ ] T031 [P] [US2] Add global exception handler for `APIError` in `main.py`: return ErrorResponse JSON with appropriate HTTP status code
- [ ] T032 [P] [US2] Add exception handler for `RequestValidationError` (Pydantic) in `main.py`: return ErrorResponse with error_code "VALIDATION_ERROR", HTTP 400, include validation details in `detail` field
- [ ] T033 [P] [US2] Add generic exception handler for `Exception` in `main.py`: return ErrorResponse with error_code "SERVICE_UNAVAILABLE", HTTP 500, log full exception for debugging
- [ ] T034 [US2] Add input validation middleware to POST `/ask` endpoint: check question length (reject if > 4000 chars with "QUESTION_TOO_LONG"), check if whitespace-only (reject with "QUESTION_EMPTY"), strip whitespace before processing
- [ ] T035 [US2] Add error handling to `RAGPipeline.ask()` in `rag_client.py`: wrap Qdrant search in try-except, raise `SearchError` on failure; wrap Gemini API call in try-except, raise `APIError` on failure with rate limit detection
- [ ] T036 [US2] Add request ID generation middleware to `main.py`: generate UUID for each request, include in all ErrorResponse instances, log request ID with errors for tracing

**Acceptance Criteria**:
- Empty question returns HTTP 400 with error_code "QUESTION_EMPTY"
- Question > 4000 chars returns HTTP 400 with error_code "QUESTION_TOO_LONG"
- Invalid JSON returns HTTP 400 with error_code "VALIDATION_ERROR" and Pydantic validation details
- Qdrant connection failure returns HTTP 500 with error_code "SEARCH_ERROR"
- Gemini API failure returns HTTP 500 with error_code "API_ERROR" (rate limit info if applicable)
- All errors include request_id for tracing
- Generic exceptions return HTTP 500 without exposing internal details

---

## Phase 7: Documentation & Testing

**Goal**: Provide comprehensive setup instructions and example usage

**Tasks**:

- [ ] T037 [P] Create `README.md` in `/backend` with sections: Overview, Prerequisites (Python 3.11+, API keys), Setup Instructions (7 steps with commands), Testing (4 methods: curl, browser /docs, Python requests, Postman), Deployment (Render + Railway instructions), Troubleshooting (5 common issues)
- [ ] T038 [P] Add "Example Requests" section to `README.md`: 4 example curl commands testing simple question, detailed question, empty question (error), very long question (error)
- [ ] T039 [P] Add "Environment Variables Reference" table to `README.md`: all env vars from `.env.example` with descriptions and defaults
- [ ] T040 [P] Add "API Endpoints" section to `README.md`: document POST `/ask` (request/response schemas, status codes, error codes), GET `/health` (response schema)
- [ ] T041 Add deployment checklist to `README.md`: environment variables configured, book content indexed via `python indexer.py`, health check responding, API accessible

**Acceptance Criteria**:
- README.md provides complete setup instructions (15-minute target for new developers)
- All example commands are copy-paste ready and work
- Environment variables clearly documented with defaults
- API endpoints documented with request/response examples
- Deployment checklist helps verify production readiness

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Production readiness, logging, performance optimization

**Tasks**:

- [ ] T042 [P] Add structured logging to `main.py`: configure Python logging with INFO level, log startup message with loaded configs (without secrets), log each request to `/ask` with question length and response time
- [ ] T043 [P] Add startup validation to `main.py`: on app startup, check required env vars are set, test Qdrant connection, log "Backend ready" or fail fast with clear error
- [ ] T044 [P] Add rate limit handling to `agent_client.py`: detect Gemini API rate limit errors (status 429), implement exponential backoff with max 3 retries, return clear error message to user if all retries fail
- [ ] T045 [P] Add connection pooling to `rag_client.py`: configure Qdrant client with keep-alive connections, set reasonable timeout (10 seconds)
- [ ] T046 Optimize chunking performance in `rag_client.py`: cache tiktoken encoder (don't reload for each chunk), batch process markdown files (process 5 at a time)
- [ ] T047 Add `.env` to `.gitignore` (if not already present) and verify no secrets committed to git
- [ ] T048 Create deployment configuration files: create `Procfile` for Render (`web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`), create `render.yaml` with build/start commands and env var placeholders
- [ ] T049 Test full RAG pipeline end-to-end: index sample book content, start server, send 10 varied questions via curl, verify responses are relevant and fast (<5s), check logs for errors

**Acceptance Criteria**:
- All requests logged with timing information
- Startup checks validate configuration and connectivity
- Gemini API rate limits handled with retries and clear errors
- Qdrant connections optimized for performance
- No secrets in git repository
- Deployment files ready for Render/Railway
- End-to-end testing confirms system works as specified

---

## Task Dependencies & Execution Order

### User Story Dependency Graph

```
Setup (Phase 1)
    ↓
Configuration (US4 - Phase 2) → Data Models (Phase 3)
    ↓                                    ↓
Book Indexing (US3 - Phase 4) ─────────→ RAG Q&A (US1 - Phase 5)
                                           ↓
                                Error Handling (US2 - Phase 6)
                                           ↓
                                Documentation (Phase 7)
                                           ↓
                                Polish (Phase 8)
```

**Critical Path**: Setup → Config → Indexing → Q&A → Polish

**MVP Scope** (Minimum Viable Product):
- Phase 1: Setup
- Phase 2: Configuration (US4)
- Phase 3: Data Models
- Phase 4: Book Indexing (US3)
- Phase 5: RAG Q&A (US1)
- Phase 7: Basic README

This delivers the core value: users can ask questions and get AI-generated answers from book content.

**Phase 6 (Error Handling) and Phase 8 (Polish)** can be added incrementally after MVP is working.

---

## Parallel Execution Opportunities

Tasks marked with **[P]** can be executed in parallel within their phase:

**Phase 2 (Configuration)**:
- T007, T008, T009, T010 (all config classes) can be written in parallel

**Phase 3 (Data Models)**:
- T012, T013, T014, T015 (all Pydantic models) can be written in parallel

**Phase 4 (Indexing)**:
- T017, T018, T019 (chunker, parser, agent client) can be developed in parallel after T016

**Phase 5 (RAG Q&A)**:
- T025 (generate answer) can be developed in parallel with T024 (search)

**Phase 6 (Error Handling)**:
- T031, T032, T033 (exception handlers) can be added in parallel

**Phase 7 (Documentation)**:
- T037, T038, T039, T040 (README sections) can be written in parallel

**Phase 8 (Polish)**:
- T042, T043, T044, T045 (logging, validation, rate limits, pooling) can be implemented in parallel

---

## Testing Strategy

**Per User Story Independent Testing**:

**US1 (Basic Q&A)**:
```bash
# Start server
cd backend && uvicorn main:app --reload

# Test question answering
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is physical AI?"}'

# Verify: Response contains answer + sources, response time < 5s
```

**US2 (Error Handling)**:
```bash
# Test empty question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": ""}'

# Verify: HTTP 400, error_code "QUESTION_EMPTY"

# Test too long question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"$(python -c 'print(\"a\" * 5000)')\"}"

# Verify: HTTP 400, error_code "QUESTION_TOO_LONG"
```

**US3 (Indexing)**:
```bash
# Run indexer
cd backend && python indexer.py

# Verify: Logs show files processed, chunks created, Qdrant upload success
# Verify: Can query Qdrant and retrieve chunks

# Test retrieval
python -c "
from rag_client import QdrantManager
from config import load_config
config = load_config()
qm = QdrantManager(config.qdrant)
results = qm.search('test query', top_k=3)
print(f'Retrieved {len(results)} chunks')
"
```

**US4 (Configuration)**:
```bash
# Test with valid .env
cp .env.example .env
# Edit .env with real API keys
python -c "from config import load_config; config = load_config(); print('Config loaded successfully')"

# Test with missing env var
mv .env .env.backup
python -c "from config import load_config; config = load_config()"
# Verify: Raises validation error listing missing variables
```

---

## Ready-to-Implement Checklist

**Prerequisites** (before starting implementation):

- [ ] **Python 3.11+** installed and available in PATH
- [ ] **Gemini API Key** obtained from Google AI Studio (https://makersuite.google.com/app/apikey)
- [ ] **Qdrant Cloud account** created (https://cloud.qdrant.io)
- [ ] **Qdrant cluster** provisioned (Free Tier)
- [ ] **Qdrant API key** generated from cluster settings
- [ ] **Qdrant cluster URL** noted (format: https://<cluster-id>.qdrant.io)
- [ ] **Git repository** cloned locally
- [ ] **Current branch** is `002-rag-chatbot-backend`
- [ ] **Docusaurus book content** exists in `/docs` folder with markdown files
- [ ] **(Optional) uv** installed for faster package management

**Environment Setup** (complete before T001):

- [ ] Navigate to repository root: `cd /path/to/Physical_AI_Humanoid_Robotics_Book`
- [ ] Verify branch: `git branch --show-current` (should be `002-rag-chatbot-backend`)
- [ ] Verify docs exist: `ls docs/` (should show markdown files or folders)
- [ ] Verify Python version: `python --version` (should be 3.11 or higher)

**Ready to Start**: Once all prerequisites and environment setup items are checked, begin with **T001**.

---

## Task Summary

**Total Tasks**: 49
**Breakdown by Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Configuration - US4): 6 tasks
- Phase 3 (Data Models): 4 tasks
- Phase 4 (Indexing - US3): 8 tasks
- Phase 5 (RAG Q&A - US1): 6 tasks
- Phase 6 (Error Handling - US2): 7 tasks
- Phase 7 (Documentation): 5 tasks
- Phase 8 (Polish): 8 tasks

**Parallelizable Tasks**: 23 tasks marked with [P]

**Estimated Effort**:
- **MVP (Phases 1-5 + basic README)**: ~12-16 hours for experienced developer, 20-25 hours for beginner
- **Full Implementation (all phases)**: ~20-25 hours for experienced developer, 30-40 hours for beginner

**Suggested Implementation Order**:
1. MVP First: Phases 1 → 2 → 3 → 4 → 5 + T037 (basic README)
2. Test MVP thoroughly with various questions
3. Add Error Handling: Phase 6
4. Complete Documentation: Phase 7 (remaining tasks)
5. Add Polish: Phase 8

---

## Notes

- **Important**: Based on research (research.md), use Google's native `google-generativeai` SDK, not OpenAI SDK, as Gemini API is not compatible with OpenAI SDK format
- All tasks confined to `/backend` folder - no modifications to Docusaurus frontend
- Tasks are independently executable - each task has clear acceptance criteria
- File paths are explicit in every task description
- Configuration loaded from `.env` file (never hardcode secrets)
- Error handling prioritizes clear, actionable messages for users
- Performance target: < 5 seconds for 95% of queries

---

**Status**: Ready for implementation. Begin with T001.
