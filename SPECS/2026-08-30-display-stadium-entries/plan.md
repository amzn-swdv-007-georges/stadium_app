# Plan: Display Stadium Entries from Persistent Storage

Date: 2026-08-30

This is a Red/Green TDD repo per the feature-specification skill, so tests
should be written before feature code and run until green. The existing stubs
already contain an implementation; the plan below treats each task group as
both an implementation and a verification pass.

## Task Group 1 — Data Layer (`backend/data_layer.py`)

- [ ] `get_all_entries()`: `SELECT * FROM stadium_entries ORDER BY hour DESC`,
      return list of plain dicts. (implemented)
- [ ] `get_entries_by_gate(gate)`: parameterized `WHERE gate = ?` query, returns
      matching dicts. (implemented)
- [ ] Check: parameterized placeholders only, no f-string SQL.

## Task Group 2 — Backend API (`backend/app.py`)

- [ ] `GET /api/entries`: reads optional `?gate=`; if present calls
      `data_layer.get_entries_by_gate(gate)`, otherwise
      `data_layer.get_all_entries()`. Returns JSON 200; JSON `{"error": ...}`
      with 500 on failure. (implemented)
- [ ] `GET /api/health`: returns `{"status": "ok"}`. (implemented)
- [ ] Check: no `import sqlite3` in app.py; no SQL in route handlers.

## Task Group 3 — Frontend (`frontend/index.html`, `frontend/app.js`)

- [ ] `index.html`: table with headers `# | Person ID | Gate | Hour | Bag`,
      gate-filter dropdown (All/A/B/C/D), Refresh button, entry count, status
      badge, empty-state. (implemented)
- [ ] `app.js`:
  - `fetchEntries(gate)`: `GET /api/entries[?gate=X]`, parse JSON, call
    `renderTable`, update count + status badge; on error mark backend offline.
  - `renderTable(entries)`: clear rows; if empty show empty-state; else render
    one `<tr>` per entry with gate badge.
  - Event wiring: gate-filter change, Refresh click, initial load on
    `DOMContentLoaded`.

## Task Group 4 — Validation / Checks

- [ ] Start server from the command line:
      `cd stadium_app && python3 backend/app.py` (may also use `./run.sh`)
      and confirm it boots on port 5000.
- [ ] `curl localhost:5000/api/health` → `{"status":"ok"}`.
- [ ] `curl localhost:5000/api/entries` → 22 JSON objects.
- [ ] `curl 'localhost:5000/api/entries?gate=C'` → only gate-C entries.
- [ ] Cross-check returned rows against `sqlite3 stadium.db` count.
- [ ] Confirm persistence: restart server, records still present.
- [ ] Syntax check backend (`python3 -m py_compile backend/*.py`).

## Cleanup & Integration

- [ ] Surface any implementation-vs-spec differences to the user for approval.
- [ ] Update SPECS/ docs (TECH.md schema note, ROADMAP checkboxes) on approval.
- [ ] Commit on the feature branch.
