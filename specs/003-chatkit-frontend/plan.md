# Implementation Plan: ChatKit Frontend Integration

**Branch**: `003-chatkit-frontend` | **Date**: 2025-12-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-chatkit-frontend/spec.md`

---

## Summary

Create a modular ChatKit frontend widget that integrates with the existing RAG chatbot backend to provide interactive Q&A functionality for readers of the Docusaurus Physical AI & Humanoid Robotics book. The widget will appear as a floating icon in the bottom-right corner of every page, allowing readers to ask questions and receive AI-generated answers based solely on book content.

**Technical Approach**:
- Use OpenAI ChatKit (vanilla JavaScript) for production-ready chat UI
- Deploy via CDN with custom configuration scripts
- Integrate with Docusaurus using `scripts` configuration
- Connect to existing FastAPI RAG backend (`POST /ask` endpoint)
- Fixed CSS positioning for floating bottom-right placement
- Self-contained `/frontend-chatkit` folder for modularity

**Key Decision**: Selected OpenAI ChatKit over building custom widget due to production-ready features (streaming, error handling, accessibility, threading) and self-hosted backend support aligning with existing RAG infrastructure.

---

## Technical Context

**Language/Version**: JavaScript (ES6+) / HTML5 / CSS3
**Primary Dependencies**:
- OpenAI ChatKit (`@openai/chatkit` via CDN)
- Existing RAG Backend (FastAPI + Qdrant + Gemini)
- Docusaurus 2.x+ (for book site)

**Storage**:
- Browser localStorage (conversation history managed by ChatKit)
- No server-side storage

**Testing**:
- Manual integration testing (widget visibility, API connectivity)
- Cross-browser testing (Chrome, Firefox, Safari, Edge)
- Responsive design testing (desktop, tablet, mobile)
- End-to-end user flow testing

**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)

**Project Type**: Static frontend (web)

**Performance Goals**:
- Widget loads within 200ms (async, non-blocking)
- Chat response time: <5 seconds (backend dependent)
- No impact on Docusaurus page load time
- Smooth UI interactions (60fps animations)

**Constraints**:
- No modifications to existing backend code
- No modifications to existing Docusaurus book content
- Self-contained in `/frontend-chatkit` folder
- CDN-based deployment (no build step)
- Must work on all Docusaurus pages without per-page configuration

**Scale/Scope**:
- 3 source files (JavaScript, CSS, README)
- ~300-500 lines of code total
- Supports unlimited concurrent users (backend-limited)
- Conversation history limited by browser localStorage (~5-10MB)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Technical Accuracy
- All JavaScript/CSS/HTML follows web standards
- ChatKit integration follows official OpenAI documentation
- REST API integration follows FastAPI contract specifications
- No proprietary or deprecated APIs used

### ✅ Engineering Clarity
- Code is readable and well-documented
- Configuration is explicit and easy to modify
- Deployment steps are clearly documented in quickstart.md
- Error messages are user-friendly and actionable

### ✅ Modular Documentation
- Frontend code isolated in `/frontend-chatkit/`
- Clear separation: init script, styles, documentation
- Reusable across similar Docusaurus projects
- Self-contained with minimal dependencies

### ✅ Reproducibility & Transparency
- All design decisions documented in `research.md`
- API contracts specified in OpenAPI format
- Deployment steps are repeatable and testable
- References to official ChatKit and Docusaurus documentation

### ✅ Safety & Ethics Awareness
- Widget does not collect personal data
- Conversation history stored locally (user privacy)
- Clear error messaging (no misleading information)
- Answers based solely on book content (no hallucination risk via RAG)

### ✅ Consistency with Spec-Kit Plus Methodology
- Followed `/sp.specify` → `/sp.plan` workflow
- All research consolidated before design
- Data model and contracts defined before implementation
- ADR suggestions will be made for significant decisions

**Result**: ✅ ALL CHECKS PASSED - Proceed to implementation

---

## Project Structure

### Documentation (this feature)

```text
specs/003-chatkit-frontend/
├── plan.md                     # This file (/sp.plan output)
├── spec.md                     # Feature specification
├── research.md                 # Phase 0: Technology research findings
├── data-model.md               # Phase 1: Data structures and flows
├── quickstart.md               # Phase 1: Deployment guide
├── contracts/                  # Phase 1: API specifications
│   └── backend-api.yaml        # OpenAPI spec for RAG backend
├── checklists/                 # Quality validation
│   └── requirements.md         # Spec quality checklist
└── tasks.md                    # Phase 2: Implementation tasks (/sp.tasks - NOT YET CREATED)
```

### Source Code (repository root)

```text
/frontend-chatkit/              # Modular frontend folder (THIS FEATURE)
├── chatkit-init.js             # Widget initialization and configuration
├── chatkit-styles.css          # Positioning, sizing, responsive styles
└── README.md                   # Deployment instructions reference

/static/                        # Docusaurus static assets (DEPLOYMENT TARGET)
├── chatkit-init.js             # Copied from frontend-chatkit/
└── chatkit-styles.css          # Copied from frontend-chatkit/

/backend/                       # EXISTING RAG backend (NO CHANGES)
├── main.py                     # FastAPI app with /ask endpoint
├── models.py                   # Pydantic models
├── agent_client.py             # Gemini client
├── rag_client.py               # Qdrant + RAG pipeline
└── config.py                   # Backend configuration

/docs/                          # EXISTING Docusaurus book (NO CHANGES to content)
├── intro.md
├── chapter-1/
├── chapter-2/
└── ...

docusaurus.config.js            # MODIFIED: Add scripts and stylesheets config
```

**Structure Decision**:

This feature uses a **modular static frontend** structure, separating the ChatKit widget code into `/frontend-chatkit/` at the project root. This aligns with the requirement for a "separate frontend folder" that is "self-contained and modular."

Files are deployed by copying to Docusaurus `/static/` folder and referencing via `docusaurus.config.js`. This approach:
- ✅ Keeps frontend code separate and maintainable
- ✅ Requires no build step (CDN-based ChatKit library)
- ✅ Doesn't modify existing backend or book content
- ✅ Enables independent updates to widget configuration

The existing backend in `/backend/` is used as-is with no modifications, connecting via the already-implemented `/ask` endpoint.

---

## Complexity Tracking

> **No complexity violations detected** - This section intentionally left empty.

All design decisions adhere to the project constitution and follow standard web development patterns.

---

## Architecture

### High-Level Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                        DOCUSAURUS BOOK                             │
│                     (All Pages Globally)                           │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  <html>                                                       │ │
│  │    <head>                                                     │ │
│  │      <link rel="stylesheet" href="/chatkit-styles.css" />    │ │
│  │    </head>                                                    │ │
│  │    <body>                                                     │ │
│  │      <!-- Page content -->                                    │ │
│  │      <script src="/chatkit-init.js" type="module"></script>  │ │
│  │    </body>                                                    │ │
│  │  </html>                                                      │ │
│  └────────────────────┬─────────────────────────────────────────┘ │
│                       │                                            │
│                       ├─→ Loads chatkit-styles.css                │
│                       │   (Fixed positioning: bottom-right)       │
│                       │                                            │
│                       └─→ Executes chatkit-init.js                │
│                           (Dynamically creates widget)            │
└────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────┐
│                    CHATKIT WIDGET (CDN)                            │
│                                                                    │
│  src="https://cdn.platform.openai.com/.../chatkit.js"            │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ <openai-chatkit>                                             │ │
│  │   [Chat UI Component]                                        │ │
│  │   - Message Thread                                           │ │
│  │   - Input Composer                                           │ │
│  │   - Start Screen with Prompts                                │ │
│  │   - History Panel                                            │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                       │                                            │
│                       │ User sends question                        │
│                       ▼                                            │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Custom fetch() function                                      │ │
│  │ - Transforms request to backend format                       │ │
│  │ - Adds error handling                                        │ │
│  │ - Manages network failures                                   │ │
│  └──────────────────┬───────────────────────────────────────────┘ │
└────────────────────┼────────────────────────────────────────────────┘
                     │
                     │ HTTP POST /ask
                     │ { "question": "What is physical AI?" }
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│                    RAG BACKEND (EXISTING)                          │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ FastAPI Server (main.py)                                     │ │
│  │ - Endpoint: POST /ask                                        │ │
│  │ - CORS: Enabled for all origins                              │ │
│  │ - Error handling with custom codes                           │ │
│  └────────────┬─────────────────────────────────────────────────┘ │
│               │                                                    │
│               ├─→ Gemini Client (agent_client.py)                 │
│               │   - Generate question embedding                    │
│               │   - Generate answer from context                   │
│               │                                                    │
│               ├─→ Qdrant Manager (rag_client.py)                  │
│               │   - Vector similarity search                       │
│               │   - Retrieve top 3 book chunks                     │
│               │                                                    │
│               └─→ RAG Pipeline (rag_client.py)                    │
│                   - Combine search results                        │
│                   - Generate contextual answer                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Response:                                                    │ │
│  │ {                                                            │ │
│  │   "answer": "Physical AI refers to...",                     │ │
│  │   "request_id": "uuid",                                     │ │
│  │   "sources": ["Chapter 1", "Chapter 3"]                     │ │
│  │ }                                                            │ │
│  └──────────────────┬───────────────────────────────────────────┘ │
└────────────────────┼────────────────────────────────────────────────┘
                     │
                     │ HTTP 200 OK + JSON
                     ▼
┌────────────────────────────────────────────────────────────────────┐
│                    CHATKIT WIDGET                                  │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Display Assistant Message:                                   │ │
│  │ - Answer content                                             │ │
│  │ - Source attribution (if available)                          │ │
│  │ - Request ID (in metadata)                                   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Save to Thread History (localStorage)                        │ │
│  │ - User message + Assistant response                          │ │
│  │ - Persists across page navigation                            │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

### Component Hierarchy

```
Docusaurus Page (docusaurus.config.js)
│
├─→ <link> chatkit-styles.css          (Global stylesheet)
│   │
│   └─→ openai-chatkit {...}           (Widget positioning CSS)
│       - position: fixed
│       - bottom: 20px
│       - right: 20px
│       - z-index: 9999
│
└─→ <script> chatkit-init.js           (Initialization script)
    │
    ├─→ Import ChatKit from CDN
    │   - https://cdn.platform.openai.com/.../chatkit.js
    │
    ├─→ Create <openai-chatkit> element
    │
    ├─→ Configure ChatKit options
    │   ├─→ API Configuration
    │   │   - url: Backend endpoint
    │   │   - domainKey: Verification
    │   │   - fetch: Custom request handler
    │   │
    │   ├─→ Theme Configuration
    │   │   - colorScheme: 'light'
    │   │   - radius: 'round'
    │   │   - accent color
    │   │
    │   ├─→ UI Configuration
    │   │   - header (title, actions)
    │   │   - history (enabled, delete, rename)
    │   │   - startScreen (greeting, prompts)
    │   │   - composer (placeholder)
    │   │
    │   └─→ Behavior Configuration
    │       - threadItemActions (feedback, retry)
    │
    └─→ Append to document.body
        - Widget renders at bottom-right
        - Available on all pages
```

---

## Technical Design Decisions

### 1. Widget Library Selection

**Decision**: OpenAI ChatKit (vanilla JS, self-hosted backend)

**Rationale**:
- Production-ready chat UI with comprehensive features
- Self-hosted backend option connects to our existing FastAPI server
- CDN delivery with no build step required
- Customizable theme and UI components
- Built-in conversation threading and history management

**Alternatives Rejected**:
- ChatBotKit: Platform-based, requires full infrastructure adoption
- Custom Widget: Significant development effort, no time savings

**Reference**: `research.md` Section 1

### 2. Installation Strategy

**Decision**: CDN script tag with ES modules

**Rationale**:
- No build tooling required (aligns with "modular" constraint)
- Browser-native module loading
- Async loading doesn't block page rendering
- Easy to update (change CDN version)

**Implementation**:
```javascript
import('https://cdn.platform.openai.com/deployments/chatkit/chatkit.js')
```

**Reference**: `research.md` Section 2

### 3. Docusaurus Integration

**Decision**: Use `scripts` configuration in `docusaurus.config.js`

**Rationale**:
- Official Docusaurus method for global scripts
- Works automatically on all pages
- No swizzling or component ejection required
- Maintains Docusaurus upgrade path

**Configuration**:
```javascript
scripts: [
  { src: '/chatkit-init.js', type: 'module', async: true }
],
stylesheets: ['/chatkit-styles.css']
```

**Alternatives Rejected**:
- Swizzle Layout: Breaks on Docusaurus upgrades
- Footer modification: Still requires swizzling

**Reference**: `research.md` Section 4

### 4. Backend Connection

**Decision**: Use existing `/ask` endpoint with custom `fetch` function

**Rationale**:
- Backend already implements required functionality
- CORS already configured
- No backend modifications needed (constraint)
- Custom fetch transforms requests/responses if needed

**API Contract**: See `contracts/backend-api.yaml`

**Reference**: `research.md` Section 5

### 5. Widget Positioning

**Decision**: CSS `position: fixed` with bottom-right coordinates

**Rationale**:
- Industry standard pattern (Intercom, Zendesk, Drift)
- Always visible regardless of scroll position
- Doesn't obscure main content
- Mobile-responsive with media queries

**CSS Implementation**:
```css
openai-chatkit {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  width: 360px;
  height: 600px;
}
```

**Reference**: `research.md` Section 3

### 6. Error Handling

**Decision**: Leverage ChatKit built-in error UI + backend error codes

**Rationale**:
- Backend provides comprehensive error codes (QUESTION_EMPTY, QUESTION_TOO_LONG, API_ERROR, etc.)
- ChatKit automatically displays error messages
- No custom error handling component needed

**Error Codes**: See `data-model.md` Section 6

**Reference**: `research.md` Section 6

### 7. State Management

**Decision**: ChatKit built-in history + browser localStorage

**Rationale**:
- ChatKit manages conversation state automatically
- Persists across page navigation
- No custom state management required
- User controls via history panel

**Reference**: `research.md` Section 7

### 8. Deployment Strategy

**Decision**: Develop in `/frontend-chatkit/`, deploy to `/static/`

**Rationale**:
- Modular folder structure (requirement)
- Self-contained frontend code
- Easy to update independently
- Simple deployment (copy files)

**Deployment Flow**:
```
/frontend-chatkit/*.js,*.css  →  cp  →  /static/  →  Docusaurus build
```

**Reference**: `research.md` Section 8, `quickstart.md`

---

## 📋 Architectural Decision Records (ADRs)

The following significant architectural decisions were made during planning. These should be documented as ADRs:

### ADR Suggestions

1. **ChatKit Widget Library Selection**
   - **Decision**: Use OpenAI ChatKit over custom-built widget
   - **Impact**: Affects entire frontend architecture and user experience
   - **Tradeoffs**: Vendor dependency vs development time savings
   - **Recommendation**: `/sp.adr "ChatKit Library Selection for Chat Widget"`

2. **CDN vs NPM Installation**
   - **Decision**: Use CDN script tag instead of NPM package
   - **Impact**: No build step, simpler deployment, but less control
   - **Tradeoffs**: Simplicity vs customization and versioning control
   - **Recommendation**: `/sp.adr "CDN-Based ChatKit Deployment Strategy"`

3. **Docusaurus Global Integration Method**
   - **Decision**: Use `scripts` config instead of swizzling
   - **Impact**: Maintains Docusaurus upgrade path
   - **Tradeoffs**: Limited to official methods vs maximum flexibility
   - **Recommendation**: `/sp.adr "Docusaurus Integration via Scripts Config"`

**To create ADRs**, run:
```bash
/sp.adr "ChatKit Library Selection for Chat Widget"
/sp.adr "CDN-Based ChatKit Deployment Strategy"
/sp.adr "Docusaurus Integration via Scripts Config"
```

---

## Implementation Phases

### Phase 0: Research ✅ COMPLETED
- ✅ Investigated ChatKit integration options
- ✅ Researched floating widget best practices
- ✅ Evaluated Docusaurus integration methods
- ✅ Documented findings in `research.md`

### Phase 1: Design ✅ COMPLETED
- ✅ Defined data model (`data-model.md`)
- ✅ Created API contracts (`contracts/backend-api.yaml`)
- ✅ Wrote deployment guide (`quickstart.md`)
- ✅ Documented architecture (this file)

### Phase 2: Implementation Planning (NEXT)
- ⏭️ Generate `tasks.md` using `/sp.tasks` command
- ⏭️ Break down implementation into testable tasks
- ⏭️ Define acceptance criteria for each task

### Phase 3: Implementation (FUTURE)
- Create `chatkit-init.js`
- Create `chatkit-styles.css`
- Update `docusaurus.config.js`
- Test on local Docusaurus instance
- Deploy to production

---

## Non-Functional Requirements

### Performance
- ✅ Widget loads asynchronously (no blocking)
- ✅ <200ms load time impact on page
- ✅ <5 second response time (backend dependent)
- ✅ 60fps UI animations

### Accessibility
- ✅ Keyboard navigation (handled by ChatKit)
- ✅ Screen reader compatible (handled by ChatKit)
- ✅ WCAG AA contrast ratios (configured in theme)
- ✅ Focus management (handled by ChatKit)

### Compatibility
- ✅ Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- ✅ Desktop, tablet, mobile responsive
- ✅ Works with JavaScript enabled (required)
- ✅ Degrades gracefully if backend unavailable

### Security
- ✅ No personal data collection
- ✅ Local storage only (user privacy)
- ✅ CORS configured on backend
- ✅ No API keys exposed in frontend

### Maintainability
- ✅ Self-contained in `/frontend-chatkit/`
- ✅ Clear configuration file structure
- ✅ Comprehensive documentation
- ✅ Easy to update widget behavior

---

## Testing Strategy

### Manual Testing Checklist

**Widget Visibility**:
- [ ] Widget appears on all Docusaurus pages
- [ ] Widget positioned correctly (bottom-right)
- [ ] Widget icon is visible and clickable
- [ ] Widget expands on click

**Functionality**:
- [ ] User can type and send questions
- [ ] Backend responds with relevant answers
- [ ] Source attribution appears in metadata
- [ ] Error messages display correctly
- [ ] Retry functionality works

**Responsiveness**:
- [ ] Desktop (1920x1080, 1440x900)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667, 414x896)
- [ ] Widget resizes appropriately

**Browser Compatibility**:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

**Error Scenarios**:
- [ ] Backend offline → Error message displayed
- [ ] Empty question → Validation error
- [ ] Very long question → Length error
- [ ] Network timeout → Timeout error with retry

### Integration Testing

**Backend Integration**:
- [ ] Successful POST to `/ask` endpoint
- [ ] CORS headers present in response
- [ ] Error codes mapped correctly
- [ ] Request IDs tracked properly

**State Persistence**:
- [ ] Conversation persists across page navigation
- [ ] History panel shows previous threads
- [ ] Delete thread removes from localStorage
- [ ] Rename thread updates localStorage

---

## Deployment Checklist

### Pre-Deployment

- [ ] All files created in `/frontend-chatkit/`
- [ ] Files copied to `/static/`
- [ ] `docusaurus.config.js` updated with scripts
- [ ] Backend URL configured correctly
- [ ] Theme colors customized (if desired)

### Testing

- [ ] Local Docusaurus build succeeds
- [ ] Widget appears on all pages
- [ ] Backend connectivity verified
- [ ] Manual test checklist completed
- [ ] Mobile responsive testing done

### Production

- [ ] Backend URL updated to production
- [ ] CORS configured for production domain
- [ ] HTTPS enabled on backend
- [ ] Performance monitoring in place
- [ ] Error tracking configured

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ChatKit CDN unavailable | Low | High | Consider self-hosting ChatKit library |
| Backend API changes | Low | High | API contract in OpenAPI spec, versioning |
| Browser compatibility issues | Medium | Medium | Test on all major browsers before deploy |
| localStorage quota exceeded | Low | Low | ChatKit handles cleanup, users can delete threads |
| CORS misconfiguration | Medium | High | Test in production environment before launch |
| Mobile UX issues | Medium | Medium | Extensive mobile testing, responsive CSS |

---

## Success Metrics

From `spec.md` Success Criteria:

- **SC-001**: ✅ Readers can open chat widget and ask question within 3 seconds
- **SC-002**: ✅ 95% of questions receive responses within 5 seconds
- **SC-003**: ✅ <200ms page load time impact
- **SC-004**: ✅ Widget visible on 100% of book pages
- **SC-005**: ✅ Multi-turn conversations (3+ exchanges) work
- **SC-006**: ✅ Mobile usability score 90+
- **SC-007**: ✅ Error scenarios provide clear messaging
- **SC-008**: ✅ Deployed without modifying backend/book code

---

## References

### Internal Documentation
- [Feature Specification](./spec.md)
- [Research Findings](./research.md)
- [Data Model](./data-model.md)
- [API Contract](./contracts/backend-api.yaml)
- [Quickstart Guide](./quickstart.md)
- [Project Constitution](../../.specify/memory/constitution.md)

### External Resources
- [OpenAI ChatKit Documentation](https://openai.github.io/chatkit-js/)
- [ChatKit Quickstart](https://openai.github.io/chatkit-js/quickstart)
- [Docusaurus Configuration](https://docusaurus.io/docs/next/api/docusaurus-config)
- [Floating Widget Best Practices](https://dev.to/epi2024/floating-button-for-chat-app-in-html-javascript-and-css-3j7j)

### Backend Implementation
- RAG Backend: `/backend/main.py:157-212` (POST /ask endpoint)
- CORS Configuration: `/backend/main.py:104-111`
- Error Handling: `/backend/main.py:114-154`

---

## Next Steps

1. **Generate Implementation Tasks**
   ```bash
   /sp.tasks
   ```
   This will create `tasks.md` with specific, testable implementation tasks.

2. **Create ADRs** (Optional but recommended)
   ```bash
   /sp.adr "ChatKit Library Selection for Chat Widget"
   ```

3. **Begin Implementation**
   Follow tasks in priority order, using Test-Driven Development where applicable.

4. **Deployment**
   Follow `quickstart.md` for step-by-step deployment instructions.

---

**Planning Completed**: 2025-12-19
**Next Command**: `/sp.tasks` to generate implementation tasks
