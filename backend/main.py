"""FastAPI application for RAG chatbot backend."""

import logging
import uuid
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from config import load_config, AppConfig
from models import (
    ChatRequest, ChatResponse, ErrorResponse, HealthResponse,
    VALIDATION_ERROR, QUESTION_EMPTY, QUESTION_TOO_LONG,
    API_ERROR, SEARCH_ERROR, SERVICE_UNAVAILABLE
)
from agent_client import GeminiClient
from rag_client import QdrantManager, RAGPipeline

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
app_config: AppConfig = None
rag_pipeline: RAGPipeline = None


# Custom exception classes
class APIError(Exception):
    """Custom exception for API errors."""

    def __init__(self, message: str, error_code: str, status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    global app_config, rag_pipeline

    # Startup
    logger.info("=== Starting RAG Chatbot Backend ===")

    # Load configuration
    load_dotenv()
    try:
        app_config = load_config()
        logger.info("✓ Configuration loaded")
    except Exception as e:
        logger.error(f"✗ Configuration failed: {e}")
        raise

    # Initialize clients
    try:
        gemini_client = GeminiClient(app_config.agent)
        logger.info("✓ Gemini client initialized")

        qdrant_manager = QdrantManager(app_config.qdrant)
        logger.info("✓ Qdrant client initialized")

        # Test Qdrant connection
        if not qdrant_manager.health_check():
            raise Exception("Qdrant health check failed")
        logger.info("✓ Qdrant connection verified")

        # Initialize RAG pipeline
        rag_pipeline = RAGPipeline(
            gemini_client=gemini_client,
            qdrant_manager=qdrant_manager,
            top_k=app_config.rag.top_k
        )
        logger.info("✓ RAG pipeline initialized")

    except Exception as e:
        logger.error(f"✗ Initialization failed: {e}")
        raise

    logger.info("=== Backend ready ===")
    logger.info(f"Server: http://{app_config.server.host}:{app_config.server.port}")
    logger.info(f"API docs: http://{app_config.server.host}:{app_config.server.port}/docs")

    yield

    # Shutdown
    logger.info("=== Shutting down ===")


# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot Backend",
    description="Retrieval-Augmented Generation chatbot for Physical AI & Humanoid Robotics book",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    """Handle custom API errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.message,
            error_code=exc.error_code,
            request_id=str(uuid.uuid4())
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            error="Validation failed",
            error_code=VALIDATION_ERROR,
            request_id=str(uuid.uuid4()),
            detail=exc.errors()
        ).model_dump()
    )


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            error_code=SERVICE_UNAVAILABLE,
            request_id=str(uuid.uuid4())
        ).model_dump()
    )


# API endpoints
@app.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """
    Ask a question about the book content.

    The system will:
    1. Generate an embedding for your question
    2. Search for the top 3 most relevant book content chunks
    3. Generate an AI answer based on the retrieved content
    4. Return the answer with source attribution
    """
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Question received (length: {len(request.question)})")

    # Additional validation
    if len(request.question) > 4000:
        raise APIError(
            message="Question exceeds maximum length of 4000 characters",
            error_code=QUESTION_TOO_LONG,
            status_code=400
        )

    try:
        # Call RAG pipeline
        answer, sources = rag_pipeline.ask(request.question)

        logger.info(f"[{request_id}] Answer generated (sources: {len(sources)})")

        return ChatResponse(
            answer=answer,
            request_id=request_id,
            sources=sources
        )

    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}")

        # Determine error type
        if "embedding" in str(e).lower():
            raise APIError(
                message=f"Failed to process question: {str(e)}",
                error_code=API_ERROR,
                status_code=500
            )
        elif "search" in str(e).lower() or "qdrant" in str(e).lower():
            raise APIError(
                message="Search service temporarily unavailable",
                error_code=SEARCH_ERROR,
                status_code=500
            )
        else:
            raise APIError(
                message="Failed to generate answer",
                error_code=SERVICE_UNAVAILABLE,
                status_code=500
            )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns the health status of the backend service and its dependencies.
    """
    try:
        # Check Qdrant connection
        qdrant_healthy = rag_pipeline.qdrant_manager.health_check()

        if qdrant_healthy:
            return HealthResponse(
                status="healthy",
                qdrant_connected=True
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content=HealthResponse(
                    status="unhealthy",
                    qdrant_connected=False,
                    error="Qdrant connection failed"
                ).model_dump()
            )

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=HealthResponse(
                status="unhealthy",
                qdrant_connected=False,
                error=str(e)
            ).model_dump()
        )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "RAG Chatbot Backend",
        "version": "1.0.0",
        "description": "Retrieval-Augmented Generation chatbot for Physical AI & Humanoid Robotics book",
        "endpoints": {
            "ask": "POST /ask - Ask a question about the book",
            "health": "GET /health - Health check",
            "docs": "GET /docs - Interactive API documentation"
        }
    }


@app.get("/chat", response_class=HTMLResponse)
async def chat_interface():
    """Simple HTML chat interface for embedding in iframe."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAG Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: #f5f5f5;
        }
        #chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .message {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 8px;
            word-wrap: break-word;
        }
        .user-message {
            align-self: flex-end;
            background: #007bff;
            color: white;
        }
        .bot-message {
            align-self: flex-start;
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
        }
        .sources {
            font-size: 0.85em;
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid #e0e0e0;
            color: #666;
        }
        #input-container {
            display: flex;
            gap: 8px;
            padding: 16px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }
        #question-input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        #send-button {
            padding: 12px 24px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
        }
        #send-button:hover:not(:disabled) {
            background: #0056b3;
        }
        #send-button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 12px;
            border-radius: 4px;
            margin: 8px 0;
        }
    </style>
</head>
<body>
    <div id="chat-container">
        <div class="message bot-message">
            Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics book. Ask me anything!
        </div>
    </div>
    <div id="input-container">
        <input type="text" id="question-input" placeholder="Type your question here..." />
        <button id="send-button">Send</button>
    </div>

    <script>
        const chatContainer = document.getElementById('chat-container');
        const questionInput = document.getElementById('question-input');
        const sendButton = document.getElementById('send-button');

        function addMessage(text, isUser, sources = null) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.textContent = text;

            if (sources && sources.length > 0) {
                const sourcesDiv = document.createElement('div');
                sourcesDiv.className = 'sources';
                sourcesDiv.innerHTML = '<strong>Sources:</strong><br>' +
                    sources.map(s => `• ${s}`).join('<br>');
                messageDiv.appendChild(sourcesDiv);
            }

            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function showError(message) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.textContent = message;
            chatContainer.appendChild(errorDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        async function sendQuestion() {
            const question = questionInput.value.trim();
            if (!question) return;

            addMessage(question, true);
            questionInput.value = '';
            sendButton.disabled = true;

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question }),
                });

                const data = await response.json();

                if (response.ok) {
                    addMessage(data.answer, false, data.sources);
                } else {
                    showError(data.error || 'An error occurred');
                }
            } catch (error) {
                showError('Failed to connect to the server');
            } finally {
                sendButton.disabled = false;
                questionInput.focus();
            }
        }

        sendButton.addEventListener('click', sendQuestion);
        questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendQuestion();
        });

        questionInput.focus();
    </script>
</body>
</html>
"""

