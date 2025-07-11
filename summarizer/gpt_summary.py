"""
Summarization utilities for Desktop Activity Tracker.
Generates a daily productivity summary using OpenAI GPT.
"""

import openai
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger("summarizer")

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
