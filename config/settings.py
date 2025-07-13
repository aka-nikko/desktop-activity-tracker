"""
Configuration settings for the Desktop Activity Tracker. 
"""

# Logging folder and database path
LOG_DIR = "logs"
DB_PATH = "logs"
DB_FILE = f"{DB_PATH}/activityDatabase.db"

# Paths for encryption key
FERNET_KEY_PATH = "assets"
FERNET_KEY_FILE = f"{FERNET_KEY_PATH}/fernet.key"

# Paths for credentials and sensitive data
CREDS_FILE_PATH = "assets"
CREDS_FILE_FILE = f"{CREDS_FILE_PATH}/creds.bin"

# Sensitive keywords to redact
SENSITIVE_KEYWORDS = ["login", "sign in", "password", "auth"]

# Maximum number of entries to keep in memory before flushing to the database
BATCH_SIZE = 20

# Interval for flushing entries to the database
FLUSH_INTERVAL = 1.0  # seconds

# Hotkey for generating summary for deaktop activity
SUMMARY_TRIGGER = "<ctrl>+<shift>+s"

# Time for automatically generating summary
SUMMARY_HOUR = 23
SUMMARY_MINUTE = 59

# GPT model to use for summary generation
GPT_MODEL = "gpt-3.5-turbo"