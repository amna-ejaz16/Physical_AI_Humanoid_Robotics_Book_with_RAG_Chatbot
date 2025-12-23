# RAG Chatbot Widget - Installation Guide

This chatbot widget provides a floating chat interface on all Docusaurus pages that connects to your FastAPI backend.

## ✅ Installation Complete

The chatbot has been automatically installed and configured:

### Files Created/Modified:

1. **`docs/static/chatbot.js`** - Main chatbot code (self-contained with CSS and JS)
2. **`docs/docusaurus.config.js`** - Updated to load chatbot on all pages

## 🚀 How to Use

### 1. Start Your Backend

Make sure your FastAPI backend is running:

```bash
cd backend
uvicorn main:app --reload
```

The backend should be accessible at `http://localhost:8000`

### 2. Start Docusaurus

```bash
cd docs
npm start
```

### 3. See the Chatbot in Action

- Open your browser to `http://localhost:3000`
- You'll see a chat icon (💬) at the bottom-right corner
- Click it to open the chat window
- Type a question and press Enter or click the send button
- The chatbot will query your `/ask` endpoint and display the response

## 🎨 Features

✅ **Floating Chat Icon** - Always visible at bottom-right
✅ **Smooth Animations** - Slide up, fade in effects
✅ **Typing Indicator** - Shows when bot is "thinking"
✅ **Source Attribution** - Displays sources from backend response
✅ **Mobile Responsive** - Works on all screen sizes
✅ **Clean Design** - Modern, professional UI
✅ **Error Handling** - Graceful error messages
✅ **Keyboard Support** - Press Enter to send

## ⚙️ Configuration

To customize the chatbot, edit `docs/static/chatbot.js` and modify the `CONFIG` object:

```javascript
const CONFIG = {
  apiEndpoint: 'http://localhost:8000/ask',  // Your backend URL
  botName: 'AI Assistant',                    // Chat header name
  welcomeMessage: 'Hello! ...',               // First message
  placeholderText: 'Type your question...',   // Input placeholder
  primaryColor: '#007bff',                    // Main theme color
  // ... more options
};
```

## 🔧 Customization Examples

### Change Colors

```javascript
primaryColor: '#ff6b6b',      // Red theme
userMessageColor: '#ff6b6b',  // User bubble color
```

### Change API Endpoint (for production)

```javascript
apiEndpoint: 'https://your-domain.com/ask',
```

### Modify Welcome Message

```javascript
welcomeMessage: 'Ask me anything about robotics!',
```

## 🐛 Troubleshooting

### Chatbot doesn't appear
- Clear browser cache and reload
- Check browser console for errors
- Verify `chatbot.js` exists in `docs/static/`

### "Failed to connect" errors
- Ensure backend is running on port 8000
- Check CORS is enabled in FastAPI (already configured)
- Verify `/ask` endpoint is working: `curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d '{"question":"test"}'`

### Sources show as "undefined"
- Make sure backend returns `sources` array in response
- Check backend logs for errors

## 📁 File Structure

```
docs/
├── static/
│   └── chatbot.js          ← Chatbot code (all-in-one file)
├── docusaurus.config.js    ← Updated to load chatbot
└── CHATBOT_README.md       ← This file
```

## 🎯 How It Works

1. **Page Load**: `chatbot.js` is loaded on every page
2. **Initialization**: Creates chat icon and window (hidden)
3. **User Clicks**: Chat window slides up
4. **User Types**: Message sent to `/ask` endpoint via POST
5. **Backend Responds**: JSON response with `{answer, sources}`
6. **Display**: Answer and sources shown in chat window

## 🔒 Security Notes

- Current config uses `localhost` - change for production
- Add rate limiting to backend if needed
- Consider adding authentication for production use

## 📝 API Contract

The chatbot expects this response format from `/ask`:

```json
{
  "answer": "Your answer text here",
  "sources": ["Source 1", "Source 2"],
  "request_id": "optional-id"
}
```

## 🚀 Production Deployment

When deploying to production:

1. Update `apiEndpoint` in `chatbot.js`:
   ```javascript
   apiEndpoint: 'https://api.yourdomain.com/ask',
   ```

2. Rebuild Docusaurus:
   ```bash
   npm run build
   ```

3. Deploy the `build` folder to your hosting service

## 📞 Support

If you encounter issues:
1. Check browser console for errors
2. Verify backend is responding: `curl -X POST http://localhost:8000/ask ...`
3. Check that the response format matches the expected structure

---

**That's it! Your chatbot is ready to use.** 🎉
