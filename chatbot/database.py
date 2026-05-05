"""
Database manager for multi-user progress tracking.
Uses SQLite to store user credentials and per-user progress.
"""

import hashlib
import json
import os
import sqlite3
import threading


def _hash_password(password: str, salt: bytes | None = None) -> str:
    """Return a hex string of the form ``<hex_salt>:<hex_hash>``."""
    if salt is None:
        salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 260_000)
    return salt.hex() + ":" + key.hex()


def _verify_password(password: str, stored: str) -> bool:
    """Return True if *password* matches the *stored* hash string."""
    try:
        salt_hex, _ = stored.split(":", 1)
        salt = bytes.fromhex(salt_hex)
    except (ValueError, AttributeError):
        return False
    return _hash_password(password, salt) == stored


class DatabaseManager:
    """Manages user accounts and progress in a SQLite database."""

    def __init__(self, db_path="karite_users.db"):
        """
        Connect to SQLite and create the users table if it doesn't exist.

        Args:
            db_path: Path to the SQLite database file.
        """
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        with self._lock:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    progress TEXT
                )
                """
            )
            self._conn.commit()

    def register_user(self, username, password):
        """
        Insert a new user with empty progress.

        Args:
            username: The desired username.
            password: The plaintext password (stored as a secure hash).

        Returns:
            True if registration succeeded, False if the username already exists.
        """
        try:
            with self._lock:
                self._conn.execute(
                    "INSERT INTO users (username, password, progress) VALUES (?, ?, ?)",
                    (username, _hash_password(password), json.dumps({})),
                )
                self._conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        """
        Check whether a username/password pair is valid.

        Args:
            username: The username to look up.
            password: The plaintext password to verify.

        Returns:
            True if credentials are correct, False otherwise.
        """
        with self._lock:
            row = self._conn.execute(
                "SELECT password FROM users WHERE username = ?", (username,)
            ).fetchone()
        if row is None:
            return False
        return _verify_password(password, row[0])

    def get_progress(self, username):
        """
        Fetch the progress dictionary for a user.

        Args:
            username: The username whose progress to retrieve.

        Returns:
            A dict with the user's progress data, or an empty dict if not found.
        """
        with self._lock:
            row = self._conn.execute(
                "SELECT progress FROM users WHERE username = ?", (username,)
            ).fetchone()
        if row is None:
            return {}
        try:
            return json.loads(row[0])
        except (json.JSONDecodeError, TypeError):
            return {}

    def save_progress(self, username, progress_dict):
        """
        Persist a user's progress dictionary to the database.

        Args:
            username: The username whose progress to update.
            progress_dict: The progress data to store.
        """
        with self._lock:
            self._conn.execute(
                "UPDATE users SET progress = ? WHERE username = ?",
                (json.dumps(progress_dict), username),
            )
            self._conn.commit()
