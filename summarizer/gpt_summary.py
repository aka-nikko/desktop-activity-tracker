"""
Summarization utilities for Desktop Activity Tracker.
Generates a daily productivity summary using OpenAI GPT.
"""

import openai
import sqlite3
import os
import time
import logger
from datetime import datetime
from pynput import keyboard as pynput_keyboard
from dotenv import load_dotenv

# Initialize logger for summarization
logger = logger.getLogger("SUMMARY")

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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

def summarize_day() -> None:
    """Generate and log a daily summary of user activity using OpenAI GPT."""
    db_path = "logs/activityDatabase.db"
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM activity WHERE timestamp >= date('now')")
            activities = c.fetchall()
            c.execute("SELECT * FROM keystrokes WHERE timestamp >= date('now')")
            keystrokes = c.fetchall()
    except Exception as db_err:
        logger.error(f"Database error: {db_err}")
        return

    # Redact sensitive keystrokes
    redacted_keys = [k if k != "[REDACTED]" else "" for _, k in keystrokes]

    # Prepare prompt for GPT
    prompt = f"""
        You are a productivity analyst. Summarize this user's day based on:
        - App usage and window titles
        - Keystrokes (with sensitive inputs redacted)
        Give insights on what they did, how long they were productive, what topics they were focused on, and any distractions.
        DATA:
        ACTIVITY: {activities[:50]}
        KEYS: {redacted_keys[:50]}
    """

    try:
        if not openai.api_key:
            logger.error("OPENAI_API_KEY not set. Please set it in your environment or .env file.")
            return
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        summary = response.choices[0].message.content
        logger.info(f"--- Daily Summary ---\n{summary}")

        # Save summary to file
        os.makedirs("logs", exist_ok=True)
        with open(f"logs/summary_{datetime.now().date()}.txt", "w", encoding="utf-8") as f:
            f.write(summary)
        logger.info("Summary saved to file.")

    except Exception as e:
        logger.error(f"Failed to generate summary: {e}")
