# Implementation Tasks: ChatKit Frontend Integration

**Feature**: 003-chatkit-frontend
**Branch**: `003-chatkit-frontend`
**Created**: 2025-12-19
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Overview

This document breaks down the ChatKit frontend widget implementation into specific, executable tasks organized by user story priority. Each task follows the format:

```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Legend**:
- `[P]` = Parallelizable (can run concurrently with other [P] tasks)
- `[US#]` = User Story number from spec.md
- Task IDs are sequential (T001, T002, etc.) in suggested execution order

---

## Task Summary

| Phase | User Story | Priority | Tasks | Parallelizable |
|-------|-----------|----------|-------|----------------|
| 1 | Setup | N/A | 3 | 2 |
| 2 | Foundational | N/A | 4 | 3 |
| 3 | US1: Reader Accesses Interactive Chat | P1 | 5 | 3 |
| 4 | US2: Reader Asks Questions & Receives Answers | P1 | 6 | 3 |
| 5 | US3: Reader Manages Chat Widget State | P2 | 3 | 2 |
| 6 | US4: Reader Handles Chat Errors Gracefully | P3 | 4 | 2 |
| 7 | Polish & Integration | N/A | 5 | 2 |
| **TOTAL** | | | **30** | **17** |

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
**Target**: User Story 1 + User Story 2 (P1 stories)
- Floating widget visible on all pages
- Basic Q&A functionality with backend
- Delivers core value: readers can ask questions

### Incremental Delivery
1. **Sprint 1**: Setup + Foundational + US1 (Widget appears and opens)
2. **Sprint 2**: US2 (Q&A functionality works)
3. **Sprint 3**: US3 (State management and history)
4. **Sprint 4**: US4 (Error handling) + Polish

### Independent Testing
Each user story phase includes independent test criteria so progress can be validated incrementally without waiting for full feature completion.

---

## Phase 1: Setup (Project Initialization)

**Goal**: Create project structure and initialize frontend folder

**Tasks**:

- [ ] T001 Create `/frontend-chatkit` directory at project root
- [ ] T002 [P] Create `/frontend-chatkit/README.md` with deployment reference
- [ ] T003 [P] Create `/frontend-chatkit/.gitignore` if needed (exclude node_modules, .env if added later)

**Acceptance**: `/frontend-chatkit/` folder exists with README.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Set up core widget infrastructure that all user stories depend on

**Independent Test**: ChatKit library loads without errors in browser console

**Tasks**:

- [ ] T004 [P] Create `frontend-chatkit/chatkit-init.js` with basic structure and imports
- [ ] T005 [P] Create `frontend-chatkit/chatkit-styles.css` with base widget positioning
- [ ] T006 [P] Add ChatKit CDN script import in `chatkit-init.js`
- [ ] T007 Configure backend API URL in `chatkit-init.js` (default: `http://localhost:8000/ask`)

**Files Created**:
- `frontend-chatkit/chatkit-init.js`
- `frontend-chatkit/chatkit-styles.css`

**Acceptance**:
- Both files exist and are syntactically valid
- ChatKit CDN import configured
- Backend URL configurable

---

## Phase 3: User Story 1 - Reader Accesses Interactive Chat (P1)

**Story Goal**: Widget appears as floating icon on all Docusaurus pages and opens when clicked

**Why Priority P1**: Core MVP - without visible widget, feature provides no value

**Independent Test**:
1. Start Docusaurus site (`npm start`)
2. Navigate to any page
3. Verify floating icon visible in bottom-right corner
4. Click icon → widget expands to show chat interface

**Tasks**:

- [ ] T008 [US1] Implement ChatKit widget creation in `chatkit-init.js`
- [ ] T009 [US1] Configure widget positioning CSS in `chatkit-styles.css` (fixed, bottom: 20px, right: 20px, z-index: 9999)
- [ ] T010 [P] [US1] Add responsive CSS for mobile devices in `chatkit-styles.css` (@media queries)
- [ ] T011 [P] [US1] Configure ChatKit theme in `chatkit-init.js` (colorScheme, radius, accent color)
- [ ] T012 [US1] Append ChatKit element to document.body in `chatkit-init.js`

**Files Modified**:
- `frontend-chatkit/chatkit-init.js`
- `frontend-chatkit/chatkit-styles.css`

**Acceptance Criteria (from spec.md)**:
- ✅ Floating chat icon appears in bottom-right corner on page load
- ✅ Icon is visible and clickable
- ✅ Clicking icon expands widget to show conversation interface
- ✅ Interface shows message input field and send button

**Parallel Execution Example**:
```bash
# Can work on these simultaneously (different concerns):
Developer A: T010 (Responsive CSS)
Developer B: T011 (Theme configuration)
```

---

## Phase 4: User Story 2 - Reader Asks Questions & Receives Answers (P1)

**Story Goal**: Users can send questions and receive relevant answers from RAG backend

**Why Priority P1**: Core functionality - delivers the main value proposition (Q&A)

**Independent Test**:
1. Open widget on any page
2. Type question: "What is physical AI?"
3. Click send or press Enter
4. Verify answer appears within 5 seconds
5. Answer should be relevant and from book content
6. Type follow-up question
7. Verify conversation context is maintained

**Tasks**:

- [ ] T013 [P] [US2] Configure API connection settings in `chatkit-init.js` (url, domainKey)
- [ ] T014 [P] [US2] Implement custom fetch function in `chatkit-init.js` for request/response transformation
- [ ] T015 [P] [US2] Configure composer (input placeholder) in `chatkit-init.js`
- [ ] T016 [US2] Set up backend error handling in custom fetch function
- [ ] T017 [US2] Configure start screen with greeting in `chatkit-init.js`
- [ ] T018 [US2] Add starter prompt suggestions in `chatkit-init.js` (4 prompts from quickstart.md)

**Files Modified**:
- `frontend-chatkit/chatkit-init.js`

**Acceptance Criteria (from spec.md)**:
- ✅ User can type question in input field
- ✅ Question appears in conversation thread when sent
- ✅ Response appears within 5 seconds
- ✅ Response content is relevant to question and derived from book
- ✅ Follow-up questions work (conversation context maintained)

**Parallel Execution Example**:
```bash
# Can work on these simultaneously:
Developer A: T013 (API config) + T014 (fetch function)
Developer B: T015 (Composer) + T017 (Start screen) + T018 (Prompts)
```

---

## Phase 5: User Story 3 - Reader Manages Chat Widget State (P2)

**Story Goal**: Users can minimize/maximize widget and conversation history persists

**Why Priority P2**: Important UX but not critical for MVP - users need control over visibility

**Independent Test**:
1. Open widget and have a conversation (2-3 exchanges)
2. Click minimize/close button
3. Verify widget collapses to icon
4. Click icon again
5. Verify widget reopens with full conversation history visible
6. Navigate to different page in book
7. Verify widget state (open/closed) is maintained

**Tasks**:

- [ ] T019 [P] [US3] Configure history panel in `chatkit-init.js` (enabled: true, showDelete: true, showRename: true)
- [ ] T020 [P] [US3] Configure header with title in `chatkit-init.js`
- [ ] T021 [US3] Test conversation persistence across page navigation

**Files Modified**:
- `frontend-chatkit/chatkit-init.js`

**Acceptance Criteria (from spec.md)**:
- ✅ Widget can be minimized/closed via button
- ✅ Widget reopens with previous conversation visible
- ✅ Widget state persists across page navigation
- ✅ History panel accessible and functional

**Parallel Execution Example**:
```bash
# Can work on these simultaneously:
Developer A: T019 (History config)
Developer B: T020 (Header config)
```

---

## Phase 6: User Story 4 - Reader Handles Chat Errors Gracefully (P3)

**Story Goal**: Clear error messages display when backend unavailable or no relevant content

**Why Priority P3**: Production-readiness, but happy path (P1-P2) must work first

**Independent Test**:
1. **Backend Offline Test**:
   - Stop backend server
   - Open widget and send question
   - Verify error message: "Unable to connect to the server"

2. **No Relevant Content Test**:
   - Ask question unrelated to book (e.g., "What's the weather?")
   - Verify helpful message appears

3. **Network Timeout Test**:
   - Simulate slow network
   - Verify timeout message after 10 seconds with retry option

**Tasks**:

- [ ] T022 [P] [US4] Add network error handling to custom fetch function in `chatkit-init.js`
- [ ] T023 [P] [US4] Add timeout handling (10 second limit) to custom fetch in `chatkit-init.js`
- [ ] T024 [US4] Configure thread item actions (retry: true) in `chatkit-init.js`
- [ ] T025 [US4] Test all error scenarios (backend offline, timeout, invalid response)

**Files Modified**:
- `frontend-chatkit/chatkit-init.js`

**Acceptance Criteria (from spec.md)**:
- ✅ Backend unavailable → "Unable to connect. Please try again in a moment."
- ✅ No relevant answer → "I couldn't find information about that in the book..."
- ✅ Network timeout → Timeout message with retry option
- ✅ All errors display user-friendly messages (not technical jargon)

**Parallel Execution Example**:
```bash
# Can work on these simultaneously:
Developer A: T022 (Network errors) + T023 (Timeouts)
Developer B: T024 (Retry config)
```

---

## Phase 7: Polish & Integration

**Goal**: Integrate widget with Docusaurus, optimize, and document

**Independent Test**:
1. Copy files to `/static/`
2. Update `docusaurus.config.js`
3. Build Docusaurus (`npm run build`)
4. Serve production build
5. Verify widget works on all pages
6. Check browser console for errors
7. Test on mobile device

**Tasks**:

- [ ] T026 [P] Copy `chatkit-init.js` to `/static/chatkit-init.js`
- [ ] T027 [P] Copy `chatkit-styles.css` to `/static/chatkit-styles.css`
- [ ] T028 Update `docusaurus.config.js` to load scripts and stylesheets globally
- [ ] T029 Test widget on multiple browsers (Chrome, Firefox, Safari, Edge)
- [ ] T030 Document deployment steps in `frontend-chatkit/README.md`

**Files Created/Modified**:
- `static/chatkit-init.js` (copied)
- `static/chatkit-styles.css` (copied)
- `docusaurus.config.js` (modified)
- `frontend-chatkit/README.md` (updated)

**Acceptance Criteria**:
- ✅ Widget loads on all Docusaurus pages
- ✅ No console errors
- ✅ Works in all major browsers
- ✅ Mobile responsive
- ✅ No performance impact on page load (<200ms)
- ✅ Deployment documented

**Parallel Execution Example**:
```bash
# Can work on these simultaneously:
Developer A: T026 + T027 (File copying)
Developer B: T029 (Browser testing)
```

---

## Task Dependencies

### Dependency Graph (User Story Completion Order)

```
Phase 1: Setup
    ↓
Phase 2: Foundational (MUST complete before any user story)
    ↓
    ├─→ Phase 3: US1 (P1) - Widget Appears
    │       ↓
    │   Phase 4: US2 (P1) - Q&A Works
    │       ↓
    │   ┌───┴───┐
    │   ↓       ↓
    ├─→ Phase 5: US3 (P2) - State Management
    │
    └─→ Phase 6: US4 (P3) - Error Handling
            │
            ↓
        Phase 7: Polish
```

### Story Independence

- **US1 → US2**: Sequential (need widget before Q&A)
- **US2 → US3**: Independent after US2 complete
- **US2 → US4**: Independent after US2 complete
- **US3 & US4**: Can be done in parallel after US2

### Task-Level Dependencies

**Blocking Tasks** (must complete before others):
- T001 (create folder) → all other tasks
- T004-T007 (foundational setup) → all US tasks
- T008-T012 (US1) → all subsequent US tasks

**Parallelizable Tasks** (marked with [P]):
- Total: 17 tasks can run in parallel
- Per Phase: See "Parallel Execution Example" sections above

---

## File Reference

### Files to Create

| File Path | Phase | Description |
|-----------|-------|-------------|
| `frontend-chatkit/README.md` | Setup | Deployment instructions |
| `frontend-chatkit/chatkit-init.js` | Foundational | Widget initialization and config |
| `frontend-chatkit/chatkit-styles.css` | Foundational | Widget positioning and styles |
| `static/chatkit-init.js` | Polish | Copy of init file |
| `static/chatkit-styles.css` | Polish | Copy of styles file |

### Files to Modify

| File Path | Phase | Modification |
|-----------|-------|--------------|
| `docusaurus.config.js` | Polish | Add scripts and stylesheets config |

### No Modifications Required

✅ All existing backend files remain unchanged
✅ All existing Docusaurus book content remains unchanged

---

## Testing Strategy

### Manual Test Scenarios

Refer to `plan.md` Section "Testing Strategy" for comprehensive test checklists:
- Widget Visibility (4 checks)
- Functionality (5 checks)
- Responsiveness (4 checks)
- Browser Compatibility (4 checks)
- Error Scenarios (4 checks)
- Integration Testing (8 checks)

### Per-Story Testing

Each user story phase includes **Independent Test** criteria that can be validated without waiting for the complete feature.

**Example**: After completing US1, you can verify the widget appears and opens without needing US2 (Q&A) to be implemented.

---

## Acceptance Testing

### Overall Feature Acceptance

From `spec.md` Success Criteria:

- [ ] **SC-001**: Readers can open chat widget and ask question within 3 seconds
- [ ] **SC-002**: 95% of questions receive responses within 5 seconds
- [ ] **SC-003**: Chat widget loads without impacting page load time by more than 200ms
- [ ] **SC-004**: Widget is visible and functional on 100% of book pages
- [ ] **SC-005**: Users can successfully complete a multi-turn conversation (3+ exchanges)
- [ ] **SC-006**: Chat widget maintains a mobile usability score of 90+
- [ ] **SC-007**: Error scenarios provide clear messaging and recovery options in 100% of cases
- [ ] **SC-008**: Widget deployed without modifying existing book or backend code

### MVP Acceptance (US1 + US2 only)

- [ ] Widget visible on all pages
- [ ] Widget opens on click
- [ ] User can send questions
- [ ] Backend responds with answers
- [ ] Answers are relevant to book content

---

## Execution Recommendations

### For Single Developer

**Week 1**:
- Days 1-2: Phase 1 (Setup) + Phase 2 (Foundational)
- Days 3-4: Phase 3 (US1 - Widget Appears)
- Day 5: Phase 4 (US2 - Q&A Works)

**Week 2**:
- Days 1-2: Phase 5 (US3 - State Management)
- Day 3: Phase 6 (US4 - Error Handling)
- Days 4-5: Phase 7 (Polish & Integration)

### For Team (Parallel Work)

**Sprint 1** (MVP - US1 + US2):
- Developer A: Setup + Foundational + US1 (widget structure)
- Developer B: US2 (backend integration + prompts)
- Merge and test together

**Sprint 2** (US3 + US4):
- Developer A: US3 (state management)
- Developer B: US4 (error handling)
- Both: Phase 7 (Polish)

---

## References

- **Spec**: [spec.md](./spec.md) - User stories and acceptance criteria
- **Plan**: [plan.md](./plan.md) - Architecture and technical decisions
- **Quickstart**: [quickstart.md](./quickstart.md) - Deployment guide
- **Data Model**: [data-model.md](./data-model.md) - Data structures
- **API Contract**: [contracts/backend-api.yaml](./contracts/backend-api.yaml) - Backend API spec

---

## Task Checklist Progress Tracker

**Setup**: 0/3 complete
**Foundational**: 0/4 complete
**US1 (P1)**: 0/5 complete
**US2 (P1)**: 0/6 complete
**US3 (P2)**: 0/3 complete
**US4 (P3)**: 0/4 complete
**Polish**: 0/5 complete

**Total Progress**: 0/30 tasks complete (0%)

**MVP Progress** (US1 + US2): 0/11 tasks complete (0%)

---

**Generated**: 2025-12-19
**Next Step**: Begin with Phase 1 (Setup) tasks T001-T003
**Ready for Implementation**: ✅ All tasks are specific and executable
