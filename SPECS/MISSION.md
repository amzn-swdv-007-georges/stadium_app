# Mission

## Why this project exists

Detectives are investigating an incident at the stadium on the night of the
championship game. When the server crashed at halftime, entry records were
lost — including the records of two people at the center of the case.

This project builds a stadium security dashboard so investigators can track
entry logs reliably. **The data must survive a server crash.** No record that
was logged should ever be lost again.

## Who it is for

- **Detectives** — they use the dashboard to view and filter entry records.
- **Student developers** — people who are just learning to program build and
  maintain this app. Everything stays simple and easy to follow.

## What success looks like

An investigator can open the dashboard, see every entry log, and filter the
logs by gate. If the server stops and restarts, every record is still there.

## Non-negotiables

1. **Data survives crashes.** Entry logs are saved to disk in SQLite
   (`stadium.db`), not kept only in the app's memory. If the server restarts,
   the records must still be there.
2. **Beginner-friendly.** The code is simple, plain, and well commented so a
   student can read and extend it.
3. **Records are never silently lost.** Logging an entry must always persist.

## What is out of scope for now

- Logging people in or out. This dashboard is read-only for now: it displays
  entry records and filters them. It has not been asked to add or edit records
  yet.
- Real-time live feeds or push notifications.
- Security / authentication for who can view the dashboard.

---

For the technology and how the parts fit together, see `TECH.md`.
For where the project is heading, see `ROADMAP.md`.
