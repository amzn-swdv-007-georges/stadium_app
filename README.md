# Stadium Security Dashboard

A security dashboard for tracking stadium entry logs. Records are saved to
SQLite so they survive server crashes.

```

Frontend → Flask API → Data Layer → SQLite
```

## Stack

- **Frontend:** HTML, CSS, [HTMX](https://htmx.org/) (no hand-written JavaScript)
- **Backend:** Flask + REST API
- **Database:** SQLite
- All SQL lives in `backend/data_layer.py` — never in routes or the frontend.

## Structure

```text
stadium_app/
├── frontend/
│   └── index.html          ← HTMX-driven, no app.js
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
- **HTMX dashboard** — `GET /api/entries/table` returns the table as an HTML
  fragment that HTMX swaps into the page (no hand-written JavaScript).

  All interactions are HTMX attributes in `frontend/index.html`:
  - page load populates the table automatically
  - gate-filter change re-fetches with `?gate=X`
  - the Refresh button re-fetches with the current gate
  - connection status and entry count update via out-of-band swaps

## Run

Start the backend with:

```bash
cd stadium_app
python3 backend/app.py
```

Flask runs on port `5000` with `host='0.0.0.0'`.

## Dashboard

Open the running dashboard in the Codio preview browser:

**https://grandherman-nelsonvitamin-5000.codio.io/**

> The hostname is derived from `CODIO_BOX_DOMAIN`
> (`grandherman-nelsonvitamin.codio.io`) plus the server port `5000`. If your
> box domain changes, rebuild the URL as `https://<hostname>-5000.codio.io/`.

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

## Run the CLI

After syncing, launch the app from the command line:

```bash
cd stadium_app
python3 backend/app.py
```

Then open **https://grandherman-nelsonvitamin-5000.codio.io/** in the Codio
preview browser to view the dashboard.
