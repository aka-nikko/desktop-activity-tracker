"""
Idle time tracking for Desktop Activity Tracker.
Logs user inactivity and triggers events based on idle time.
"""

import time
from pynput import keyboard, mouse
from storage.db import log_idle

# Global variable to track last input time
last_input_time = time.time()

# Initialize logger for idle detection
main_logger = None
def get_logger():
    """Get the main logger instance, initializing it if necessary."""
    global main_logger
    if main_logger is None:
        from logging_utils.logger import init_logger
        main_logger = init_logger("IDLE")
    return main_logger

def on_input(_: object) -> None:
    """Reset the last input time on any keyboard or mouse event."""
    global last_input_time
    last_input_time = time.time()

def start_listeners() -> None:
    """Start listeners for keyboard and mouse input."""
    keyboard.Listener(on_press=on_input).start()
    mouse.Listener(on_click=on_input).start()
    get_logger().info("Input listeners started for keyboard and mouse.")

def idle_watcher() -> None:
    """Monitor for user inactivity and log idle events."""
    global last_input_time
    while True:
        time.sleep(5)
        idle_duration = time.time() - last_input_time
        if idle_duration > 300:
            log_idle(idle_duration)
            last_input_time = time.time()
            get_logger().info(f"User idle for {int(idle_duration)} seconds, logged idle activity.")