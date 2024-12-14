# test_db.py
# Author: William Richmond
# Date: 2024-12-01
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Unit tests for the database operations of SecureFileGuard, utilizing the DatabaseManager class.
# Revised on: 2024-12-08

import os
import unittest
from datetime import datetime, timedelta

from src.db import DatabaseManager


class TestDatabaseOperations(unittest.TestCase):
    """Unit tests for database operations."""

    TEST_METADATA_DB_PATH = "test_file_metadata.db"
    TEST_SECURE_STORAGE_DB_PATH = "test_secure_storage.db"

    # Function: setUp
    # Purpose: Sets up fresh databases for testing.
    # Inputs: None
    # Returns: None
    def setUp(self):
        """Set up fresh databases for testing."""
        self.metadata_manager = DatabaseManager(self.TEST_METADATA_DB_PATH)
        self.secure_storage_manager = DatabaseManager(self.TEST_SECURE_STORAGE_DB_PATH)

        for db_manager in [self.metadata_manager, self.secure_storage_manager]:
            if os.path.exists(db_manager.db_path):
                os.remove(db_manager.db_path)

        self.metadata_manager.initialize_database()
        self.secure_storage_manager.initialize_database(is_secure_storage=True)

    # Function: tearDown
    # Purpose: Removes test databases after tests.
    # Inputs: None
    # Returns: None
    def tearDown(self):
        """Remove the test databases after tests."""
        for db_manager in [self.metadata_manager, self.secure_storage_manager]:
            if os.path.exists(db_manager.db_path):
                os.remove(db_manager.db_path)

    # Function: test_initialize_metadata_database
    # Purpose: Tests if the metadata database initializes correctly.
    # Inputs: None
    # Returns: None
    def test_initialize_metadata_database(self):
        """Tests if the metadata database initializes correctly."""
        self.assertTrue(self.metadata_manager.validate_database_integrity(), "Metadata database integrity check failed.")

    # Function: test_initialize_secure_storage_database
    # Purpose: Tests if the secure storage database initializes correctly.
    # Inputs: None
    # Returns: None
    def test_initialize_secure_storage_database(self):
        """Tests if the secure storage database initializes correctly."""
        self.assertTrue(self.secure_storage_manager.validate_database_integrity(), "Secure storage database integrity check failed.")

    # Function: test_store_and_fetch_metadata
    # Purpose: Tests storing and fetching metadata functionality in the metadata database.
    # Inputs: None
    # Returns: None
    def test_store_and_fetch_metadata(self):
        """Tests storing and fetching metadata functionality."""
        metadata = {
            "original_filename": "test_file.txt",
            "file_size": 1024,
            "upload_time": datetime.now().isoformat(),
            "encryption_key_hash": "dummyhash123",
            "encrypted_file_path": "/path/to/encrypted/test_file.txt",
        }
        self.metadata_manager.store_metadata(metadata)

        records = self.metadata_manager.fetch_all("uploaded_files")
        self.assertEqual(len(records), 1, "Metadata was not stored in the metadata database.")

    # Function: test_store_and_fetch_secure_file
    # Purpose: Tests storing and fetching encrypted file data in the secure storage database.
    # Inputs: None
    # Returns: None
    def test_store_and_fetch_secure_file(self):
        """Tests storing and fetching encrypted file data."""
        file_data = b"Encrypted file content"
        metadata = {
            "original_filename": "secure_test_file.txt",
            "encryption_key_hash": "securehash123",
            "upload_time": datetime.now().isoformat(),
        }
        self.secure_storage_manager.store_secure_file(file_data, metadata)

        records = self.secure_storage_manager.fetch_all("secure_files")
        self.assertEqual(len(records), 1, "Encrypted file was not stored in the secure storage database.")

    # Function: test_log_audit_event
    # Purpose: Tests if audit events are logged correctly in the metadata database.
    # Inputs: None
    # Returns: None
    def test_log_audit_event(self):
        """Tests if audit events are logged correctly."""
        self.metadata_manager.log_audit_event("TEST_OPERATION", "Test details")

        records = self.metadata_manager.fetch_all("audit_log")
        self.assertEqual(len(records), 1, "Audit event was not logged.")

    # Function: test_archive_old_metadata
    # Purpose: Tests archiving old metadata in the metadata database.
    # Inputs: None
    # Returns: None
    def test_archive_old_metadata(self):
        """Tests archiving old metadata."""
        metadata_old = {
            "original_filename": "old_file.txt",
            "file_size": 512,
            "upload_time": (datetime.now() - timedelta(days=100)).isoformat(),
            "encryption_key_hash": "oldhash",
            "encrypted_file_path": "/path/to/encrypted/old_file.txt",
        }
        metadata_new = {
            "original_filename": "new_file.txt",
            "file_size": 256,
            "upload_time": datetime.now().isoformat(),
            "encryption_key_hash": "newhash",
            "encrypted_file_path": "/path/to/encrypted/new_file.txt",
        }
        self.metadata_manager.store_metadata(metadata_old)
        self.metadata_manager.store_metadata(metadata_new)

        self.metadata_manager.archive_old_metadata(90)

        records = self.metadata_manager.fetch_all("uploaded_files")
        self.assertEqual(len(records), 1, "Old records were not archived correctly.")

    # Function: test_validate_database_integrity
    # Purpose: Ensures integrity validation works correctly for both databases.
    # Inputs: None
    # Returns: None
    def test_validate_database_integrity(self):
        """Ensures integrity validation works correctly for both databases."""
        self.assertTrue(self.metadata_manager.validate_database_integrity(), "Metadata database integrity validation failed.")
        self.assertTrue(self.secure_storage_manager.validate_database_integrity(), "Secure storage database integrity validation failed.")


if __name__ == "__main__":
    unittest.main()
