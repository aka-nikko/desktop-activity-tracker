import json
import os
import sys
from pathlib import Path

def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for PyInstaller and dev"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_config() -> dict:
    """Load the configuration from the JSON file"""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

# Paths for configuration files
config_path = Path(resource_path("config/settings.json")).resolve()
env_path = Path(resource_path(".env")).resolve()
config_data = load_config()
