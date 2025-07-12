import os
import logging
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Create timestamped log file name
LOG_TIME = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = os.path.join(LOG_DIR, f"{LOG_TIME}.log")

def getLogger(name: str, is_main: bool = False) -> logging.Logger:
    """Get a configured logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels, filter in handlers
    logger.propagate = False  # Avoid duplicate logs

    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)-24s %(name)-10s %(levelname)-8s %(message)s"
        ))
        logger.addHandler(file_handler)

        # Stream (console) handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO if is_main else logging.WARNING)
        stream_handler.setFormatter(logging.Formatter(
            "%(name)s - %(levelname)s - %(message)s"
        ))
        logger.addHandler(stream_handler)

    return logger
