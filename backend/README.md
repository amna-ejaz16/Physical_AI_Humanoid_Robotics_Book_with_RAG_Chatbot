# RAG Chatbot Backend

Retrieval-Augmented Generation (RAG) chatbot backend for the Physical AI & Humanoid Robotics book. This backend enables users to ask questions about the book content and receive AI-generated answers based on the most relevant sections.

## 🎯 Features

- **Semantic Search**: Vector-based search using Gemini embeddings and Qdrant
- **Context-Aware Answers**: AI answers generated from retrieved book content
- **Source Attribution**: Responses include source file references
- **Production-Ready**: FastAPI with error handling, logging, and health checks
- **Beginner-Friendly**: Step-by-step setup with clear documentation

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11 or higher** ([Download](https://www.python.org/downloads/))
- **Gemini API Key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Qdrant Cloud Account** (Free Tier) from [Qdrant Cloud](https://cloud.qdrant.io)

## 🚀 Quick Start

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

**Option A: Using standard Python venv**
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# OR
.venv\Scripts\activate  # On Windows
```

**Option B: Using uv (faster)**
```bash
uv venv
source .venv/bin/activate  # On Linux/macOS
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your actual API keys:
```env
# Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_EMBEDDING_MODEL=models/text-embedding-004

# Qdrant Configuration
QDRANT_URL=https://your-cluster-id.qdrant.io
QDRANT_API_KEY=your_actual_qdrant_api_key_here
QDRANT_COLLECTION=book_chunks

# Server Configuration (defaults are fine for development)
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
SERVER_DEBUG=False

# RAG Configuration (defaults are fine)
RAG_CHUNK_SIZE=500
RAG_CHUNK_OVERLAP=50
RAG_TOP_K=3
RAG_BOOK_CONTENT_PATH=../docs
```

**How to get API keys:**

1. **Gemini API Key**:
   - Go to https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the key and paste it into your `.env` file

2. **Qdrant Cloud**:
   - Go to https://cloud.qdrant.io
   - Sign up for a free account
   - Create a new cluster (Free Tier)
   - Copy the cluster URL (format: `https://<cluster-id>.qdrant.io`)
   - Generate an API key from cluster settings
   - Paste both into your `.env` file

### 5. Index Book Content (One-Time Setup)

This step reads the book's markdown files, generates embeddings, and stores them in Qdrant:

```bash
python indexer.py
```

**Expected output:**
```
=== Starting book content indexing ===
Found 15 markdown files
Processing (1/15): ../docs/intro.md
  Created 3 chunks
  Generated 3/3 embeddings
Processing (2/15): ../docs/chapter1.md
  Created 5 chunks
  ...
=== Uploading to Qdrant ===
Total chunks to upload: 87
✓ Successfully uploaded all chunks
=== Indexing Complete ===
Files processed: 15/15
Total chunks indexed: 87
```

**⚠️ Important**: Run this indexing step **only once** (or when book content is updated). To force re-indexing, use:
```bash
python indexer.py --force
```

### 6. Start the Server

```bash
uvicorn main:app --reload
```

**Expected output:**
```
=== Starting RAG Chatbot Backend ===
✓ Configuration loaded
✓ Gemini client initialized
✓ Qdrant client initialized
✓ Qdrant connection verified
✓ RAG pipeline initialized
=== Backend ready ===
Server: http://0.0.0.0:8000
API docs: http://0.0.0.0:8000/docs
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

The backend is now running! 🎉

## 🧪 Testing the API

### Method 1: Using curl (Command Line)

**Ask a question:**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is physical AI?"}'
```

**Expected response:**
```json
{
  "answer": "Physical AI refers to artificial intelligence systems that are embodied in physical robots...",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "sources": ["../docs/intro.md", "../docs/chapter1.md"]
}
```

**Test error handling (empty question):**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": ""}'
```

**Expected error:**
```json
{
  "error": "Question cannot be empty or whitespace-only",
  "error_code": "VALIDATION_ERROR",
  "request_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901"
}
```

**Check health:**
```bash
curl http://localhost:8000/health
```

### Method 2: Using FastAPI Interactive Docs

1. Open your browser
2. Go to: http://localhost:8000/docs
3. You'll see the auto-generated Swagger UI
4. Click on `/ask` → "Try it out"
5. Enter your question:
   ```json
   {
     "question": "Explain reinforcement learning in robotics"
   }
   ```
6. Click "Execute"
7. View the response below

### Method 3: Using Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is physical AI?"}
)

result = response.json()
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
```

### Method 4: Using Postman

1. Open Postman
2. Create a new POST request to `http://localhost:8000/ask`
3. Set Headers: `Content-Type: application/json`
4. Set Body (raw JSON):
   ```json
   {
     "question": "What are the main challenges in humanoid robotics?"
   }
   ```
5. Click "Send"

## 📚 Example Questions to Try

1. **Simple question:**
   ```json
   {"question": "What is physical AI?"}
   ```

2. **Detailed question:**
   ```json
   {"question": "How does reinforcement learning help humanoid robots learn to walk?"}
   ```

3. **Specific technical question:**
   ```json
   {"question": "What are the main challenges in real-time control for bipedal locomotion?"}
   ```

4. **Comparative question:**
   ```json
   {"question": "What are the differences between model-based and model-free reinforcement learning?"}
   ```

## 🔌 API Endpoints

### POST /ask

Ask a question about the book content.

**Request:**
```json
{
  "question": "string (1-4000 characters)"
}
```

**Response (200 OK):**
```json
{
  "answer": "string",
  "request_id": "uuid",
  "sources": ["string"]
}
```

**Error Responses:**
- **400 Bad Request**: Invalid input (empty question, too long, validation error)
- **500 Internal Server Error**: API error, search error, service unavailable

**Error Codes:**
- `VALIDATION_ERROR`: Generic validation failure
- `QUESTION_EMPTY`: Question is empty or whitespace-only
- `QUESTION_TOO_LONG`: Question exceeds 4000 characters
- `API_ERROR`: Gemini API failure
- `SEARCH_ERROR`: Qdrant search failure
- `SERVICE_UNAVAILABLE`: General server error

### GET /health

Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "qdrant_connected": true
}
```

**Response (503 Service Unavailable):**
```json
{
  "status": "unhealthy",
  "qdrant_connected": false,
  "error": "Connection failed"
}
```

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate  # Activate venv
pip install -r requirements.txt
```

### Issue: "Configuration error: GEMINI_API_KEY not set"

**Solution:** Ensure `.env` file exists in the `/backend` folder and contains your API key:
```bash
cat .env  # Check if file exists and has GEMINI_API_KEY
```

### Issue: "Qdrant connection failed"

**Solutions:**
1. Verify Qdrant URL is correct (should be HTTPS with cluster ID)
2. Check API key is valid
3. Ensure cluster is running in Qdrant Cloud dashboard
4. Try pinging the cluster: `curl https://your-cluster-id.qdrant.io/collections`

### Issue: "Question cannot be empty" error

**Solution:** Ensure your question is not empty or whitespace-only:
```json
{"question": "Your actual question here"}
```

### Issue: "Rate limit exceeded" error

**Solution:** Gemini API has rate limits (typically 60 requests/minute). Wait 60 seconds and retry.

### Issue: Port 8000 already in use

**Solution:** Either:
1. Stop the process using port 8000
2. Or use a different port: `uvicorn main:app --reload --port 8080`

### Issue: No markdown files found during indexing

**Solution:** Verify the `RAG_BOOK_CONTENT_PATH` in your `.env` points to the correct location:
```bash
ls ../docs  # Should show markdown files
```

## 🚢 Deployment

### Deploying to Render

1. **Create Render Account**
   - Go to https://dashboard.render.com
   - Sign up or log in

2. **Create New Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - **Name**: `rag-chatbot-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend` (if repo root is not backend)

4. **Set Environment Variables**
   - Add all variables from your `.env` file in the Render dashboard
   - ⚠️ **Important**: Use actual API keys, not the example values

5. **Deploy**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Note your public URL: `https://your-app.onrender.com`

6. **Run Indexer (One-Time)**
   - After deployment, you need to index the book content once
   - Option A: Use Render Shell (if available)
   - Option B: Run indexer locally pointing to production Qdrant

### Deploying to Railway

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository

3. **Configure Service**
   - Railway auto-detects Python
   - Set Root Directory: `backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**
   - In Railway project settings, add all env vars from `.env`

5. **Deploy**
   - Railway will auto-deploy on push
   - Note your public URL

## 📁 Project Structure

```
backend/
├── main.py                # FastAPI application entry point
├── agent_client.py        # Gemini API client for embeddings & generation
├── rag_client.py          # RAG components (chunking, parsing, Qdrant, pipeline)
├── config.py              # Configuration management (Pydantic Settings)
├── models.py              # Pydantic models (request/response/error)
├── indexer.py             # Book content indexing script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── .env                   # Actual environment variables (gitignored)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔐 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✓ | - | Gemini API key from Google AI Studio |
| `GEMINI_MODEL` | | `gemini-1.5-flash` | Gemini model for text generation |
| `GEMINI_EMBEDDING_MODEL` | | `models/text-embedding-004` | Gemini embedding model |
| `QDRANT_URL` | ✓ | - | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | ✓ | - | Qdrant API key |
| `QDRANT_COLLECTION` | | `book_chunks` | Qdrant collection name |
| `SERVER_HOST` | | `0.0.0.0` | Server bind host |
| `SERVER_PORT` | | `8000` | Server port |
| `SERVER_DEBUG` | | `False` | Enable debug mode |
| `RAG_CHUNK_SIZE` | | `500` | Target tokens per chunk (100-1000) |
| `RAG_CHUNK_OVERLAP` | | `50` | Overlap tokens (0-200) |
| `RAG_TOP_K` | | `3` | Number of chunks to retrieve (1-10) |
| `RAG_BOOK_CONTENT_PATH` | | `../docs` | Path to book markdown files |

## 🧹 Maintenance

### Re-indexing Book Content

If the book content is updated, re-run the indexer:

```bash
python indexer.py --force
```

**⚠️ Warning**: This deletes all existing embeddings and re-creates them.

### Updating Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Checking Logs

Logs are output to console. In production, configure logging to file:

```python
# Add to main.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend.log'),
        logging.StreamHandler()
    ]
)
```

## 📊 Performance

- **Response Time**: Typically 2-4 seconds per query
- **Throughput**: Handles 100+ concurrent requests
- **Storage**: ~277KB for 90 chunks (well within Qdrant Free Tier 1GB limit)

## 🤝 Support

- **Issues**: Report bugs or issues in the GitHub repository
- **API Docs**: Visit http://localhost:8000/docs when server is running
- **Logs**: Check console output for debugging information

## 📄 License

This project is part of the Physical AI & Humanoid Robotics book.

---

**Happy Chatting!** 🤖✨
