"""
Security utilities for Desktop Activity Tracker.
Handles encryption and storage of sensitive credentials.
"""

from cryptography.fernet import Fernet
import os
import logger
from datetime import datetime

key_file = "logs/fernet.key"
cred_file = "logs/creds.bin"
logger = logger.getLogger("SECURITY")

cipher = None

def generate_key() -> None:
    """Generate and store a new Fernet key."""
    os.makedirs('logs', exist_ok=True)
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)

def setup_security():
    """Initialize encryption key and cipher."""
    global cipher
    os.makedirs('logs', exist_ok=True)
    if not os.path.exists(key_file):
        generate_key()
    with open(key_file, "rb") as f:
        key = f.read()
    cipher = Fernet(key)

def encrypt_and_store_credential(username: str, password: str, app: str, title: str) -> None:
    """Encrypt and store a credential record."""
    if cipher is None:
        raise RuntimeError("Security not initialized. Call setup_security() first.")
    try:
        data = f"{datetime.now().isoformat()}||{username}||{password}||{app}||{title}"
        encrypted = cipher.encrypt(data.encode())
        with open(cred_file, "ab") as f:
            f.write(encrypted + b"\n")
        logger.info(f"Credential encrypted and stored for app: {app}, title: {title}")
    except Exception as e:
        logger.error(f"Failed to encrypt/store credential: {e}")

def decrypt_credentials() -> list[str]:
    """Decrypt and return all stored credentials as a list of strings."""
    if cipher is None:
        raise RuntimeError("Security not initialized. Call setup_security() first.")
    decrypted = []
    try:
        with open(cred_file, "rb") as f:
            for line in f:
                decrypted.append(cipher.decrypt(line.strip()).decode())
        return decrypted
    except Exception as e:
        logger.error(f"Failed to decrypt credentials: {e}")
        return []
