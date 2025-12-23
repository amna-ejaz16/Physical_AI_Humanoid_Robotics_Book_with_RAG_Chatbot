# Quickstart Guide: RAG Chatbot Backend

**Feature**: RAG Chatbot Backend
**Branch**: 002-rag-chatbot-backend
**Date**: 2025-12-09

## Overview

This guide will help you set up and run the RAG chatbot backend locally. Follow these step-by-step instructions to get the system running in under 15 minutes.

---

## Prerequisites

Before you begin, ensure you have the following:

### Required Software
- **Python 3.11 or higher** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **(Optional) uv** - Fast Python package installer ([Install](https://github.com/astral-sh/uv))

### Required Accounts & API Keys
1. **Gemini API Key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy and save your API key securely

2. **Qdrant Cloud Account** (Free Tier)
   - Go to [Qdrant Cloud](https://cloud.qdrant.io)
   - Sign up for a free account
   - Create a new cluster (Free Tier)
   - Copy your cluster URL (format: `https://<cluster-id>.qdrant.io`)
   - Generate an API key from cluster settings

---

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### Step 2: Navigate to Backend Folder

```bash
cd backend
```

### Step 3: Create Virtual Environment

**Option A: Using `uv` (Recommended - Faster)**
```bash
uv venv
source .venv/bin/activate  # On Linux/macOS
# OR
.venv\Scripts\activate  # On Windows
```

**Option B: Using standard Python venv**
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# OR
.venv\Scripts\activate  # On Windows
```

You should see `(.venv)` prefix in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected packages:**
- fastapi
- uvicorn
- google-generativeai
- qdrant-client
- pydantic
- pydantic-settings
- python-dotenv
- tiktoken

Installation should complete in 30-60 seconds.

### Step 5: Configure Environment Variables

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your favorite text editor:
   ```bash
   nano .env  # or vim, code, notepad, etc.
   ```

3. **Fill in your API keys:**
   ```env
   # Gemini API Configuration
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   GEMINI_EMBEDDING_MODEL=models/text-embedding-004

   # Qdrant Configuration
   QDRANT_URL=https://your-cluster-id.qdrant.io
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION=book_chunks

   # Server Configuration (Optional - defaults are fine for local dev)
   SERVER_HOST=0.0.0.0
   SERVER_PORT=8000
   SERVER_DEBUG=False

   # RAG Configuration (Optional - defaults are fine)
   RAG_CHUNK_SIZE=500
   RAG_CHUNK_OVERLAP=50
   RAG_TOP_K=3
   RAG_BOOK_CONTENT_PATH=../docs
   ```

4. **Save the file** (Ctrl+O, Enter, Ctrl+X for nano)

### Step 6: Index Book Content (One-Time Setup)

This step reads the book's markdown files, generates embeddings, and stores them in Qdrant.

```bash
python indexer.py
```

**Expected output:**
```
Indexing book content from ../docs
Found 15 markdown files
Processing: docs/chapters/01-introduction.md
  Created 3 chunks
Processing: docs/chapters/02-embodied-intelligence.md
  Created 4 chunks
...
Total chunks created: 87
Uploading to Qdrant...
Successfully indexed 87 chunks
Indexing complete!
```

**Note:** This process may take 2-5 minutes depending on book size and API rate limits. Run this only once, or whenever book content is updated.

### Step 7: Start the Server

```bash
uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The backend is now running at **http://localhost:8000**

---

## Testing the API

### Method 1: Using curl (Terminal)

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
  "sources": ["docs/chapters/01-introduction.md"]
}
```

**Check health:**
```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "qdrant_connected": true
}
```

### Method 2: Using FastAPI Interactive Docs

1. Open your browser and go to: **http://localhost:8000/docs**
2. You'll see the auto-generated Swagger UI
3. Click on `/ask` endpoint → "Try it out"
4. Enter your question in the JSON input:
   ```json
   {
     "question": "Explain reinforcement learning in robotics"
   }
   ```
5. Click "Execute"
6. View the response below

### Method 3: Using Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is physical AI?"}
)

print(response.json())
```

### Method 4: Using Postman

1. Open Postman
2. Create a new POST request to `http://localhost:8000/ask`
3. Set Headers: `Content-Type: application/json`
4. Set Body (raw JSON):
   ```json
   {
     "question": "What is physical AI?"
   }
   ```
5. Click "Send"

---

## Example Questions to Try

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
   {"question": "What are the differences between model-based and model-free reinforcement learning in robotics?"}
   ```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate  # Activate venv
pip install -r requirements.txt
```

### Issue: "Error: GEMINI_API_KEY not set"

**Solution:** Ensure `.env` file exists in `/backend` folder and contains your API key:
```bash
cat .env  # Check if file exists and has GEMINI_API_KEY
```

### Issue: "Qdrant connection failed"

**Solutions:**
1. Verify Qdrant URL is correct (should be HTTPS with cluster ID)
2. Check API key is valid
3. Ensure cluster is running in Qdrant Cloud dashboard
4. Try pinging cluster: `curl https://your-cluster-id.qdrant.io/collections`

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
2. Or use a different port:
   ```bash
   uvicorn main:app --reload --port 8080
   ```

---

## Stopping the Server

Press `Ctrl+C` in the terminal where uvicorn is running.

**Output:**
```
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [12346]
```

---

## Re-Indexing Book Content

If the book content is updated (new chapters, edits to existing chapters), re-run the indexer:

```bash
python indexer.py --force  # Deletes existing collection and re-indexes
```

**Warning:** This will delete all existing vectors in Qdrant and create new ones.

---

## Deployment (Production)

### Deploying to Render

1. **Connect Repository:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service:**
   - Name: `rag-chatbot-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: Leave empty (or set to `/backend` if supported)

3. **Set Environment Variables:**
   - Add all variables from your `.env` file in Render dashboard
   - Important: Don't commit `.env` to Git!

4. **Deploy:**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Note your public URL: `https://your-app.onrender.com`

5. **Run Indexer (One-Time):**
   - After deployment, run indexer via SSH or local script pointing to production Qdrant

### Deploying to Railway

1. **Create New Project:**
   - Go to [Railway Dashboard](https://railway.app)
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository

2. **Configure Service:**
   - Railway auto-detects Python
   - Set Root Directory: `/backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables:**
   - In Railway project settings, add all env vars from `.env`

4. **Deploy:**
   - Railway will auto-deploy on push
   - Note your public URL

---

## Project Structure Reference

```
backend/
├── main.py                # FastAPI app entry point
├── agent_client.py        # Gemini API integration
├── rag_client.py          # RAG logic (embeddings, search)
├── config.py              # Configuration management
├── models.py              # Pydantic models (ChatRequest, ChatResponse, etc.)
├── indexer.py             # Book content indexing script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (gitignored)
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore rules
└── README.md              # Detailed setup and deployment guide
```

---

## Next Steps

1. ✅ Backend is running locally
2. → Test the API with various questions
3. → Integrate frontend (make API calls from Docusaurus site)
4. → Deploy to production (Render or Railway)
5. → Monitor logs and performance
6. → (Optional) Add authentication for production use

---

## Support & Feedback

- **Issues:** [GitHub Issues](https://github.com/your-username/your-repo/issues)
- **Documentation:** See `/backend/README.md` for detailed API docs
- **API Reference:** Visit `http://localhost:8000/docs` when server is running

---

**Congratulations!** You've successfully set up the RAG chatbot backend. 🎉
