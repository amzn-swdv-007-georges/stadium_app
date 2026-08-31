# System Architecture & Technical Specifications

## Overview

This document defines the system architecture, component boundaries, and technical constraints for the Stadium Security Management Application. The architecture adheres to strict separation of concerns, ensuring user interfaces, business routes, query logic, and physical storage remain decoupled.

---

## Target Data Flow & Architecture

Data flows unidirectionally through four distinct architectural layers:

```
+-------------------+        HTTP / JSON        +-------------------+
|     Frontend      |  <--------------------->  |  Backend (Routes) |
| (Web UI / Client) |                           |  (REST API Server)|
+-------------------+                           +-------------------+
                                                          |
                                                  Function Calls / Py
                                                          v
+-------------------+        SQL / Parameters   +-------------------+
| SQLite Database   |  <--------------------->  |    Data Layer     |
|   (stadium.db)    |                           | (data_layer.py)   |
+-------------------+                           +-------------------+
```

---

## Component Boundaries & Layer Responsibilities

### 1. Frontend Layer
* **Role**: User interaction, rendering security dashboards, entry log visualization, and gate alerts.
* **Communication**: Communicates exclusively with the Backend via RESTful HTTP endpoints (`/api/...`).
* **Constraints**: 
  * Zero knowledge of database schemas, SQL syntax, or file paths.
  * Formats outgoing payloads as JSON; parses incoming JSON responses.

### 2. Backend Layer (API & Service Routing)
* **Role**: HTTP request handling, route dispatching, request payload validation, HTTP status code formatting, and error handling.
* **Communication**: Receives HTTP requests from Frontend; invokes Python methods in the Data Layer.
* **Constraints**:
  * Does not construct or execute raw SQL strings directly within route handlers.
  * Delegates all persistence operations to `backend/data_layer.py`.

### 3. Data Layer (`backend/data_layer.py`)
* **Role**: Database connection lifecycle management, SQL query generation, parameterized binding, transaction control (`COMMIT`/`ROLLBACK`), and row-to-dictionary translation.
* **Communication**: Executes parameterized SQL commands against `stadium.db`.
* **Constraints**:
  * Acts as the sole access point to SQLite.
  * All user inputs must be passed via query parameters (preventing SQL injection).

### 4. Database Storage Layer (`stadium.db`)
* **Role**: Persistent on-disk storage using SQLite 3.
* **Location**: Root workspace / backend runtime folder (`stadium.db`).
* **Constraints**:
  * Single file storage with SQLite WAL (Write-Ahead Logging) enabled for local concurrency.

---

## Primary Data Schemas

### Table: `stadium_entries`

Tracks individual badge scans and security gate event logs.

| Column Name      | Data Type | Constraints               | Description                              |
|------------------|-----------|---------------------------|------------------------------------------|
| `id`             | INTEGER   | PRIMARY KEY AUTOINCREMENT | Unique entry record identifier           |
| `timestamp`      | DATETIME  | NOT NULL DEFAULT CURRENT_TIMESTAMP | UTC timestamp of the entry scan |
| `badge_id`       | TEXT      | NOT NULL                  | Unique identifier for attendee/staff     |
| `gate`           | TEXT      | NOT NULL                  | Gate designation (e.g., `'A'`, `'B'`)   |
| `entry_status`   | TEXT      | NOT NULL                  | Status (`'GRANTED'`, `'DENIED'`, `'FLAGGED'`) |
| `security_level` | INTEGER   | NOT NULL DEFAULT 1        | Clearance level required for gate       |
| `notes`          | TEXT      | NULL                      | Optional guard audit notes               |

---

## Security & Implementation Rules

1. **SQL Injection Prevention**:
   * NEVER use string interpolation (`f"SELECT * FROM ... WHERE gate = '{gate}'"`) for SQL construction.
   * ALWAYS use parameterized placeholders (`SELECT * FROM stadium_entries WHERE gate = ?`).
2. **Boundary Enforcement**:
   * No backend API route may import `sqlite3` directly. All database access calls `DataLayer` class methods.
3. **Data Integrity**:
   * Transactions must be wrapped in atomic blocks with proper error catching and rollback capabilities.