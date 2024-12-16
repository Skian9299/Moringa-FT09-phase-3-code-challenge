import sqlite3
from typing import Any

class Connection:
    _db_connection = None

    @classmethod
    def get_db_connection(cls) -> sqlite3.Connection:
        """Return a database connection. Create one if it doesn't exist."""
        if cls._db_connection is None:
            cls._db_connection = sqlite3.connect("your_database_name.db")  # Replace with your DB name
            cls._db_connection.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
        return cls._db_connection

    @classmethod
    def close_connection(cls):
        """Close the database connection."""
        if cls._db_connection:
            cls._db_connection.close()
            cls._db_connection = None