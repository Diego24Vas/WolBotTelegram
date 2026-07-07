import sqlite3
import os
from config import settings

def get_connection():
    db_dir = os.path.dirname(settings.DATABASE_PATH)
    os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    from database.models import CREATE_TABLES
    conn = get_connection()
    conn.executescript(CREATE_TABLES)
    conn.commit()
    conn.close()
