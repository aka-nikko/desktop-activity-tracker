"""
Main entry point for Desktop Activity Tracker.
Initializes all background trackers and summary triggers.
"""

import threading
import time
import logger
from pynput import keyboard as pynput_keyboard
from tracker.window_tracker import track_windows
from tracker.keystroke_tracker import start_keystroke_logger
from tracker.idle_detector import start_listeners, idle_watcher
from summarizer.gpt_summary import summarize_day
from storage.security import setup_security

# Initialize logger
logger = logger.getLogger("MAIN", is_main=True)

def _summary_hotkey_callback() -> None:
    """Callback for manual summary generation via hotkey."""
    logger.info("Generating daily summary via hotkey.")
    summarize_day()

def listen_for_summary_trigger() -> None:
    """Listen for Ctrl+Shift+S to trigger summary generation."""
    logger.info("Press Ctrl+Shift+S anytime to generate summary.")

    hotkey = pynput_keyboard.HotKey(
        pynput_keyboard.HotKey.parse('<ctrl>+<shift>+s'),
        lambda: _summary_hotkey_callback()
    )

    def for_canonical(f):
        return lambda k: f(l.canonical(k))

    with pynput_keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)
    ) as l:
        l.join()

def schedule_nightly_summary() -> None:
    """Automatically generate summary at 23:59 each day."""
    while True:
        now = time.localtime()
        if now.tm_hour == 23 and now.tm_min == 59:
            logger.info("Generating nightly summary at 23:59.")
            summarize_day()
            time.sleep(60)
        time.sleep(10)

if __name__ == "__main__":
    setup_security()
    logger.info("Desktop Activity Tracker starting...")
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
        logger.info("Desktop Activity Tracker stopped by user.")
