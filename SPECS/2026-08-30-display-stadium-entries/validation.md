# Validation: Display Stadium Entries from Persistent Storage

Date: 2026-08-30

How we know this feature is complete and can be merged.

## Automated Checks

Run each command and confirm the expected result.

1. Syntax check the backend:
   ```
   python3 -m py_compile backend/app.py backend/data_layer.py
   ```
   → exits 0 with no output.

2. Endpoint — health:
   ```
   curl http://localhost:5000/api/health
   ```
   → `{"status": "ok"}`

3. Endpoint — all entries:
   ```
   curl http://localhost:5000/api/entries
   ```
   → JSON array of 22 objects, each with keys
   `id, person_id, gate, hour, bag`, matching the count in the database:
   ```
   sqlite3 stadium.db "SELECT COUNT(*) FROM stadium_entries;"   # → 22
   ```

4. Endpoint — gate filter:
   ```
   curl 'http://localhost:5000/api/entries?gate=C'
   ```
   → only objects whose `gate` equals `"C"`, and matches:
   ```
   sqlite3 stadium.db "SELECT COUNT(*) FROM stadium_entries WHERE gate='C';"
   ```

## Manual / Browser Checks (via Codio preview)

1. Open the dashboard. The entry table renders rows populated from the backend.
2. The status badge shows **Backend Connected**.
3. The entry count equals the number of rows in the table.
4. Change the gate filter to a specific gate → the table narrows to that gate.
5. Click **Refresh** → the table reloads with the current filter.
6. Stop and restart the server, refresh the dashboard → the same records remain
   (persistence across restart, per SPECS/MISSION.md).

## Boundary Enforcement Checks

1. `backend/app.py` does not contain `import sqlite3` and has no SQL strings in
   route handlers.
2. All SQL and the only `import sqlite3` live in `backend/data_layer.py`.
3. No SQL syntax appears anywhere in `frontend/`.

## Merge Criteria

Passes all automated checks **and** all manual/browser checks, and the user has
reviewed any differences between implementation and the specs.
