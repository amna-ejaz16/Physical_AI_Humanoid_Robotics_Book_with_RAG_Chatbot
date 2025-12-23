---
id: 0002
title: ChatKit Frontend Planning
stage: plan
date: 2025-12-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-chatkit-frontend
branch: 003-chatkit-frontend
user: developer
command: /sp.plan
labels: ["chatkit", "frontend", "planning", "architecture", "openai", "docusaurus"]
links:
  spec: specs/003-chatkit-frontend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-chatkit-frontend/plan.md
  - specs/003-chatkit-frontend/research.md
  - specs/003-chatkit-frontend/data-model.md
  - specs/003-chatkit-frontend/quickstart.md
  - specs/003-chatkit-frontend/contracts/backend-api.yaml
  - CLAUDE.md
tests:
  - Constitution Check: All checks passed
  - Technical Context: Fully specified
  - Architecture diagrams created
  - ADR suggestions documented
---

## Prompt

Project: Docusaurus Book ChatKit Frontend Integration

Objective:
- Plan the frontend integration of ChatKit using Context7 MCP to connect with the existing RAG chatbot backend.
- Ensure the floating chat widget appears at the bottom-right corner of every page.
- Maintain a user-friendly interface.

Create:
1. Architecture Sketch:
   - Diagram showing interaction: User query → ChatKit widget → RAG backend → Response displayed.
   - Frontend folder `/frontend-chatkit` interfacing with Docusaurus book.

2. Section Structure:
   - Folder organization: HTML, CSS, JS, configuration files.
   - Component hierarchy for ChatKit widget.
   - Placement strategy for floating widget on all pages.

3. Research Approach:
   - Use research-concurrent approach: gather ChatKit and Context7 MCP integration details while planning.
   - Reference RAG backend API documentation.
   - Apply Context7 MCP best practices for embedding floating widgets.

4. Quality Validation:
   - Ensure ChatKit connects correctly to backend.
   - Floating icon visible on all pages.
   - Verify answers are relevant, accurate, and user-friendly.
   - Validate modularity and maintainability of `/frontend-chatkit`.

Decisions Needing Documentation:
- ChatKit integration method (inline script vs npm module).
- Widget placement strategy (bottom-right vs alternative corners).
- Connection method to RAG backend (REST API fetch vs Axios).
- Tradeoffs: modularity vs simplicity, UX vs resource usage.

Testing Strategy:
- Confirm widget visibility on all book pages.
- Test user queries for accuracy and relevance.
- Verify responsiveness and UI usability.
- Check modular folder structure for independent deployment.

Technical Details:
- Use research-concurrent approach (research while writing).
- Follow APA citation style for references.
- Organize plan by phases: Research → Foundation → Analysis → Synthesis.

## Response snapshot

Created comprehensive implementation plan for ChatKit Frontend Integration:

**Phase 0: Research (Completed)**
- Researched OpenAI ChatKit integration methods using Context7 MCP
- Evaluated CDN vs NPM installation strategies
- Investigated floating widget CSS positioning best practices
- Analyzed Docusaurus global script integration methods
- Documented all findings in `research.md` with source references

**Phase 1: Design (Completed)**
1. **Data Model** (`data-model.md`):
   - Defined Chat Message structure with metadata
   - Specified Chat Thread and Widget State management
   - Documented Backend Request/Response contracts
   - Created Error Response specifications with codes
   - Mapped data flow from user input through backend to display

2. **API Contracts** (`contracts/backend-api.yaml`):
   - OpenAPI 3.0.3 specification for RAG backend
   - POST /ask endpoint documentation
   - Error response schemas with all error codes
   - Health check endpoint specification
   - Request/response examples for all scenarios

3. **Quickstart Guide** (`quickstart.md`):
   - Step-by-step deployment instructions
   - File creation templates for chatkit-init.js and chatkit-styles.css
   - Docusaurus configuration examples
   - Testing procedures and troubleshooting
   - Production deployment checklist

4. **Implementation Plan** (`plan.md`):
   - Complete technical context (JavaScript ES6+, ChatKit CDN, Docusaurus)
   - Constitution check (all criteria passed)
   - High-level and component architecture diagrams
   - 8 technical design decisions with rationales
   - ADR suggestions for significant decisions
   - Testing strategy and success metrics
   - Risk analysis and mitigation strategies

**Key Architectural Decisions**:
1. OpenAI ChatKit (vanilla JS) over custom widget - production-ready features
2. CDN delivery with ESM modules - no build step required
3. Docusaurus `scripts` config for global integration - upgrade-safe
4. Existing `/ask` endpoint with custom fetch - no backend changes
5. CSS `position: fixed` bottom-right - industry standard pattern

**Technical Approach**:
- Modular `/frontend-chatkit/` folder with 3 files (init.js, styles.css, README.md)
- Deploy by copying to `/static/` and configuring `docusaurus.config.js`
- Connect to existing FastAPI backend at POST /ask endpoint
- ChatKit manages state via browser localStorage
- Responsive design with mobile-first CSS

**Deliverables Created**:
- ✅ research.md (8 decisions with research findings)
- ✅ data-model.md (7 entity types with validation rules)
- ✅ contracts/backend-api.yaml (complete OpenAPI spec)
- ✅ quickstart.md (comprehensive deployment guide)
- ✅ plan.md (full implementation plan with architecture)

Planning phase complete. Ready for `/sp.tasks` to generate implementation tasks.

## Outcome

- ✅ Impact: Comprehensive implementation plan created covering research, design, architecture, and deployment strategy for ChatKit frontend widget integration. All design decisions documented with rationales and alternatives.
- 🧪 Tests: Constitution check passed all criteria. Architecture validated against spec requirements. All technical decisions traceable to research findings.
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/backend-api.yaml. Updated CLAUDE.md with JavaScript/HTML/CSS technologies.
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks breakdown. Optionally run `/sp.adr` for architectural decision records.
- 🧠 Reflection: Planning successfully balanced thoroughness with pragmatism. Research-first approach identified OpenAI ChatKit as optimal solution, avoiding custom widget development. Modular structure aligns with spec requirements.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all phases executed
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all 6 criteria validated)
- Prompt variant (if applicable): research-concurrent-planning-v1
- Next experiment (smallest change to try): Proceed to task generation phase to validate that plan provides sufficient detail for implementation tasks
