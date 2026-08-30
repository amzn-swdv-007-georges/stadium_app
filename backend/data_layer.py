# ─────────────────────────────────────────────────────────────────────────────
# backend/data_layer.py — Database access layer
# STUB FILE — OpenCode will complete get_entries_by_gate() below.
# The two functions above it are already implemented as reference.
# ─────────────────────────────────────────────────────────────────────────────
#
# ARCHITECTURAL BOUNDARY RULE (from SPECS/TECH.md):
#   This is the ONLY file in the project that may import sqlite3 or write SQL.
#   app.py calls these functions. It never touches the database directly.
#
import sqlite3
import os

# Path to the database file — one level up from this backend/ folder.
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'stadium.db')


# ─── get_db_connection() ──────────────────────────────────────────────────────
#
# Opens and returns a connection to stadium.db.
#
# conn.row_factory = sqlite3.Row lets each returned row behave like a
# dictionary, so you can access columns by name (row['gate']) instead
# of by index (row[2]).
#
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    return conn


# ─── get_all_entries() ────────────────────────────────────────────────────────
#
# Retrieves every row from stadium_entries, newest first.
#
# Returns: list of plain Python dicts — one per entry row.
#
# [dict(row) for row in rows] converts sqlite3.Row objects into regular
# Python dicts so Flask's jsonify() can serialize them to JSON.
#
def get_all_entries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM stadium_entries ORDER BY hour DESC'
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]  # convert to plain dicts


# ─── get_entries_by_gate(gate) ────────────────────────────────────────────────
#
# Retrieves only the rows where gate matches the given value.
#
# Parameters:
#   gate — string, e.g. "A", "B", "C", or "D"
#
# SECURITY RULE — always use a parameterised query (the ? placeholder).
# Never build the query with string formatting like f"WHERE gate = '{gate}'".
# The ? tells SQLite to treat the value as literal data, not as SQL syntax.
# This prevents SQL injection attacks.
#
# Returns: list of plain Python dicts — same shape as get_all_entries().
#
# OpenCode will implement this function body in Step 6.
#
def get_entries_by_gate(gate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM stadium_entries WHERE gate = ? ORDER BY hour DESC',
        (gate,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
