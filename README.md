# Stadium Security Dashboard

A security dashboard for tracking stadium entry logs. Records are saved to
SQLite so they survive server crashes.

```

Frontend → Flask API → Data Layer → SQLite
```

## Stack

- **Frontend:** HTML, CSS, JavaScript (no frameworks)
- **Backend:** Flask + REST API
- **Database:** SQLite
- All SQL lives in `backend/data_layer.py` — never in routes or the frontend.

## Structure

```text
stadium_app/
├── frontend/
│   ├── index.html
│   └── app.js
├── backend/
│   ├── app.py
│   └── data_layer.py
├── SPECS/            ← project constitution
│   ├── MISSION.md
│   ├── TECH.md
│   └── ROADMAP.md
├── stadium.db
└── README.md
```

## Features

- **View entries** — `GET /api/entries`
- **Filter by gate** — `GET /api/entries?gate=A` (gates A–D)

## Run

```bash
python3 backend/app.py
```

Then open the dashboard URL in the Codio preview browser. Flask runs on
port `5000` with `host='0.0.0.0'`.

## Verify persistence

1. Start the server, confirm entries load.
2. Stop the server, restart it, refresh the dashboard.
3. The same records are still there — they live in `stadium.db`, not memory.

## Sync with GitHub

```bash
# authenticate once
gh auth login

# create your own repo and push
gh repo create stadium_app --source=. --remote=origin --push
git add .
git commit -m "Build stadium security dashboard"
git push
```
