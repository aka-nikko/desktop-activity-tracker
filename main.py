"""
Main entry point for Desktop Activity Tracker.
Initializes all background trackers and summary triggers.
"""

import threading
from tracker.window_tracker import track_windows
from tracker.keystroke_tracker import start_keystroke_logger
from tracker.idle_detector import start_listeners, idle_watcher
from summarizer.gpt_summary import summarize_day
from storage.security import setup_security
from summarizer.gpt_summary import listen_for_summary_trigger, schedule_nightly_summary

# Initialize logger
main_logger = None
def get_logger():
    """Get the main logger instance, initializing it if necessary."""
    global main_logger
    if main_logger is None:
        from logger import init_logger
        main_logger = init_logger("MAIN", is_main=True)
    return main_logger

if __name__ == "__main__":
    get_logger().info("Desktop Activity Tracker starting...")

    # Setup security features
    setup_security()

    # Start background trackers
    threading.Thread(target=start_keystroke_logger, daemon=True).start()     # Keystroke logger
    threading.Thread(target=start_listeners, daemon=True).start()            # Mouse and keyboard listeners
    threading.Thread(target=idle_watcher, daemon=True).start()               # Idle detector
    threading.Thread(target=listen_for_summary_trigger, daemon=True).start() # Hotkey listener
    threading.Thread(target=schedule_nightly_summary, daemon=True).start()   # Nightly summary
    try:
        # Main window tracker (blocking)
        track_windows()
    except KeyboardInterrupt:
        get_logger().info("Desktop Activity Tracker stopped by user.")
