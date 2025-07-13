import os
import logging
from datetime import datetime
from config.load_config import config_data

# Global logger instance
_log_file = None  # Will be set on first init_logger()
_loggers = {}     # Cache of loggers to avoid duplicates

def init_logger(name: str, is_main: bool = False) -> logging.Logger:
    """Initialize and return a logger instance with file and console handlers."""
    if name in _loggers:
        return _loggers[name]

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)  # Capture all levels, filter in handlers
    log.propagate = False        # Avoid duplicate logs

    if not log.handlers:
        # Create logs directory if it doesn't exist
        os.makedirs(config_data["LOG_DIR"], exist_ok=True)

        # File handler
        global _log_file
        if _log_file is None:
            log_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            _log_file = os.path.join(config_data["LOG_DIR"], f"{log_time}.log")

        if name != "TRAY":
            file_handler = logging.FileHandler(_log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(
                "%(asctime)-24s %(name)-10s %(levelname)-8s %(message)s"
            ))
            log.addHandler(file_handler)

        # Stream (console) handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO if is_main else logging.WARNING)
        stream_handler.setFormatter(logging.Formatter(
            "%(name)s - %(levelname)s - %(message)s"
        ))
        log.addHandler(stream_handler)

    _loggers[name] = log
    return log
