"""
Window tracking for Desktop Activity Tracker.
Logs active window changes and durations.
"""

import time
import win32gui
import win32process
import psutil
from storage.db import log_activity
import logging

logger = logging.getLogger("window_tracker")

def get_active_window() -> tuple[str, str]:
    """Return the current active window's process name and title."""
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        process = psutil.Process(pid)
        exe = process.name()
    except psutil.NoSuchProcess:
        exe = "Unknown"
    title = win32gui.GetWindowText(hwnd)
    return exe, title

def track_windows() -> None:
    """Continuously track and log active window changes."""
    last_window = None
    start_time = time.time()
    while True:
        time.sleep(1)
        current_window = get_active_window()
        if current_window != last_window:
            end_time = time.time()
            if last_window:
                duration = end_time - start_time
                log_activity(last_window[0], last_window[1], duration)
                logger.info(f"Window switched: {last_window[0]} - {last_window[1]} | Duration: {duration:.2f}s")
            start_time = end_time
            last_window = current_window
