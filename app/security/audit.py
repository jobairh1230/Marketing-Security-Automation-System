import sqlite3
import time
import json

DB_PATH = ".app.db"

def log_audit(action: str, text: str, allowed: bool, reasons: str):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at REAL NOT NULL,
            action TEXT NOT NULL,
            allowed INTEGER NOT NULL,
            reasons TEXT NOT NULL,
            redacted_input TEXT NOT NULL
        )
        """)
        con.execute(
            "INSERT INTO audit_logs (created_at, action, allowed, reasons, redacted_input) VALUES (?, ?, ?, ?, ?)",
            (time.time(), action, int(allowed), reasons, text)
        )
        con.commit()
