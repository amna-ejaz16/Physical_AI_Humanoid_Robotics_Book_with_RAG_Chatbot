# Vercel Deployment Guide

This guide covers deploying both the **frontend (Docusaurus)** and **backend (FastAPI)** to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at https://vercel.com
2. **Vercel CLI** (optional but recommended):
   ```bash
   npm install -g vercel
   ```
3. **Environment Variables**: Have your API keys ready:
   - `GEMINI_API_KEY` - Your Google Gemini API key
   - `QDRANT_URL` - Your Qdrant cluster URL
   - `QDRANT_API_KEY` - Your Qdrant API key

---

## Option 1: Deploy via Vercel Dashboard (Recommended for Beginners)

### A. Deploy Frontend (Docusaurus Site)

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Click "Add New Project"

2. **Import Repository**
   - Select "Import Git Repository"
   - Choose your repository: `Physical_AI_Humanoid_Robotics_Book_with_RAG_Chatbot`
   - Click "Import"

3. **Configure Frontend Project**
   ```
   Project Name: physical-ai-robotics-frontend (or your choice)
   Framework Preset: Docusaurus
   Root Directory: docs
   Build Command: npm run build
   Output Directory: build
   Install Command: npm install
   ```

4. **Environment Variables**
   - No environment variables needed for frontend (ChatKit will connect to backend)

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Note your frontend URL (e.g., `https://physical-ai-robotics-frontend.vercel.app`)

### B. Deploy Backend (FastAPI)

1. **Create New Project**
   - In Vercel Dashboard, click "Add New Project"
   - Import the **same repository** again

2. **Configure Backend Project**
   ```
   Project Name: physical-ai-robotics-backend (or your choice)
   Framework Preset: Other
   Root Directory: backend
   Build Command: (leave empty)
   Output Directory: (leave empty)
   Install Command: pip install -r requirements.txt
   ```

3. **Add Environment Variables** (CRITICAL)
   Click "Environment Variables" and add:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

   Make sure to set these for:
   - ✅ Production
   - ✅ Preview
   - ✅ Development

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Note your backend URL (e.g., `https://physical-ai-robotics-backend.vercel.app`)

---

## Option 2: Deploy via Vercel CLI (Recommended for Developers)

### A. Deploy Frontend

```bash
# Navigate to the docs directory
cd docs

# Login to Vercel (first time only)
vercel login

# Deploy to production
vercel --prod

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? [Select your account]
# - Link to existing project? No
# - What's your project's name? physical-ai-robotics-frontend
# - In which directory is your code located? ./
# - Want to override settings? No
```

### B. Deploy Backend

```bash
# Navigate to the backend directory
cd ../backend

# Add environment variables first
vercel env add GEMINI_API_KEY
# Enter your Gemini API key when prompted
# Select: Production, Preview, Development

vercel env add QDRANT_URL
# Enter your Qdrant URL when prompted
# Select: Production, Preview, Development

vercel env add QDRANT_API_KEY
# Enter your Qdrant API key when prompted
# Select: Production, Preview, Development

# Deploy to production
vercel --prod

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? [Select your account]
# - Link to existing project? No
# - What's your project's name? physical-ai-robotics-backend
# - In which directory is your code located? ./
# - Want to override settings? No
```

---

## Post-Deployment Configuration

### 1. Update Frontend to Point to Backend

After deploying both services, you need to update the frontend to use the backend URL:

**Edit `docs/src/components/FloatingChatbot.jsx`:**
```javascript
const BACKEND_URL = 'https://your-backend-url.vercel.app'; // Update this
```

**Or better, use environment variables:**

Create `docs/.env.production`:
```env
REACT_APP_BACKEND_URL=https://your-backend-url.vercel.app
```

Then update the component to use:
```javascript
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
```

### 2. Update CORS in Backend

**Edit `backend/main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-url.vercel.app",  # Add your frontend URL
        "http://localhost:3000"  # Keep for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Redeploy

After making these changes:
```bash
# Commit changes
git add .
git commit -m "Update frontend and backend URLs for production"
git push

# Vercel will auto-deploy if you've enabled GitHub integration
# Or manually redeploy:
cd docs && vercel --prod
cd ../backend && vercel --prod
```

---

## Important Notes

### Backend Limitations on Vercel

⚠️ **Serverless Function Timeout**: Vercel's free tier has a 10-second timeout for serverless functions. For longer operations:
- Upgrade to Pro plan (60-second timeout)
- Or consider deploying backend to Railway, Render, or Fly.io instead

⚠️ **Cold Starts**: The first request after inactivity may be slower due to cold starts.

⚠️ **Persistent Connections**: The `lifespan` context manager in FastAPI might not work optimally in serverless. Consider:
- Initializing clients on first request
- Using connection pooling
- Moving to a persistent deployment platform for the backend

### Alternative Backend Deployment Options

If Vercel doesn't work well for your backend:

**Railway** (Recommended for Python backends):
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd backend
railway init
railway up
```

**Render**:
- Create account at https://render.com
- Create new "Web Service"
- Connect repository
- Set root directory to `backend`
- Add environment variables
- Deploy

---

## Troubleshooting

### Build Error: "npm build" not found
✅ **Fixed** - Updated `package.json` to use `npm run build`

### Backend Returns 500 Error
- Check environment variables are set correctly in Vercel
- View logs: `vercel logs [deployment-url]`
- Ensure Qdrant is accessible from Vercel's servers

### Frontend Can't Connect to Backend
- Check CORS settings in backend
- Verify backend URL is correct in frontend
- Check browser console for errors

### Timeout Errors
- Upgrade Vercel plan
- Optimize backend queries
- Consider alternative hosting for backend

---

## Deployment Checklist

### Frontend ✅
- [ ] Deploy to Vercel
- [ ] Note frontend URL
- [ ] Update backend URL in frontend code
- [ ] Redeploy frontend

### Backend ✅
- [ ] Deploy to Vercel (or alternative platform)
- [ ] Set all environment variables
- [ ] Note backend URL
- [ ] Update CORS settings
- [ ] Test API endpoints
- [ ] Redeploy backend

### Testing ✅
- [ ] Visit frontend URL
- [ ] Test chatbot functionality
- [ ] Check browser console for errors
- [ ] Verify backend responses

---

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Review browser console errors
3. Test backend API directly using `/docs` endpoint
4. Verify all environment variables are set

## Next Steps

1. Set up custom domain (optional)
2. Configure analytics
3. Set up monitoring
4. Enable auto-deployment from GitHub
