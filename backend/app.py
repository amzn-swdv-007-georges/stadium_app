# ─────────────────────────────────────────────────────────────────────────────
# backend/app.py — Flask API server
# ─────────────────────────────────────────────────────────────────────────────
#
# ARCHITECTURAL BOUNDARY RULE (from SPECS/TECH.md):
#   This file handles HTTP routing ONLY.
#   It must NEVER import sqlite3 or write SQL queries directly.
#   All database access goes through data_layer.py.
#
# Logging is kept out of business logic by using a small decorator that
# records each request at the route boundary — no log statements mixed into
# the route handlers themselves.
#
import logging
import os
from functools import wraps

from flask import Flask, jsonify, request, send_from_directory

import data_layer

# Configure a module-level logger so request logging is centralized here,
# not scattered inside route handlers.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_request(fn):
    """Decorator: logs the method and path before delegating to the route.

    Keeps logging concerns separate from HTTP/business logic.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        logger.info(
            "REQUEST %s %s",
            request.method,
            request.full_path.rstrip('?'),
        )
        return fn(*args, **kwargs)
    return wrapper


app = Flask(__name__)
FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'frontend',
)


@app.route('/')
@log_request
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:filename>')
@log_request
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# ─── GET /api/entries ─────────────────────────────────────────────────────────
#
# Returns all stadium entry records as a JSON array.
#
# Optional query parameter:
#   ?gate=A  — filters results to a single gate (A, B, C, or D)
#
# This route only reads the request and delegates to the data layer.
# It must never build SQL or import sqlite3.
#
@app.route('/api/entries', methods=['GET'])
@log_request
def get_entries():
    try:
        gate = request.args.get('gate')
        if gate:
            entries = data_layer.get_entries_by_gate(gate)
        else:
            entries = data_layer.get_all_entries()
        return jsonify(entries)
    except Exception as exc:
        logger.exception("Failed to fetch entries")
        return jsonify({"error": str(exc)}), 500


# ─── GET /api/health ─────────────────────────────────────────────────────────
#
# Simple health check so the frontend can confirm the backend is running.
# Returns: {"status": "ok"}
#
@app.route('/api/health', methods=['GET'])
@log_request
def health():
    return jsonify({"status": "ok"})


# ─────────────────────────────────────────────────────────────────────────────
# Server entry point
#
# host="0.0.0.0"  — required for Codio's preview panel to reach the server.
#                   Never use "127.0.0.1" here or the preview will not load.
# port=5000       — matches the project run command and Codio preview.
# debug=True      — auto-reloads when you save a file during development.
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Stadium Security Backend starting…")
    print("Dashboard: http://0.0.0.0:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
