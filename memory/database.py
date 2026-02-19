import sqlite3
import json
from pathlib import Path

# -------------------------
# Database Setup
# -------------------------

DB_PATH = Path(__file__).parent / "failures.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Initialize database with failures table
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS failures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_description TEXT,
            metadata TEXT,
            failure_category TEXT,
            severity TEXT,
            root_causes TEXT,
            failure_type TEXT,
            pattern_summary TEXT,
            prevention_strategies TEXT
        )
    """)
    conn.commit()
    conn.close()


# -------------------------
# Save Failure Event
# -------------------------

def save_failure_event(record: dict) -> int:
    """
    Save failure event to database and return event ID
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO failures (
            timestamp,
            event_description,
            metadata,
            failure_category,
            severity,
            root_causes,
            failure_type,
            pattern_summary,
            prevention_strategies
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record.get("timestamp"),
        record.get("event_description"),
        json.dumps(record.get("metadata", {})),
        record.get("failure_category"),
        record.get("severity"),
        json.dumps(record.get("root_causes", [])),
        record.get("failure_type"),
        record.get("pattern_summary"),
        json.dumps(record.get("prevention_strategies", []))
    ))

    event_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return event_id


# -------------------------
# Initialize DB on Import
# -------------------------
init_db()
