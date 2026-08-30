# Feature: Display Stadium Entries from Persistent Storage

Date: 2026-08-30
Branch: `feature/display-stadium-entries`

## Scope

Display the stadium entry logs from persistent storage (`stadium.db`) in a
readable table on the dashboard. This is read-only: it displays and filters
existing records. It does not add or edit records.

## Context

- The project constitution (SPECS/MISSION.md, SPECS/TECH.md, SPECS/ROADMAP.md)
  mandates SQLite persistence via a dedicated data layer.
- The data already exists in `stadium.db`, seeded by `seed.sql`. The seed uses
  this schema (which is the source of truth for this feature):

  ```
  people (id, name, phone)
  stadium_entries (id, person_id, gate, hour, bag)
  ```

- The seeded `stadium.db` contains 22 entry rows tied to 18 people.

## Running the App

Start the backend from the command line:

```
cd stadium_app
python3 backend/app.py
```

The server boots on port `5000` with `host='0.0.0.0'`. The dashboard is
available in the Codio preview browser at:

```
https://grandherman-nelsonvitamin-5000.codio.io/
```

## Requirements (Functional)

1. **Backend endpoint** — `GET /api/entries` returns all stadium entry records
   as a JSON array, each entry with the fields: `id`, `person_id`, `gate`,
   `hour`, `bag`.
2. **Gate filter** — `GET /api/entries?gate=A` returns only entries for that
   gate. Parameter value must be passed as a bound query parameter (no string
   interpolation).
3. **Frontend table** — `frontend/index.html` renders the returned entries in a
   table with columns: `#`, `Person ID`, `Gate`, `Hour`, `Bag`. Gate values are
   shown as coloured badges.
4. **Frontend load & refresh** — the table populates automatically on page load,
   on gate-filter change, and on clicking the Refresh button.
5. **Entry count & status** — the UI shows the number of entries and a
   Backend-Connected / Backend-Offline status badge.

## Non-Functional Requirements

1. **Architectural boundaries** (per SPECS/TECH.md) are strictly respected:
   - Frontend: UI + HTTP requests only. Zero SQL knowledge.
   - Backend (`backend/app.py`): route handling only. Must NOT import `sqlite3`
     or write SQL.
   - Data layer (`backend/data_layer.py`): the sole owner of SQL and DB access.
   - Database (`stadium.db`): on-disk SQLite, never touched directly by routes.
2. **SQL injection prevention**: all queries use parameterized placeholders.
3. **Beginner-friendly**: plain, well-commented code a student can read.

## Decisions

- Persistence via SQLite wins over the generic "no persistence" guideline in the
  feature-specification skill, because the user's explicit request and the
  project constitution require `stadium.db`.
- The seed.sql schema (`person_id`, `gate`, `hour`, `bag`) governs, not the
  schema printed in TECH.md (which describes `badge_id`/`timestamp`/etc. that
  does not exist in the seeded DB).
