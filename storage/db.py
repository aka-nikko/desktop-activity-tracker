"""
Database logging utilities for Desktop Activity Tracker.
Handles activity, keystroke, and idle event logging.
"""

import sqlite3
import os
import logger
from datetime import datetime

os.makedirs("logs", exist_ok=True)
db_path = "logs/activityDatabase.db"
logger = logger.getLogger("DB")

def init_db() -> None:
    """Initialize the SQLite database and tables if not present."""
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS activity (timestamp TEXT, app TEXT, title TEXT, duration REAL)")
        c.execute("CREATE TABLE IF NOT EXISTS keystrokes (timestamp TEXT, key TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS idle (timestamp TEXT, duration REAL)")
        conn.commit()

init_db()

def log_activity(app: str, title: str, duration: float) -> None:
    """Log an application window activity event."""
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute("INSERT INTO activity VALUES (?, ?, ?, ?)", (datetime.now().isoformat(), app, title, duration))
            conn.commit()
        logger.info(f"Activity logged: {app} - {title} ({duration:.2f}s)")
    except Exception as e:
        logger.error(f"Failed to log activity: {e}")

def log_keystroke(key: str) -> None:
    """Log a single keystroke event."""
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute("INSERT INTO keystrokes VALUES (?, ?)", (datetime.now().isoformat(), key))
            conn.commit()
        logger.info(f"Keystroke logged: {key}")
    except Exception as e:
        logger.error(f"Failed to log keystroke: {e}")

def log_keystrokes_batch(keys: list[str]) -> None:
    """Batch log multiple keystrokes."""
    if not keys:
        return
    now = datetime.now().isoformat()
    try:
        with sqlite3.connect(db_path) as conn:
            conn.executemany("INSERT INTO keystrokes VALUES (?, ?)", [(now, k) for k in keys])
            conn.commit()
        logger.info(f"Batch keystrokes logged: {len(keys)} keys")
    except Exception as e:
        logger.error(f"Failed to log keystrokes batch: {e}")

def log_idle(duration: float) -> None:
    """Log an idle event (user inactivity)."""
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute("INSERT INTO idle VALUES (?, ?)", (datetime.now().isoformat(), duration))
            conn.commit()
        logger.info(f"Idle event logged: {duration:.0f}s")
    except Exception as e:
        logger.error(f"Failed to log idle: {e}")
