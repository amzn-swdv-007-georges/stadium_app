# Plan: Display Stadium Entries from Persistent Storage

**Date:** 2026-08-31

Series of numbered task groups. Each group ends with a verification step. This is a Red/Green TDD repo, so automated checks should pass before and after the work.

## Task Group 1 — Validate the Persistent Data Layer

1. Confirm `stadium.db` exists at the repo root and contains seeded rows.
2. Confirm `backend/data_layer.py` is the only module that imports `sqlite3`.
3. Confirm `get_all_entries()` and `get_entries_by_gate(gate)` exist and use parameterized queries (`?` placeholders — no string interpolation).
4. Run a quick import/execution check: load `data_layer`, call `get_all_entries()` and `get_entries_by_gate('A')`, print row counts.

**Verify:** Both functions return lists of plain dicts; `get_entries_by_gate('A')` returns only gate A rows; queries are parameterized.

## Task Group 2 — Validate the Backend Route

5. Confirm `backend/app.py` does **not** import `sqlite3` and does not build SQL.
6. Confirm `GET /api/entries` reads the optional `?gate=` parameter and delegates to the data layer (`get_entries_by_gate` or `get_all_entries`).
7. Confirm `GET /api/entries` returns HTTP 200 JSON on success and `{"error": ...}` with HTTP 500 on failure.

**Verify:** Start the server; `curl /api/entries` returns seeded entries; `curl "/api/entries?gate=A"` returns only gate A rows.

## Task Group 3 — Validate the Frontend Rendering

8. Confirm `frontend/index.html` has a table whose `<tbody id="entries-body">` is populated dynamically.
9. Confirm `frontend/app.js` implements `fetchEntries(gate)` and `renderTable(entries)` showing `id, person_id, gate, hour, bag`.
10. Confirm event wiring: gate-filter `change`, refresh-button `click`, and initial load call `fetchEntries`.

**Verify:** Load the dashboard in a browser; the table shows entries from `stadium.db`; filtering by gate refreshes the list; empty state shows when no data.

## Task Group 4 — Architectural Boundary / Logging Review

11. Grep the frontend and backend for `sqlite3` and raw SQL strings — only `data_layer.py` may contain them.
12. Confirm `app.py` has no `import sqlite3`.
13. Confirm there is no logging mixed into business logic; requests log cleanly at the route boundary (per skill requirement for decorator-style logging, not inline business-logic + logging coupling).

**Verify:** `grep -r "sqlite3" frontend/ backend/ --include=*.py --include=*.js` returns only `backend/data_layer.py` matches.

## Task Group 5 — Persistence Across Restart

14. Restart the Flask server.
15. Re-fetch `/api/entries` and confirm the same seeded rows are returned (data persisted on disk, not in memory).

**Verify:** Same entry set returned after a full restart.
