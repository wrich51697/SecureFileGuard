# test_file_upload.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Unit tests for the file upload module of SecureFileGuard.
# Revised on: 2024-12-01
import shutil
import unittest
import os
from unittest.mock import patch
from src.file_upload import FileUploader
from src.db import initialize_database


class TestFileUpload(unittest.TestCase):
    """Unit tests for the FileUploader class."""

    # Function: setUpClass
    # Purpose: Sets up the test environment by defining test file paths and creating sample test files.
    # Inputs: None
    # Returns: None
    @classmethod
    def setUpClass(cls):
        """Setup for tests: define test file paths, create test files, and initialize the database."""
        # Initialize the database
        initialize_database()

        # Define test file paths and create test files
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.valid_file = os.path.join(project_root, "resources", "sample1.txt")
        cls.large_file = os.path.join(project_root, "resources", "large_sample.txt")
        cls.unsupported_file = os.path.join(project_root, "resources", "sample.exe")

        # Create a valid sample file
        with open(cls.valid_file, 'w') as f:
            f.write("This is a valid test file for SecureFileGuard.")

        # Create a large sample file (15 MB)
        with open(cls.large_file, 'wb') as f:
            f.write(b'\0' * (15 * 1024 * 1024))  # 15 MB file

        # Create an unsupported sample file
        with open(cls.unsupported_file, 'w') as f:
            f.write("This is an unsupported file type.")

    # Function: tearDownClass
    # Purpose: Cleans up the test environment by deleting sample test files.
    # Inputs: None
    # Returns: None
    @classmethod
    def tearDownClass(cls):
        """Cleanup after tests: remove test files."""
        os.remove(cls.valid_file)
        os.remove(cls.large_file)
        os.remove(cls.unsupported_file)

    # Function: setUp
    # Purpose: Initializes the FileUploader instance for use in each test.
    # Inputs: None
    # Returns: None
    def setUp(self):
        """Set up the FileUploader instance for each test."""
        self.uploader = FileUploader()

    # Function: test_valid_file_upload
    # Purpose: Tests uploading a valid file and ensures it is processed successfully.
    # Inputs: None
    # Returns: None
    @patch("src.file_upload.FileUploader.save_to_sandbox")
    def test_valid_file_upload(self, mock_save_to_sandbox):
        """Test uploading a valid file."""
        mock_save_to_sandbox.return_value = "sandbox/sample1.txt"  # Mocked sandbox path
        result = self.uploader.upload_file(self.valid_file)
        self.assertEqual(result["status"], "success", "Expected file upload to succeed.")
        self.assertIn("sandbox_path", result, "Sandbox path missing from result.")
        self.assertEqual(result["sandbox_path"], "sandbox/sample1.txt", "Unexpected sandbox path.")

    # Function: test_unsupported_file_type
    # Purpose: Tests uploading a file with an unsupported file extension.
    # Inputs: None
    # Returns: None
    def test_unsupported_file_type(self):
        """Test uploading a file with an unsupported extension."""
        result = self.uploader.upload_file(self.unsupported_file)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Unsupported file type")

    # Function: test_file_size_exceeds_limit
    # Purpose: Tests uploading a file that exceeds the maximum allowed size.
    # Inputs: None
    # Returns: None
    def test_file_size_exceeds_limit(self):
        """Test uploading a file that exceeds the size limit."""
        result = self.uploader.upload_file(self.large_file)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "File size exceeds limit")

    # Function: test_missing_file
    # Purpose: Tests handling a missing file during the upload process.
    # Inputs: None
    # Returns: None
    def test_missing_file(self):
        """Test uploading a file that does not exist."""
        missing_file = os.path.join(os.path.dirname(self.valid_file), "missing.txt")
        result = self.uploader.upload_file(missing_file)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "File not found")

    # Function: test_encryption_failure
    # Purpose: Tests handling an encryption failure during the upload process.
    # Inputs: None
    # Returns: None
    @patch("src.file_upload.FileUploader.encrypt_and_store", side_effect=Exception("Encryption failed"))
    def test_encryption_failure(self, mock_encrypt_and_store):
        """Test handling encryption failure during file upload."""
        result = self.uploader.upload_file(self.valid_file)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Encryption failed")

    # Function: test_database_failure
    # Purpose: Tests handling a database failure during the metadata storage process.
    # Inputs: None
    # Returns: None
    @patch("src.file_upload.FileUploader.store_metadata", side_effect=Exception("Database error"))
    def test_database_failure(self, mock_store_metadata):
        """Test handling database failure during metadata storage."""
        result = self.uploader.upload_file(self.valid_file)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Database error")

    # Function: test_missing_sandbox_directory
    # Purpose: Tests behavior when the sandbox directory is missing during the upload process.
    # Inputs: None
    # Returns: None
    def test_missing_sandbox_directory(self):
        """Test behavior when the sandbox directory is missing."""
        sandbox_dir = self.uploader.sandbox_dir
        if os.path.exists(sandbox_dir):
            shutil.rmtree(sandbox_dir)  # Recursively remove sandbox directory

        result = self.uploader.upload_file(self.valid_file)
        self.assertEqual(result["status"], "error", "Expected error status when sandbox directory is missing.")

        # Recreate the sandbox directory for other tests
        os.makedirs(sandbox_dir, exist_ok=True)

    # Function: test_missing_encryption_key
    # Purpose: Tests behavior when the ENCRYPTION_KEY environment variable is not set.
    # Inputs: None
    # Returns: None
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_encryption_key(self):
        """Test behavior when ENCRYPTION_KEY environment variable is not set."""
        # Since a fallback is used, the test will check for successful handling
        result = self.uploader.upload_file(self.valid_file)
        self.assertEqual(result["status"], "success", "Expected file upload to succeed with default encryption key.")
        print(f"Test missing encryption key results: {result}")

# Entry point for running the unit tests
if __name__ == "__main__":
    unittest.main()
