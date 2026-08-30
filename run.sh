#!/bin/bash
# Starts the Stadium Security backend on port 5000.
# Kills any process already holding port 5000 before starting.
# Run from any directory — the script always resolves its own location.

# Find and kill any PIDs currently bound to port 5000
PIDS=$(ss -tlnp sport = :5000 2>/dev/null | grep -oP 'pid=\K[0-9]+' | sort -u)
if [ -n "$PIDS" ]; then
    echo "Freeing port 5000 (PIDs: $PIDS)…"
    kill -9 $PIDS 2>/dev/null
    sleep 1
fi

cd "$(dirname "$0")"
python3 backend/app.py
