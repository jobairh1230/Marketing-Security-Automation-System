import sqlite3
import time
from app.marketing.schema import MarketingContent
import json
from dotenv import load_dotenv
import os

load_dotenv()

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
    # Ensure that payload is serialized properly using Pydantic's .json() method
    payload_json = payload.json() if hasattr(payload, "json") else json.dumps(payload.__dict__)
    
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            "INSERT INTO marketing_content (created_at, content_type, status, brief, payload_json) VALUES (?, ?, ?, ?, ?)",
            (time.time(), content_type, "DRAFT", brief, payload_json)
        )
        con.commit()

def list_items():
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.execute("SELECT * FROM marketing_content WHERE status = 'DRAFT'")
        items = cursor.fetchall()
    return items

def update_status(item_id, status):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("UPDATE marketing_content SET status = ? WHERE id = ?", (status, item_id))
        con.commit()

def get_item(item_id):
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.execute("SELECT * FROM marketing_content WHERE id = ?", (item_id,))
        item = cursor.fetchone()
    return item



# import sqlite3
# import time
# from app.marketing.schema import MarketingContent
# from dotenv import load_dotenv
# import os
# import json

# load_dotenv()

# DB_PATH = os.getenv("APP_DB_PATH", ".app.db")  # Database path from environment variable

# def init_db() -> None:
#     with sqlite3.connect(DB_PATH) as con:
#         con.execute("""
#         CREATE TABLE IF NOT EXISTS marketing_content (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             created_at REAL NOT NULL,
#             content_type TEXT NOT NULL,
#             status TEXT NOT NULL,
#             brief TEXT NOT NULL,
#             payload_json TEXT NOT NULL
#         )
#         """)
#         con.commit()

# def create_draft(content_type: str, brief: str, payload: MarketingContent):
#     # Ensure that payload is serialized properly using Pydantic's .json() method
#     payload_json = payload.json() if hasattr(payload, "json") else json.dumps(payload.__dict__)
    
#     with sqlite3.connect(DB_PATH) as con:
#         con.execute(
#             "INSERT INTO marketing_content (created_at, content_type, status, brief, payload_json) VALUES (?, ?, ?, ?, ?)",
#             (time.time(), content_type, "DRAFT", brief, payload_json)
#         )
#         con.commit()

