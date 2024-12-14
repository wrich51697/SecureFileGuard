# file_upload.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Handles file upload, validation, and saving with enhanced security features for SecureFileGuard.
# Revised on: 2024-12-08

import os
import hashlib
from datetime import datetime
from src.encryption import encrypt_file, generate_key
from src.db import DatabaseManager
from src.logger_config import LoggerConfig

# Initialize logger for this module
logger = LoggerConfig(name="file_upload", log_filename="file_upload.log").get_logger()

# Set sandbox directory relative to the project root
sandbox_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sandbox")
os.makedirs(sandbox_directory, exist_ok=True)


class FileUploader:
    """Handles file uploads, validations, and secure storage."""

    # Function: __init__
    # Purpose: Initializes the FileUploader class and ensures required directories exist.
    # Inputs:
    #   - metadata_manager (DatabaseManager): Instance of DatabaseManager for metadata operations.
    #   - sandbox_dir (str): Path to the sandbox directory.
    # Returns: None
    def __init__(self, metadata_manager: DatabaseManager, sandbox_dir=sandbox_directory):
        self.metadata_manager = metadata_manager
        self.sandbox_dir = sandbox_dir

    # Function: validate_file_type
    # Purpose: Validates the file type against a list of allowed extensions.
    # Inputs: file_path (str) - Path of the file to validate.
    # Returns: bool - True if the file type is allowed; otherwise, False.
    @staticmethod
    def validate_file_type(file_path: str) -> bool:
        allowed_extensions = {'.txt', '.pdf', '.docx'}
        _, extension = os.path.splitext(file_path)
        if extension.lower() in allowed_extensions:
            logger.info(f"File type {extension} is valid.")
            return True
        else:
            logger.warning(f"File type {extension} is not supported.")
            return False

    # Function: validate_file_size
    # Purpose: Validates the file size against a maximum allowed size.
    # Inputs: file_path (str) - Path of the file to validate.
    #         max_size (int) - Maximum allowed file size in bytes.
    # Returns: bool - True if the file size is within the allowed limit; otherwise, False.
    @staticmethod
    def validate_file_size(file_path: str, max_size: int = 10 * 1024 * 1024) -> bool:
        file_size = os.path.getsize(file_path)
        if file_size <= max_size:
            logger.info(f"File size {file_size} bytes is within the allowed limit.")
            return True
        else:
            logger.warning(f"File size {file_size} bytes exceeds the maximum limit of {max_size} bytes.")
            return False

    # Function: generate_file_hash
    # Purpose: Generates a hash for the file content using SHA-256.
    # Inputs: file_data (bytes) - File content in bytes.
    # Returns: str - SHA-256 hash of the file.
    @staticmethod
    def generate_file_hash(file_data: bytes) -> str:
        file_hash = hashlib.sha256(file_data).hexdigest()
        logger.info(f"Generated file hash: {file_hash}")
        return file_hash

    # Function: save_to_sandbox
    # Purpose: Saves the file to the sandbox directory for scanning.
    # Inputs: file_data (bytes) - File content in bytes.
    #         file_name (str) - Name of the file to save.
    # Returns: str - Full path to the saved file in the sandbox.
    def save_to_sandbox(self, file_data: bytes, file_name: str) -> str:
        file_path = os.path.join(self.sandbox_dir, file_name)
        with open(file_path, 'wb') as file:
            file.write(file_data)
        normalized_path = os.path.normpath(file_path)
        logger.info(f"File saved to sandbox: {normalized_path}")

        return file_path

    # Function: encrypt_and_store
    # Purpose: Encrypts the file and stores metadata in the database.
    # Inputs: file_data (bytes) - File content in bytes.
    #         file_name (str) - Original name of the file.
    # Returns: dict - Contains the encrypted file path and encryption key details.
    def encrypt_and_store(self, file_data: bytes, file_name: str) -> dict:
        try:
            encryption_key, salt = generate_key(os.getenv("ENCRYPTION_KEY", "SecurePass123"))
            encrypted_data = encrypt_file(file_data, encryption_key)
            encrypted_file_path = self.save_to_sandbox(encrypted_data, file_name + ".enc")
            normalized_path = os.path.normpath(encrypted_file_path)
            logger.info(f"File encrypted and saved: {normalized_path}")


            return {
                "encrypted_file_path": encrypted_file_path,
                "encryption_key_hash": hashlib.sha256(encryption_key).hexdigest(),
                "salt": salt
            }
        except Exception as e:
            logger.error(f"Error during encryption: {e}")
            raise

    # Function: upload_file
    # Purpose: Handles the upload process, validating, encrypting, and storing the file.
    # Inputs: file_path (str) - Path of the file to upload.
    # Returns: dict - Contains the upload status, message, and sandbox path if successful.
    def upload_file(self, file_path: str) -> dict:
        upload_results = {
            "file": file_path,
            "status": "unknown",
            "message": None
        }

        if not os.path.isfile(file_path):
            normalized_path = os.path.normpath(file_path)
            logger.error(f"File not found: {normalized_path}")

            upload_results["status"] = "error"
            upload_results["message"] = "File not found"
            return upload_results

        if not self.validate_file_type(file_path):
            upload_results["status"] = "error"
            upload_results["message"] = "Unsupported file type"
            return upload_results

        if not self.validate_file_size(file_path):
            upload_results["status"] = "error"
            upload_results["message"] = "File size exceeds limit"
            return upload_results

        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            encryption_results = self.encrypt_and_store(file_data, os.path.basename(file_path))

            metadata = {
                "original_filename": os.path.basename(file_path),
                "file_size": os.path.getsize(file_path),
                "upload_time": datetime.now().isoformat(),
                "file_hash": self.generate_file_hash(file_data),
                **encryption_results
            }

            self.metadata_manager.store_metadata(metadata)

            upload_results["status"] = "success"
            upload_results["message"] = "File uploaded successfully"
            upload_results["sandbox_path"] = encryption_results["encrypted_file_path"]
        except Exception as e:
            upload_results["status"] = "error"
            upload_results["message"] = str(e)
            logger.error(f"Error during file upload: {e}")

        return upload_results

if __name__ == "__main__":
    logger = LoggerConfig("file_upload", "file_upload.log").get_logger()
    logger.info("Test log entry for file_upload.py")
