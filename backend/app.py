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


# ─────────────────────────────────────────────────────────────────────────────
# Server entry point
#
# host="0.0.0.0"  — required for Codio's preview panel to reach the server.
#                   Never use "127.0.0.1" here or the preview will not load.
# port=3000       — matches the Codio preview URL (https://HOSTNAME-3000.codio.io)
# debug=True      — auto-reloads when you save a file during development.
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Stadium Security Backend starting…")
    print("Dashboard: https://nervefuel-crimsonfish-5000.codio.io/")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
