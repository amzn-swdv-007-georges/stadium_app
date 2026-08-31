# Validation: Display Stadium Entries from Persistent Storage

**Date:** 2026-08-31

This feature is considered **validated and ready to merge** when all of the following checks pass.

## 1. Data Layer (SQLite-only boundary)

- [ ] `backend/data_layer.py` is the **only** file importing `sqlite3`.
- [ ] `get_all_entries()` returns all seeded rows from `stadium.db` as a list of dicts.
- [ ] `get_entries_by_gate(gate)` returns only rows matching that gate.
- [ ] Every SQL statement uses the `?` placeholder (parameterized); no string-interpolated SQL.

## 2. Backend Route

- [ ] `backend/app.py` does **not** import `sqlite3`.
- [ ] `GET /api/entries` returns HTTP 200 with a JSON array of entry objects (`id`, `person_id`, `gate`, `hour`, `bag`).
- [ ] `GET /api/entries?gate=X` returns a filtered subset with HTTP 200.
- [ ] On failure, the route returns `{"error": ...}` with HTTP 500.
- [ ] The route delegates all persistence to `data_layer` functions (no raw SQL in the route).

## 3. Frontend

- [ ] The dashboard table (`<tbody id="entries-body">`) renders entries returned by `/api/entries`.
- [ ] Each row shows `id`, `person_id`, `gate`, `hour`, `bag`.
- [ ] Gate filter, refresh button, and initial page load all trigger `fetchEntries()` and re-render.

## 4. Boundary Enforcement

- [ ] `grep -r "sqlite3" backend/ frontend/ --include=*.py --include=*.js` matches only `backend/data_layer.py`.
- [ ] No raw SQL strings exist anywhere outside `backend/data_layer.py`.

## 5. Persistence

- [ ] After restarting the server, `GET /api/entries` returns the same seeded rows (persisted on disk, not in memory).

## 6. Automated / Dev Runtime Checks

- [ ] Linting / type checks (if configured) pass; if none are configured, the manual `curl` + browser checks above are the verification.
- [ ] Server starts successfully via the project run command.

---

## Merge Gate

When all boxes above are checked, the feature spec (`requirements.md`, `plan.md`, `validation.md`) matches the implemented behavior. Any differences between the spec and the code found during validation must be surfaced and, if approved by the instructor, the specs updated *before* merge.
