# Stadium Security System - Engineering Roadmap

This document serves as the living roadmap for the Stadium Security System, tracking project milestones, feature specifications, and implementation progress following Spec-Driven Development (SDD) principles.

---

## 🎯 Current Focus: Persistent Storage Layer (SQLite Integration)

We are transitioning the backend from in-memory stub data to a persistent SQLite database (`stadium.db`) managed via a dedicated Data Layer (`backend/data_layer.py`).

---

## 🗺️ Engineering Milestones

### Phase 1: Baseline Architecture & Mock Backend `[COMPLETED]`
- [x] Initial REST API route setup (Frontend <-> Backend)
- [x] Baseline entry log schema definition
- [x] Mock dataset for stadium gates and security alerts

### Phase 2: SQLite Data Layer & Persistence `[IN PROGRESS]`
- [x] **Spec Specification (SDD Workflow)**
  - [x] Requirements defined (`SPECS/DATA_LAYER/requirements.md`)
  - [x] Technical plan drafted (`SPECS/DATA_LAYER/plan.md`)
  - [x] Validation criteria set (`SPECS/DATA_LAYER/validation.md`)
  - [x] System Architecture updated (`SPECS/TECH.md`)
  - [x] Project Roadmap updated (`SPECS/ROADMAP.md`)
- [ ] **SQL Comprehension & Architectural Boundary Gate**
  - [ ] Peer review on basic SQL queries (`SELECT`, `WHERE`, `INSERT`)
  - [ ] Verification of zero-SQL leak into Frontend/Backend routes
- [ ] **Data Layer Implementation**
  - [ ] SQLite database initialization (`stadium.db`)
  - [ ] Implement `backend/data_layer.py` module
  - [ ] Create table schemas (`stadium_entries`, `security_alerts`, `gates`)
  - [ ] Refactor API routes to query data layer
- [ ] **Validation & Testing**
  - [ ] Execute automated validation test suite
  - [ ] Verify persistence across application restarts

### Phase 3: Frontend Integration & Real-time Gate Feeds `[UPCOMING]`
- [ ] Connect Frontend dashboard to active SQLite backend endpoints
- [ ] Implement real-time status indicators for Gates A-D
- [ ] Add entry filtering by gate, time window, and clearance level
- [ ] Handle database disconnect and reconnect states gracefully in UI

### Phase 4: Security Analytics & Audit Logging `[PLANNED]`
- [ ] Add aggregate queries for entry volume by hour
- [ ] Implement flagged re-entry alert triggering in data layer
- [ ] Export security audit logs to CSV/JSON format

---

## 📐 Architectural Boundary Rules

To maintain maintainability and clean separation of concerns:

1. **Frontend**: UI rendering and HTTP requests only. **Zero SQL knowledge.**
2. **Backend**: HTTP routing, request parsing, authentication. **No direct SQL strings.**
3. **Data Layer (`backend/data_layer.py`)**: SQLite connection management, parameterized SQL execution, data mapping.
4. **Database (`stadium.db`)**: On-disk SQLite database file storing relational tables.