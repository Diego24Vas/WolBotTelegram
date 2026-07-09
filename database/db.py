import asyncio
import sqlite3
import os
from config import settings

_connection = None
_lock = asyncio.Lock()


def get_connection():
    global _connection
    if _connection is None:
        db_dir = os.path.dirname(settings.DATABASE_PATH)
        os.makedirs(db_dir, exist_ok=True)
        _connection = sqlite3.connect(settings.DATABASE_PATH, check_same_thread=False)
        _connection.row_factory = sqlite3.Row
        _connection.execute("PRAGMA journal_mode=WAL")
        _connection.execute("PRAGMA foreign_keys=ON")
        _connection.execute("PRAGMA wal_autocheckpoint=100")
    return _connection


def init_db():
    from database.models import CREATE_TABLES
    conn = get_connection()
    conn.executescript(CREATE_TABLES)
    conn.commit()


async def execute_db(func, *args, **kwargs):
    async with _lock:
        return await asyncio.to_thread(func, *args, **kwargs)


async def checkpoint():
    async with _lock:
        conn = get_connection()
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")


def close_db():
    global _connection
    if _connection:
        try:
            _connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        except Exception:
            pass
        try:
            _connection.close()
        except Exception:
            pass
        _connection = None
