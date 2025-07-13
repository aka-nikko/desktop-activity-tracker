"""
Database logging utilities for Desktop Activity Tracker.
Handles activity, keystroke, and idle event logging.
"""

import sqlite3
import os
from datetime import datetime
from config.load_config import config_data

# Initialize logger for database operations
main_logger = None
def get_logger():
    """Get the main logger instance, initializing it if necessary."""
    global main_logger
    if main_logger is None:
        from logging_utils.logger import init_logger
        main_logger = init_logger("DB")
    return main_logger

def init_db() -> None:
    """Initialize the SQLite database and tables if not present."""
    # Ensure logs directory exists
    os.makedirs(config_data["DB_PATH"], exist_ok=True)
    try:
        with sqlite3.connect(f"{config_data["DB_PATH"]}/{config_data["DB_FILE"]}") as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS activity (timestamp TEXT, app TEXT, title TEXT, duration REAL)")
            c.execute("CREATE TABLE IF NOT EXISTS keystrokes (timestamp TEXT, key TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS idle (timestamp TEXT, duration REAL)")
            conn.commit()
        get_logger().info("Database initialized with activity, keystrokes, and idle tables.")
    except Exception as e:
        get_logger().error(f"Failed to initialize database: {e}")

def log_activity(app: str, title: str, duration: float) -> None:
    """Log an application window activity event."""
    try:
        with sqlite3.connect(f"{config_data["DB_PATH"]}/{config_data["DB_FILE"]}") as conn:
            conn.execute("INSERT INTO activity VALUES (?, ?, ?, ?)", (datetime.now().isoformat(), app, title, duration))
            conn.commit()
        get_logger().info(f"Activity logged: {app} - {title} ({duration:.2f}s)")
    except Exception as e:
        get_logger().error(f"Failed to log activity: {e}")

def log_keystroke(key: str) -> None:
    """Log a single keystroke event."""
    try:
        with sqlite3.connect(f"{config_data["DB_PATH"]}/{config_data["DB_FILE"]}") as conn:
            conn.execute("INSERT INTO keystrokes VALUES (?, ?)", (datetime.now().isoformat(), key))
            conn.commit()
        get_logger().info(f"Keystroke logged: {key}")
    except Exception as e:
        get_logger().error(f"Failed to log keystroke: {e}")

def log_keystrokes_batch(keys: list[str]) -> None:
    """Batch log multiple keystrokes."""
    if not keys:
        return
    now = datetime.now().isoformat()
    try:
        with sqlite3.connect(f"{config_data["DB_PATH"]}/{config_data["DB_FILE"]}") as conn:
            conn.executemany("INSERT INTO keystrokes VALUES (?, ?)", [(now, k) for k in keys])
            conn.commit()
        get_logger().info(f"Batch keystrokes logged: {len(keys)} keys")
    except Exception as e:
        get_logger().error(f"Failed to log keystrokes batch: {e}")

def log_idle(duration: float) -> None:
    """Log an idle event (user inactivity)."""
    try:
        with sqlite3.connect(f"{config_data["DB_PATH"]}/{config_data["DB_FILE"]}") as conn:
            conn.execute("INSERT INTO idle VALUES (?, ?)", (datetime.now().isoformat(), duration))
            conn.commit()
        get_logger().info(f"Idle event logged: {duration:.0f}s")
    except Exception as e:
        get_logger().error(f"Failed to log idle: {e}")