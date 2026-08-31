# Feature: Display Stadium Entries from Persistent Storage

**Date:** 2026-08-31
**Roadmap item:** Phase 2 — Persistent Storage Layer (SQLite Integration), sub-item *"Data Layer Implementation"* / *"Refactor API routes to query data layer"*
**Branch:** `feature/display-stadium-entries`

---

## Goal

Display the stadium entry records that live in persistent SQLite storage (`stadium.db`) on the Security Command Dashboard, following the four-layer architecture in `SPECS/TECH.md` strictly.

## Scope

- **Frontend** (`stadium_app/frontend/index.html`): render stadium entries in a table.
- **Backend** (`backend/app.py`): expose `GET /api/entries` that reads from the data layer.
- **Data layer** (`backend/data_layer.py`): contains **all** database queries.
- **Database** (`stadium.db`): seeded with championship-game data.

## Non-Goals (out of scope for this item)

- Filtering by time window or clearance level (Phase 3).
- Real-time gate feeds / status indicators (Phase 3).
- Security analytics and audit log export (Phase 4).
- Creating the `security_alerts` and `gates` tables (separate roadmap step).

## Architecture & Boundary Rules (from `SPECS/TECH.md`)

1. **Frontend**: UI rendering and HTTP requests only. Zero SQL / schema knowledge. Uses JSON payloads.
2. **Backend (`app.py`)**: HTTP routing, request parsing, error formatting only. **Never imports `sqlite3` and never builds SQL.**
3. **Data layer (`data_layer.py`)**: the sole SQLite access point; parameterized queries with `?` placeholders; connection lifecycle management.
4. **Database (`stadium.db`)**: on-disk SQLite file.

### Enforcement points

- `backend/app.py` must not import `sqlite3`.
- All SQL lives in `backend/data_layer.py`, using parameterized placeholders (never string interpolation).
- No schema/column knowledge leaks into the frontend; the frontend consumes a JSON array of entry objects.

## Key Decisions

- **Schema:** Uses the seeded schema (`people` + `stadium_entries` with `person_id/gate/hour/bag`), matching `seed.sql` and `stadium.db`. This is the authoritative schema for the seeded dataset. (`SPECS/TECH.md`'s documented `stadium_entries` columns — `timestamp/badge_id/entry_status/security_level/notes` — describe a future/alternative schema and are NOT the seeded one.)
- **JSON shape:** `GET /api/entries` returns a JSON array of objects with keys `id`, `person_id`, `gate`, `hour`, `bag`.
- **Optional filter:** `GET /api/entries?gate=X` returns only rows for that gate, parameterized to prevent SQL injection.
- **Port:** Backend runs on port `5000` (`0.0.0.0` for Codio preview). Note: comments in `app.py`/`app.js` reference port 3000 but the `app.run` block uses 5000 — the running port (5000) is authoritative.

## Current State

The implementation for this item already exists in the working tree and satisfies the requirements above:

- `backend/data_layer.py` — `get_db_connection()`, `get_all_entries()`, `get_entries_by_gate(gate)` (SQLite-only file).
- `backend/app.py` — `GET /api/entries` route delegating to the data layer; no `sqlite3` import.
- `frontend/app.js` — `fetchEntries(gate)` and `renderTable(entries)`; wire-up on DOM load.
- `frontend/index.html` — renders the table body.

This spec documents and validates that implementation.
