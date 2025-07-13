"""
Security utilities for Desktop Activity Tracker.
Handles encryption and storage of sensitive credentials.
"""

import os
from cryptography.fernet import Fernet
from datetime import datetime
from config.load_config import config_data

# Global variable for the Fernet cipher
cipher = None

# Initialize logger for security operations
main_logger = None
def get_logger():
    """Get the main logger instance, initializing it if necessary."""
    global main_logger
    if main_logger is None:
        from logging_utils.logger import init_logger
        main_logger = init_logger("SECURITY")
    return main_logger

def generate_key() -> None:
    """Generate and store a new Fernet key."""
    os.makedirs(config_data["FERNET_KEY_PATH"], exist_ok=True)
    key = Fernet.generate_key()
    with open(f"{config_data["FERNET_KEY_PATH"]}/fernet.key", "wb") as f:
        f.write(key)
    get_logger().info("Generated and stored new Fernet key.")

def setup_security() -> None:
    """Initialize encryption key and cipher."""
    global cipher
    os.makedirs(config_data["FERNET_KEY_PATH"], exist_ok=True)
    if not os.path.exists(f"{config_data["FERNET_KEY_PATH"]}/fernet.key"):
        generate_key()
    with open(f"{config_data["FERNET_KEY_PATH"]}/fernet.key", "rb") as f:
        key = f.read()
    cipher = Fernet(key)
    get_logger().info("Loaded Fernet key from file.")

def encrypt_and_store_credential(username: str, password: str, app: str, title: str) -> None:
    """Encrypt and store a credential record."""
    if cipher is None:
        raise RuntimeError("Security not initialized. Call setup_security() first.")
    try:
        data = f"{datetime.now().isoformat()}||{username}||{password}||{app}||{title}"
        encrypted = cipher.encrypt(data.encode())
        with open(f"{config_data["DB_PATH"]}/creds.bin", "ab") as f:
            f.write(encrypted + b"\n")
        get_logger().info(f"Credential encrypted and stored for app: {app}, title: {title}")
    except Exception as e:
        get_logger().error(f"Failed to encrypt/store credential: {e}")

def decrypt_credentials() -> list[str]:
    """Decrypt and return all stored credentials as a list of strings."""
    if cipher is None:
        raise RuntimeError("Security not initialized. Call setup_security() first.")
    decrypted = []
    try:
        with open(f"{config_data["DB_PATH"]}/creds.bin", "rb") as f:
            for line in f:
                decrypted.append(cipher.decrypt(line.strip()).decode())
        return decrypted
    except Exception as e:
        get_logger().error(f"Failed to decrypt credentials: {e}")
        return []
