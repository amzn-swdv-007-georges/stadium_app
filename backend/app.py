# ─────────────────────────────────────────────────────────────────────────────
# backend/app.py — Flask API server
# STUB FILE — OpenCode will implement the route bodies below.
# Read the comments to understand what each route must do.
# ─────────────────────────────────────────────────────────────────────────────
#
# ARCHITECTURAL BOUNDARY RULE (from SPECS/TECH.md):
#   This file handles HTTP routing ONLY.
#   It must NEVER import sqlite3 or write SQL queries directly.
#   All database access goes through data_layer.py.
#
from flask import Flask, jsonify, request
from markupsafe import escape

# Import the data layer — the ONLY place SQL is allowed.
# Notice: no "import sqlite3" here. That boundary is enforced.
import data_layer

import os
from flask import send_from_directory

app = Flask(__name__)
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')


@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# ─── GET /api/entries ─────────────────────────────────────────────────────────
#
# Returns all stadium entry records as a JSON array.
#
# Optional query parameter:
#   ?gate=A  — filters results to a single gate (A, B, C, or D)
#
# What it must do:
#   1. Read the optional ?gate= query parameter from the request
#   2. If gate is provided → call data_layer.get_entries_by_gate(gate)
#      If gate is absent   → call data_layer.get_all_entries()
#   3. Return the result as JSON with HTTP 200
#   4. On error → return {"error": "..."} with HTTP 500
#
# OpenCode will implement this route body.
#
@app.route('/api/entries', methods=['GET'])
def get_entries():
    try:
        gate = request.args.get('gate')
        if gate:
            entries = data_layer.get_entries_by_gate(gate)
        else:
            entries = data_layer.get_all_entries()
        return jsonify(entries)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── GET /api/health ─────────────────────────────────────────────────────────
#
# Simple health check so the frontend can confirm the backend is running.
# Returns: {"status": "ok"}
#
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


# ─── GET /api/entries/table ──────────────────────────────────────────────────
#
# HTMX fragment endpoint — returns HTML for the entry table body, plus
# out-of-band (OOB) swaps that update the entry count and connection status
# elsewhere on the page. The frontend needs no custom JavaScript.
#
# The response body is swapped into #entries-body (the table rows). Elements
# carrying hx-swap-oob="true" are applied to matching ids anywhere in the DOM:
#   - <span id="count-value">       -> updates Entries: N counter
#   - <div id="status-badge">       -> updates the connection status pill
#
# Query parameter:
#   ?gate=A  — optional, filters rows to a single gate (same as /api/entries)
#
@app.route('/api/entries/table', methods=['GET'])
def entries_table():
    try:
        gate = request.args.get('gate')
        if gate:
            entries = data_layer.get_entries_by_gate(gate)
        else:
            entries = data_layer.get_all_entries()

        rows = ''
        for e in entries:
            rows += (
                '<tr>'
                f'<td>{e["id"]}</td>'
                f'<td>{e["person_id"]}</td>'
                f'<td><span class="gate-badge gate-{escape(e["gate"])}">{escape(e["gate"])}</span></td>'
                f'<td>{e["hour"]}</td>'
                f'<td>{escape(e["bag"])}</td>'
                '</tr>'
            )

        if not rows:
            rows = '<tr><td colspan="5" class="empty-cell">No entries for this gate.</td></tr>'

        count_oob = f'<span id="count-value" hx-swap-oob="true">{len(entries)}</span>'
        status_oob = '<div id="status-badge" class="connected" hx-swap-oob="true">Backend Connected</div>'
        return f'{rows}{count_oob}{status_oob}'
    except Exception as e:
        count_oob = '<span id="count-value" hx-swap-oob="true">0</span>'
        status_oob = '<div id="status-badge" hx-swap-oob="true">Backend Offline</div>'
        return f'<tr><td colspan="5" class="empty-cell">Unable to load entries.</td></tr>{count_oob}{status_oob}', 500


# ─────────────────────────────────────────────────────────────────────────────
# Server entry point
#
# host="0.0.0.0"  — required for Codio's preview panel to reach the server.
#                   Never use "127.0.0.1" here or the preview will not load.
# port=5000       — matches the Codio preview URL (https://HOSTNAME-5000.codio.io)
# debug=True      — auto-reloads when you save a file during development.
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Stadium Security Backend starting…")
    print("Dashboard: https://grandherman-nelsonvitamin-5000.codio.io/")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
