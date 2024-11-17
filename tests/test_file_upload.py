# test_file_upload.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Unit tests for the file upload module of SecureFileGuard.

import unittest
import os
from src.file_upload import upload_file, validate_file_type, validate_file_size

class TestFileUpload(unittest.TestCase):
    # Function: setUpClass
    # Purpose: Sets up the test environment, creating sample test files.
    # Inputs: None
    # Returns: None
    @classmethod
    def setUpClass(cls):
        """Setup for tests: define test file paths and create test files."""
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
    # Purpose: Cleans up the test environment by deleting the sample test files.
    # Inputs: None
    # Returns: None
    @classmethod
    def tearDownClass(cls):
        """Cleanup after tests: remove test files."""
        os.remove(cls.valid_file)
        os.remove(cls.large_file)
        os.remove(cls.unsupported_file)

    # Function: test_valid_file_upload
    # Purpose: Tests uploading a valid file to ensure it is processed successfully.
    # Inputs: None
    # Returns: None
    def test_valid_file_upload(self):
        """Test uploading a valid file."""
        result = upload_file(self.valid_file)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "File uploaded successfully")
        print(f"Test valid file upload results: {result}")

    # Function: test_unsupported_file_type
    # Purpose: Tests uploading a file with an unsupported extension.
    # Inputs: None
    # Returns: None
    def test_unsupported_file_type(self):
        """Test uploading a file with an unsupported extension."""
        result = upload_file(self.unsupported_file)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Unsupported file type")
        print(f"Test unsupported file type results: {result}")

    # Function: test_file_size_exceeds_limit
    # Purpose: Tests uploading a file that exceeds the maximum allowed size.
    # Inputs: None
    # Returns: None
    def test_file_size_exceeds_limit(self):
        """Test uploading a file that exceeds the size limit."""
        result = upload_file(self.large_file)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "File size exceeds limit")
        print(f"Test file size exceeds limit results: {result}")

    # Function: test_missing_file
    # Purpose: Tests handling of a missing file during upload.
    # Inputs: None
    # Returns: None
    def test_missing_file(self):
        """Test uploading a file that does not exist."""
        missing_file = os.path.join(os.path.dirname(self.valid_file), "missing.txt")
        result = upload_file(missing_file)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "File not found")
        print(f"Test missing file results: {result}")

# Entry point for running the unit tests
if __name__ == "__main__":
    unittest.main()
