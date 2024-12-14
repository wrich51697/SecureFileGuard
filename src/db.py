# db.py
# Author: William Richmond
# Date: 2024-11-21
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Handles database initialization and operations for SecureFileGuard, including metadata storage,
#              integrity checks, advanced security measures, and audit log management.
# Revised on: 2024-12-08

import sqlite3
from datetime import datetime, timedelta
from src.logger_config import LoggerConfig

# Initialize logger for this module
logger = LoggerConfig(name="db", log_filename="db.log").get_logger()


class DatabaseManager:
    """
    A class to manage database operations for SecureFileGuard.
    """

    MAX_AUDIT_LOG_ENTRIES = 1000  # Retain only the last 1000 audit log rows

    # Function: __init__
    # Purpose: Initializes the DatabaseManager class with the given database path.
    # Inputs:
    #   - db_path (str): Path to the SQLite database file.
    # Returns: None
    def __init__(self, db_path: str):
        self.db_path = db_path

    # Function: initialize_database
    # Purpose: Ensures the SQLite database and required tables are created.
    # Inputs:
    #   - is_secure_storage (bool): Indicates if this is for secure storage.
    # Returns: None
    def initialize_database(self, is_secure_storage: bool = False):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if is_secure_storage:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS secure_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_filename TEXT NOT NULL,
                    file_data BLOB NOT NULL,
                    encryption_key_hash TEXT NOT NULL,
                    upload_time TEXT NOT NULL
                )
            ''')
            else:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS uploaded_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_filename TEXT NOT NULL,
                    file_size INTEGER,
                    upload_time TEXT,
                    encryption_key_hash TEXT NOT NULL,
                    encrypted_file_path TEXT
                )
            ''')
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    details TEXT,
                    status TEXT NOT NULL,
                    log_level TEXT NOT NULL
                )
            ''')
                cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_upload_time ON uploaded_files(upload_time)
            ''')

            conn.commit()
            conn.close()
            logger.info(f"Database initialized and updated: {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise


    # Function: store_metadata
    # Purpose: Stores file metadata in the metadata database.
    # Inputs:
    #   - metadata (dict): Metadata dictionary for the uploaded file.
    # Returns: None
    def store_metadata(self, metadata: dict):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO uploaded_files (
                    original_filename,
                    file_size,
                    upload_time,
                    encryption_key_hash,
                    encrypted_file_path
                )
                VALUES (?, ?, ?, ?, ?)
            ''', (
                metadata['original_filename'],
                metadata['file_size'],
                metadata['upload_time'],
                metadata['encryption_key_hash'],
                metadata.get('encrypted_file_path', None)
            ))
            conn.commit()
            conn.close()
            logger.info(f"Metadata stored: {metadata}")
        except Exception as e:
            logger.error(f"Error storing metadata: {e}")
            raise

    # Function: initialize
    # Purpose: Wrapper method for initialize_database to align with references in main.py.
    # Inputs:
    #   - is_secure_storage (bool): Indicates if this is for secure storage.
    # Returns: None
    def initialize(self, is_secure_storage: bool = False):
        self.initialize_database(is_secure_storage)

    # Function: store_secure_file
    # Purpose: Stores encrypted file data in the secure storage database.
    # Inputs:
    #   - file_data (bytes): Encrypted file content.
    #   - metadata (dict): Metadata dictionary for the uploaded file.
    # Returns: None
    def store_secure_file(self, file_data: bytes, metadata: dict):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO secure_files (
                    original_filename,
                    file_data,
                    encryption_key_hash,
                    upload_time
                )
                VALUES (?, ?, ?, ?)
            ''', (
                metadata['original_filename'],
                file_data,
                metadata['encryption_key_hash'],
                metadata['upload_time']
            ))
            conn.commit()
            conn.close()
            logger.info(f"Encrypted file stored: {metadata['original_filename']}")
        except Exception as e:
            logger.error(f"Error storing secure file: {e}")
            raise

    # Function: log_audit_event
    # Logs critical actions into the audit log with proper log levels.
    # Inputs:
    #   - operation (str): The operation being logged.
    #   - details (str): Additional details about the operation.
    #   - status (str): The status of the operation ('success' or 'failure').
    #   - log_level (str): The log level ('info', 'warning', 'error').
    # Returns: None
    def log_audit_event(self, operation: str, details: str, status: str = "success", log_level: str = "info"):
        try:
            # Map log_level to actual logging methods
            log_methods = {
                "info": logger.info,
                "warning": logger.warning,
                "error": logger.error,
                "debug": logger.debug
            }
            log_method = log_methods.get(log_level, logger.info)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO audit_log (operation, timestamp, details, status, log_level)
            VALUES (?, ?, ?, ?, ?)
        ''', (operation, datetime.now().isoformat(), details, status, log_level))
            conn.commit()
            conn.close()

            # Log to console and file
            log_method(f"Audit event logged: {operation}, Status: {status}, Level: {log_level}")
        except Exception as e:
            logger.error(f"Error logging audit event: {e}")
            raise

    # Function: fetch_audit_logs
    # Purpose: Fetches all records from the audit_log table.
    # Inputs: None
    # Returns: list - A list of tuples representing the rows in the audit_log table.
    def fetch_audit_logs(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM audit_log")
            records = cursor.fetchall()
            conn.close()
            return records
        except Exception as e:
            logger.error(f"Error fetching audit logs: {e}")
            raise

    # Function: validate_database_integrity
    # Purpose: Validates the database's integrity.
    # Inputs: None
    # Returns: bool - True if the database passes integrity check, False otherwise.
    def validate_database_integrity(self) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check;")
            result = cursor.fetchone()
            conn.close()
            if result and result[0] == "ok":
                logger.info("Database integrity check passed.")
                return True
            else:
                logger.error("Database integrity check failed.")
                return False
        except Exception as e:
            logger.error(f"Error during integrity check: {e}")
            return False

    # Function: archive_old_metadata
    # Purpose: Archives old records from the metadata database.
    # Inputs:
    #   - days (int): The number of days to retain records.
    # Returns: None
    def archive_old_metadata(self, days: int = 90):
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM uploaded_files WHERE upload_time < ?", (cutoff_date.isoformat(),))
            conn.commit()
            conn.close()
            logger.info(f"Archived metadata older than {days} days.")
        except Exception as e:
            logger.error(f"Error archiving metadata: {e}")
            raise

# Example usage
if __name__ == "__main__":

    logger = LoggerConfig("db", "db.log").get_logger()
    logger.info("Test log entry for db.py")