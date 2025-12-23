# Quick Start Guide: ChatKit Frontend Integration

**Feature**: 003-chatkit-frontend
**Purpose**: Step-by-step guide to deploy the ChatKit widget on the Docusaurus book
**Audience**: Developers deploying the chat widget

---

## Prerequisites

Before you begin, ensure you have:

- ✅ The RAG backend is running and accessible
- ✅ Docusaurus book is set up and running locally
- ✅ Access to modify `docusaurus.config.js`
- ✅ Basic knowledge of JavaScript and CSS

---

## Architecture Overview

```
┌──────────────────┐
│  Docusaurus Book │  ← User visits any page
│   (All Pages)    │
└────────┬─────────┘
         │
         │ Loads globally via docusaurus.config.js
         │
┌────────▼──────────────────────────────────────┐
│  ChatKit Widget (Floating Bottom-Right)       │
│  - CDN: chatkit.js                            │
│  - Init: /static/chatkit-init.js              │
│  - Style: /static/chatkit-styles.css          │
└────────┬──────────────────────────────────────┘
         │
         │ HTTP POST /ask
         │
┌────────▼─────────────────────────────┐
│  RAG Backend (FastAPI)               │
│  - Endpoint: http://localhost:8000   │
│  - Qdrant + Gemini                   │
└──────────────────────────────────────┘
```

---

## Step 1: Prepare Frontend Files

### 1.1 Create the Frontend Directory

Navigate to your project root and create the frontend folder:

```bash
cd /path/to/Physical_AI_Humanoid_Robotics_Book
mkdir -p frontend-chatkit
cd frontend-chatkit
```

### 1.2 Create `chatkit-init.js`

This file initializes the ChatKit widget with configuration.

**File**: `frontend-chatkit/chatkit-init.js`

```javascript
/**
 * ChatKit Widget Initialization
 * This script creates and configures the ChatKit floating widget
 * for the Docusaurus Physical AI & Humanoid Robotics book.
 */

// Configuration
const CHATKIT_CONFIG = {
  // Backend API endpoint (change for production)
  backendUrl: window.CHATKIT_BACKEND_URL || 'http://localhost:8000/ask',

  // Domain key for verification
  domainKey: 'docusaurus-physical-ai-book',

  // Theme configuration
  theme: {
    colorScheme: 'light',
    radius: 'round',
    color: {
      accent: {
        primary: '#3B82F6', // Blue accent color
        level: 2
      }
    }
  },

  // Start screen configuration
  startPrompts: [
    {
      label: 'What is Physical AI?',
      prompt: 'Can you explain what physical AI means and how it differs from traditional AI?',
      icon: 'robot'
    },
    {
      label: 'Humanoid Components',
      prompt: 'What are the main components and subsystems of a humanoid robot?',
      icon: 'settings'
    },
    {
      label: 'Control Systems',
      prompt: 'How do humanoid robot control systems work for bipedal locomotion?',
      icon: 'brain'
    },
    {
      label: 'Sensor Integration',
      prompt: 'How do humanoid robots integrate data from multiple sensors?',
      icon: 'eye'
    }
  ]
};

// Initialize ChatKit when DOM is ready
function initializeChatKit() {
  // Import ChatKit library
  import('https://cdn.platform.openai.com/deployments/chatkit/chatkit.js')
    .then(() => {
      console.log('[ChatKit] Library loaded successfully');

      // Create ChatKit element
      const chatkit = document.createElement('openai-chatkit');

      // Configure ChatKit options
      chatkit.setOptions({
        api: {
          url: CHATKIT_CONFIG.backendUrl,
          domainKey: CHATKIT_CONFIG.domainKey,

          // Custom fetch to transform request/response if needed
          fetch: async (url, options) => {
            try {
              // Add custom headers if needed
              const customOptions = {
                ...options,
                headers: {
                  ...options.headers,
                  'Content-Type': 'application/json'
                }
              };

              // Make request to backend
              const response = await fetch(url, customOptions);

              // Handle errors
              if (!response.ok) {
                const errorData = await response.json();
                console.error('[ChatKit] Backend error:', errorData);

                // Return error response in expected format
                return new Response(
                  JSON.stringify({
                    error: errorData.error || 'Failed to get response',
                    metadata: {
                      error_code: errorData.error_code,
                      request_id: errorData.request_id
                    }
                  }),
                  {
                    status: response.status,
                    headers: response.headers
                  }
                );
              }

              return response;
            } catch (error) {
              console.error('[ChatKit] Network error:', error);

              // Return network error response
              return new Response(
                JSON.stringify({
                  error: 'Unable to connect to the server. Please try again.',
                  metadata: { error_code: 'NETWORK_ERROR' }
                }),
                { status: 500 }
              );
            }
          }
        },

        theme: CHATKIT_CONFIG.theme,

        header: {
          enabled: true,
          title: {
            text: 'Book Assistant'
          }
        },

        history: {
          enabled: true,
          showDelete: true,
          showRename: true
        },

        startScreen: {
          greeting: 'Ask me anything about Physical AI & Humanoid Robotics!',
          prompts: CHATKIT_CONFIG.startPrompts
        },

        composer: {
          placeholder: 'Ask about the book content...'
        },

        threadItemActions: {
          feedback: true, // Allow user feedback
          retry: true // Allow retry on errors
        }
      });

      // Add ChatKit to page
      document.body.appendChild(chatkit);

      console.log('[ChatKit] Widget initialized successfully');
    })
    .catch(error => {
      console.error('[ChatKit] Failed to load:', error);
    });
}

// Wait for DOM to be ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeChatKit);
} else {
  initializeChatKit();
}
```

### 1.3 Create `chatkit-styles.css`

This file styles the widget positioning and responsive behavior.

**File**: `frontend-chatkit/chatkit-styles.css`

```css
/**
 * ChatKit Widget Styles
 * Handles positioning, sizing, and responsive behavior
 */

/* Main widget positioning */
openai-chatkit {
  /* Fixed positioning in bottom-right corner */
  position: fixed !important;
  bottom: 20px;
  right: 20px;
  z-index: 9999;

  /* Size */
  width: 360px;
  height: 600px;
  max-height: calc(100vh - 40px);

  /* Visual styling */
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  overflow: hidden;

  /* Smooth transitions */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Hover effect */
openai-chatkit:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

/* Tablet responsive (768px - 1024px) */
@media (max-width: 1024px) and (min-width: 769px) {
  openai-chatkit {
    width: 340px;
    height: 550px;
  }
}

/* Mobile responsive (max 768px) */
@media (max-width: 768px) {
  openai-chatkit {
    bottom: 10px;
    right: 10px;
    left: 10px;
    width: auto;
    height: 500px;
    max-height: calc(100vh - 20px);
  }
}

/* Very small screens (max 480px) */
@media (max-width: 480px) {
  openai-chatkit {
    bottom: 0;
    right: 0;
    left: 0;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0;
  }
}

/* Dark theme adjustments (if Docusaurus uses dark theme) */
[data-theme='dark'] openai-chatkit {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
}

/* Prevent widget from blocking important UI elements */
.docusaurus-highlight-code-line,
.theme-code-block,
.pagination-nav {
  position: relative;
  z-index: 1;
}

/* Ensure proper rendering on print */
@media print {
  openai-chatkit {
    display: none !important;
  }
}
```

### 1.4 Create `README.md`

**File**: `frontend-chatkit/README.md`

```markdown
# ChatKit Frontend Widget

This folder contains the ChatKit widget implementation for the Physical AI & Humanoid Robotics Docusaurus book.

## Files

- `chatkit-init.js` - Widget initialization and configuration
- `chatkit-styles.css` - Widget positioning and responsive styling
- `README.md` - This file

## Deployment

See `../specs/003-chatkit-frontend/quickstart.md` for complete deployment instructions.

## Configuration

Edit `chatkit-init.js` to customize:
- Backend URL (`backendUrl`)
- Theme colors and appearance
- Start screen prompts
- Widget behavior
```

---

## Step 2: Deploy to Docusaurus

### 2.1 Copy Files to Static Folder

Copy the frontend files to Docusaurus's `/static` directory:

```bash
# From project root
cp frontend-chatkit/chatkit-init.js static/
cp frontend-chatkit/chatkit-styles.css static/
```

**Verify**:
```bash
ls -la static/chatkit-*
# Should show:
# static/chatkit-init.js
# static/chatkit-styles.css
```

### 2.2 Update `docusaurus.config.js`

Add the ChatKit scripts and styles to your Docusaurus configuration.

**File**: `docusaurus.config.js`

```javascript
const config = {
  // ... existing config

  // Add ChatKit scripts
  scripts: [
    // ChatKit initialization
    {
      src: '/chatkit-init.js',
      type: 'module',
      async: true
    }
  ],

  // Add ChatKit styles
  stylesheets: [
    '/chatkit-styles.css'
  ],

  // ... rest of config
};

module.exports = config;
```

**Full example** with context:

```javascript
// @ts-check
// Note: type annotations allow type checking and IDE autocompletion

const {themes} = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A comprehensive guide to physical AI and humanoid robotics',
  favicon: 'img/favicon.ico',
  url: 'https://your-site.com',
  baseUrl: '/',
  organizationName: 'your-org',
  projectName: 'physical-ai-robotics-book',

  // ... other config options

  // ChatKit Integration
  scripts: [
    {
      src: '/chatkit-init.js',
      type: 'module',
      async: true
    }
  ],

  stylesheets: [
    '/chatkit-styles.css'
  ],

  // ... rest of config
};

module.exports = config;
```

---

## Step 3: Configure Backend URL

### Development (Local Testing)

The default configuration in `chatkit-init.js` uses:
```javascript
backendUrl: 'http://localhost:8000/ask'
```

Make sure your RAG backend is running:
```bash
cd backend
python main.py
# Should start on http://localhost:8000
```

### Production Deployment

For production, set the backend URL via environment variable or global config:

**Option 1: Global JavaScript Variable** (Recommended)

Add to your `docusaurus.config.js`:

```javascript
const config = {
  // ... other config

  headTags: [
    {
      tagName: 'script',
      innerHTML: `
        window.CHATKIT_BACKEND_URL = 'https://api.your-domain.com/ask';
      `
    }
  ],

  // ... rest of config
};
```

**Option 2: Modify `chatkit-init.js` Directly**

```javascript
const CHATKIT_CONFIG = {
  backendUrl: 'https://api.your-domain.com/ask',  // Production URL
  // ... rest of config
};
```

---

## Step 4: Test the Integration

### 4.1 Start the Development Server

```bash
cd /path/to/Physical_AI_Humanoid_Robotics_Book
npm start
```

### 4.2 Verify Widget Appears

1. Open browser to `http://localhost:3000`
2. Check **bottom-right corner** for the ChatKit widget
3. Widget should be visible on all pages

### 4.3 Test Functionality

**Test 1: Open Widget**
- Click the widget icon
- Widget should expand to show chat interface

**Test 2: Send Question**
- Type: "What is physical AI?"
- Click send or press Enter
- Should receive answer within 5 seconds

**Test 3: Error Handling**
- Stop the backend server
- Send a question
- Should display: "Unable to connect to the server"

**Test 4: Mobile Responsiveness**
- Open DevTools (F12)
- Switch to mobile view (360px width)
- Widget should resize appropriately

### 4.4 Check Browser Console

Open DevTools Console (F12) and look for:
```
[ChatKit] Library loaded successfully
[ChatKit] Widget initialized successfully
```

If you see errors, check:
- Backend server is running
- CORS is configured correctly
- No browser extensions blocking scripts

---

## Step 5: Customize (Optional)

### Change Theme Colors

Edit `chatkit-init.js`:

```javascript
theme: {
  colorScheme: 'dark',  // 'light' or 'dark'
  radius: 'round',      // 'sharp', 'round', or 'pill'
  color: {
    accent: {
      primary: '#10B981',  // Green instead of blue
      level: 2
    }
  }
}
```

### Add Custom Prompts

Edit `startPrompts` in `chatkit-init.js`:

```javascript
startPrompts: [
  {
    label: 'Your Custom Topic',
    prompt: 'Full question text here',
    icon: 'lightbulb'  // ChatKit icon name
  },
  // ... more prompts
]
```

### Adjust Widget Size

Edit `chatkit-styles.css`:

```css
openai-chatkit {
  width: 400px;   /* Wider widget */
  height: 700px;  /* Taller widget */
}
```

---

## Troubleshooting

### Widget Doesn't Appear

**Check 1**: Verify files are in `/static`
```bash
ls static/chatkit-*
```

**Check 2**: Check `docusaurus.config.js` includes scripts
```bash
grep -A 5 "scripts:" docusaurus.config.js
```

**Check 3**: Clear browser cache
- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

### Backend Connection Errors

**Check 1**: Backend is running
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","qdrant_connected":true}
```

**Check 2**: CORS configured
- Check browser DevTools Network tab
- Look for CORS errors in console

**Check 3**: Backend URL is correct
- Check `chatkit-init.js` line with `backendUrl`

### Widget Not Responsive on Mobile

**Check**: CSS file is loaded
- Open DevTools
- Go to Network tab
- Refresh page
- Look for `chatkit-styles.css` with status 200

---

## Production Deployment

### Checklist

- [ ] Update `backendUrl` to production API
- [ ] Configure backend CORS for production domain
- [ ] Test on production environment
- [ ] Verify HTTPS is used (not HTTP)
- [ ] Test on multiple devices and browsers
- [ ] Monitor backend logs for errors

### Security

- ✅ Use HTTPS for backend API
- ✅ Configure CORS to allow only your domain
- ✅ Don't expose API keys in frontend code
- ✅ Rate limit backend API to prevent abuse

---

## Next Steps

- 📖 See `data-model.md` for data structures
- 📋 See `contracts/backend-api.yaml` for API specification
- 📝 See `plan.md` for full architectural details

For implementation tasks, proceed to `/sp.tasks` command.
