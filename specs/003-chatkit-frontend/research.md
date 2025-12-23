# Research: ChatKit Frontend Integration

**Feature**: 003-chatkit-frontend
**Date**: 2025-12-19
**Purpose**: Research technical decisions for ChatKit widget integration with existing RAG backend

---

## 1. ChatKit Integration Method

### Decision: Use OpenAI ChatKit with Custom Backend (Self-Hosted)

**Rationale**:
- OpenAI ChatKit provides a production-ready chat UI framework specifically designed for AI-powered conversational interfaces
- Supports both vanilla JavaScript and React implementations
- Provides self-hosted backend option, allowing us to connect to our existing RAG backend (FastAPI + Qdrant + Gemini)
- Minimal setup with comprehensive widget customization capabilities

**Alternatives Considered**:
1. **ChatBotKit** (Score: 70.4, 442 snippets)
   - ❌ Rejected: Platform-based solution requiring full adoption of their infrastructure
   - ❌ Would require migrating away from our existing RAG backend

2. **Build Custom Widget from Scratch**
   - ❌ Rejected: Significant development effort to replicate production-ready features
   - ❌ Would need to implement: message threading, streaming responses, error handling, accessibility, responsive design

3. **OpenAI ChatKit** (Selected)
   - ✅ Framework-agnostic (supports vanilla JS and React)
   - ✅ Self-hosted backend option connects to our existing FastAPI server
   - ✅ Production-ready UI with streaming, widgets, and customization
   - ✅ 410 code snippets with High source reputation (Score: 52.7)

**Implementation Path**:
- Use vanilla JavaScript approach with custom web component `<openai-chatkit>`
- Configure with `CustomApiConfig` pointing to our FastAPI backend
- Backend (already implemented) exposes `/ask` endpoint that ChatKit will consume

**References**:
- [OpenAI ChatKit Documentation](https://openai.github.io/chatkit-js/)
- [ChatKit Quickstart Guide](https://openai.github.io/chatkit-js/quickstart)

---

## 2. Installation & Loading Strategy

### Decision: CDN Script Tag + ESM Module

**Rationale**:
- Simplest deployment model for Docusaurus integration
- No build step required for the frontend folder
- ChatKit loads asynchronously without blocking page render
- Compatible with Docusaurus's static site generation

**Implementation**:
```html
<!-- Load ChatKit library from CDN -->
<script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" async></script>

<!-- Initialize widget -->
<script type="module">
  import '@openai/chatkit';

  const chatkit = document.createElement('openai-chatkit');
  chatkit.setOptions({
    api: {
      url: 'http://localhost:8000/ask',  // Our FastAPI backend
      domainKey: 'docusaurus-book-chatkit'
    },
    theme: { colorScheme: 'light' },
    composer: { placeholder: 'Ask about Physical AI & Humanoid Robotics...' }
  });
  document.body.appendChild(chatkit);
</script>
```

**Alternatives Considered**:
1. **NPM Package Installation**
   - ❌ Rejected: Requires build tooling and bundler setup
   - ❌ Adds complexity to deployment process

2. **CDN + ESM** (Selected)
   - ✅ No build step required
   - ✅ Faster deployment and updates
   - ✅ Browser-native module loading
   - ✅ Async loading doesn't block page rendering

**References**:
- [ChatKit Installation - Vanilla JS](https://openai.github.io/chatkit-js/quickstart)
- [ChatKit CDN Script Tag](https://openai.github.io/chatkit-js/api/openai/chatkit/interfaces/openaichatkit)

---

## 3. Widget Placement Strategy

### Decision: Fixed Position Bottom-Right with CSS `position: fixed`

**Rationale**:
- Industry standard for chat widgets (Intercom, Drift, Zendesk pattern)
- Remains accessible regardless of scroll position
- Doesn't obscure main content
- Mobile-responsive with conditional positioning

**CSS Implementation**:
```css
openai-chatkit {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  width: 360px;
  height: 600px;
  max-height: calc(100vh - 40px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  transition: transform 0.3s ease;
}

openai-chatkit:hover {
  transform: translateY(-2px);
}

/* Mobile responsive */
@media (max-width: 768px) {
  openai-chatkit {
    bottom: 10px;
    right: 10px;
    left: 10px;
    width: auto;
    height: calc(100vh - 20px);
    max-height: 500px;
  }
}
```

**Best Practices Applied**:
- `position: fixed` with `bottom` and `right` for viewport anchoring
- High `z-index` (9999) ensures widget appears above all page content
- `box-shadow` provides visual depth and separation
- `transition` for smooth hover interactions
- Responsive adjustments for mobile screens

**Alternatives Considered**:
1. **Inline/Embedded Widget**
   - ❌ Rejected: Would require modifying Docusaurus page templates
   - ❌ Not visible across all pages without template changes

2. **Fixed Bottom-Right** (Selected)
   - ✅ Viewport-anchored, always visible
   - ✅ Doesn't interfere with scrolling or content
   - ✅ Familiar UX pattern for users
   - ✅ Mobile-responsive with media queries

**References**:
- [Floating Chat Button Best Practices](https://dev.to/epi2024/floating-button-for-chat-app-in-html-javascript-and-css-3j7j)
- [CSS Positioning Patterns](https://codepen.io/thatkookooguy/pen/VPJpaW)
- [Fixed Positioning for Chat Widgets](https://codehim.com/forms/floating-chat-box-ui-in-html-css/)

---

## 4. Docusaurus Global Integration

### Decision: Use `scripts` Configuration in `docusaurus.config.js`

**Rationale**:
- Official Docusaurus method for adding global scripts
- Ensures script loads on all pages automatically
- No swizzling or component modification required
- Maintains upgrade path for Docusaurus updates

**Implementation**:
```javascript
// docusaurus.config.js
module.exports = {
  // ... other config
  scripts: [
    {
      src: 'https://cdn.platform.openai.com/deployments/chatkit/chatkit.js',
      async: true
    },
    {
      src: '/chatkit-init.js',  // Custom initialization script
      type: 'module',
      async: true
    }
  ],
  stylesheets: [
    '/chatkit-styles.css'  // Widget positioning and styling
  ]
};
```

**File Structure**:
```
/frontend-chatkit/
├── chatkit-init.js       # Widget initialization logic
├── chatkit-styles.css    # Positioning and responsive styles
└── README.md             # Deployment instructions

/static/                  # Docusaurus static folder
├── chatkit-init.js       # Symlink or copy from frontend-chatkit
└── chatkit-styles.css    # Symlink or copy from frontend-chatkit
```

**Alternatives Considered**:
1. **Swizzle Layout Component**
   - ❌ Rejected: Requires ejecting Docusaurus internals
   - ❌ Breaks on Docusaurus upgrades
   - ❌ More complex maintenance

2. **Footer Component Modification**
   - ❌ Rejected: Still requires swizzling
   - ❌ Footer may not render on all pages

3. **`scripts` Config** (Selected)
   - ✅ Official Docusaurus approach
   - ✅ Works on all pages automatically
   - ✅ No internal modifications required
   - ✅ Upgrade-safe

**References**:
- [Docusaurus Config - Scripts](https://docusaurus.io/docs/next/api/docusaurus-config)
- [Adding Scripts to Docusaurus](https://dev.to/rallipi/adding-scripts-to-every-page-of-a-docusaurus-project-3fee)
- [Docusaurus Script Integration](https://patrickjohnstevens.com/add-script-to-the-head-of-a-docusaurous-site)

---

## 5. Backend API Connection

### Decision: Connect to Existing FastAPI `/ask` Endpoint

**Rationale**:
- RAG backend already implements the required `/ask` POST endpoint
- Returns structured JSON response compatible with ChatKit expectations
- CORS middleware already configured to accept frontend requests
- No backend modifications required

**Existing Backend API** (from `backend/main.py`):

**Endpoint**: `POST /ask`

**Request Schema**:
```json
{
  "question": "What is physical AI?"
}
```

**Response Schema**:
```json
{
  "answer": "Physical AI refers to...",
  "request_id": "uuid-string",
  "sources": ["source1", "source2", "source3"]
}
```

**ChatKit Integration**:
```javascript
chatkit.setOptions({
  api: {
    url: process.env.RAG_BACKEND_URL || 'http://localhost:8000/ask',
    domainKey: 'docusaurus-book-chatkit',
    fetch: async (url, options) => {
      // Custom fetch to transform ChatKit request to our backend format
      const body = JSON.parse(options.body);
      const response = await fetch(url, {
        ...options,
        body: JSON.stringify({
          question: body.message || body.question
        })
      });

      const data = await response.json();

      // Transform our backend response to ChatKit format if needed
      return new Response(JSON.stringify({
        answer: data.answer,
        metadata: {
          request_id: data.request_id,
          sources: data.sources
        }
      }), {
        status: response.status,
        headers: response.headers
      });
    }
  }
});
```

**CORS Configuration** (already in place):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (configure for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Alternatives Considered**:
1. **Create New ChatKit-Specific Endpoint**
   - ❌ Rejected: Duplicates existing functionality
   - ❌ Violates constraint of "no backend changes"

2. **Use Existing `/ask` Endpoint** (Selected)
   - ✅ Already implemented and tested
   - ✅ No backend modifications required
   - ✅ Uses custom `fetch` function to transform requests/responses if needed
   - ✅ CORS already configured

**References**:
- [ChatKit CustomApiConfig](https://openai.github.io/chatkit-js/api/openai/chatkit/type-aliases/customapiconfig)
- Existing backend implementation: `backend/main.py:157-212`

---

## 6. Error Handling & User Experience

### Decision: Leverage ChatKit Built-in Error Handling + Backend Error Codes

**Rationale**:
- Backend already implements comprehensive error handling with codes
- ChatKit has built-in UI for displaying errors
- Custom error messages provide user-friendly feedback

**Error Scenarios** (from backend):
1. **Empty Question** → HTTP 400 `QUESTION_EMPTY`
2. **Question Too Long** → HTTP 400 `QUESTION_TOO_LONG` (>4000 chars)
3. **Embedding Service Error** → HTTP 500 `API_ERROR`
4. **Search Service Error** → HTTP 500 `SEARCH_ERROR`
5. **Generic Failure** → HTTP 500 `SERVICE_UNAVAILABLE`

**ChatKit Error Display**:
ChatKit automatically displays error messages returned from the backend in the chat UI. No custom error handling component required.

**Enhanced UX Configuration**:
```javascript
chatkit.setOptions({
  // ... api config
  startScreen: {
    greeting: 'Ask me anything about Physical AI & Humanoid Robotics!',
    prompts: [
      { label: 'What is Physical AI?', prompt: 'Explain physical AI', icon: 'robot' },
      { label: 'Humanoid Components', prompt: 'What are the key components of humanoid robots?', icon: 'settings' },
      { label: 'Control Systems', prompt: 'How do humanoid control systems work?', icon: 'brain' }
    ]
  },
  composer: {
    placeholder: 'Ask about the book content...'
  },
  threadItemActions: {
    feedback: true,  // Allow users to provide feedback
    retry: true      // Allow retry on errors
  }
});
```

**References**:
- [ChatKit Customization](https://openai.github.io/chatkit-js/customize)
- Backend error handling: `backend/main.py:114-154`

---

## 7. Widget State Management

### Decision: Use ChatKit Built-in History + localStorage

**Rationale**:
- ChatKit provides built-in conversation history management
- Browser `localStorage` persists threads across page navigation
- No custom state management required

**Configuration**:
```javascript
chatkit.setOptions({
  history: {
    enabled: true,        // Enable conversation history panel
    showDelete: true,     // Allow users to delete threads
    showRename: true      // Allow users to rename threads
  },
  initialThread: null     // Start with new thread view
});
```

**State Persistence**:
- ChatKit automatically saves conversation threads to browser localStorage
- Threads persist across page navigation within the book
- User can revisit previous conversations via history panel

**Alternatives Considered**:
1. **Custom State Management with Redux/Context**
   - ❌ Rejected: Unnecessary complexity
   - ❌ Duplicates ChatKit's built-in functionality

2. **ChatKit Built-in History** (Selected)
   - ✅ Zero implementation effort
   - ✅ Persistent across navigation
   - ✅ Built-in UI for thread management

**References**:
- [ChatKit History Configuration](https://openai.github.io/chatkit-js/api/openai/chatkit/type-aliases/chatkitoptions)

---

## 8. Deployment Strategy

### Decision: Modular `/frontend-chatkit` Folder with Static File Deployment

**Rationale**:
- Keeps frontend code separate and modular
- Files can be copied to Docusaurus `/static` folder
- No build process required
- Easy to update and maintain independently

**Deployment Steps**:
1. Develop files in `/frontend-chatkit/` at project root
2. Copy `chatkit-init.js` and `chatkit-styles.css` to `/static/` folder
3. Update `docusaurus.config.js` with script/stylesheet references
4. Deploy Docusaurus site (script and styles load automatically)

**File Organization**:
```
/frontend-chatkit/
├── chatkit-init.js          # Widget initialization
├── chatkit-styles.css       # Widget styles and positioning
├── README.md                # Deployment instructions
└── .env.example             # Backend URL configuration template
```

**Configuration Management**:
```javascript
// chatkit-init.js
const BACKEND_URL = window.CHATKIT_CONFIG?.backendUrl || 'http://localhost:8000/ask';

const chatkit = document.createElement('openai-chatkit');
chatkit.setOptions({
  api: {
    url: BACKEND_URL,
    domainKey: 'docusaurus-book'
  },
  // ... other options
});
```

**Alternatives Considered**:
1. **Integrated into Docusaurus Source**
   - ❌ Rejected: Violates "separate frontend folder" requirement
   - ❌ Couples widget to Docusaurus internals

2. **Separate Frontend Folder** (Selected)
   - ✅ Modular and maintainable
   - ✅ Can be updated independently
   - ✅ Easy deployment via static file copy

---

## Summary of Key Decisions

| Decision Area | Choice | Key Reason |
|--------------|--------|------------|
| **Widget Library** | OpenAI ChatKit (vanilla JS) | Production-ready, self-hosted backend support |
| **Installation** | CDN + ESM modules | No build step, browser-native loading |
| **Positioning** | Fixed bottom-right | Industry standard, always visible |
| **Docusaurus Integration** | `scripts` config | Official method, upgrade-safe |
| **Backend Connection** | Existing `/ask` endpoint | No modifications required |
| **Error Handling** | ChatKit built-in + backend codes | Comprehensive, user-friendly |
| **State Management** | ChatKit history + localStorage | Zero implementation, persistent |
| **Deployment** | Modular folder → static files | Simple, maintainable, separated |

---

## Next Steps

**Phase 1 Planning**:
1. Define data model for chat interactions (messages, sessions, state)
2. Create API contract documentation for ChatKit ↔ Backend integration
3. Write quickstart guide for deployment
4. Generate tasks for implementation

**References**:
- All research findings documented with source links above
- Backend API already operational at `backend/main.py`
- ChatKit documentation: https://openai.github.io/chatkit-js/
