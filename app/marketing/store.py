import sqlite3
import time
from app.marketing.schema import MarketingContent
from dotenv import load_dotenv
load_dotenv()
import os

DB_PATH = os.getenv("APP_DB_PATH", ".app.db")

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS marketing_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at REAL NOT NULL,
            content_type TEXT NOT NULL,
            status TEXT NOT NULL,
            brief TEXT NOT NULL,
            payload_json TEXT NOT NULL
        )
        """)
        con.commit()

def create_draft(content_type: str, brief: str, payload: MarketingContent):
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO marketing_content (created_at, content_type, status, brief, payload_json) VALUES (?, ?, ?, ?, ?)",
            (time.time(), content_type, "DRAFT", brief, payload.json())
        )
        con.commit()
