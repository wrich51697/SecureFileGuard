# file_upload.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Handles file upload, validation, and saving for SecureFileGuard.
# Revised on: 2024-11-17

import os
import logging

# Ensure the logs directory exists
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_directory, 'file_upload.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function: validate_file_type
# Purpose: Validates the file type against a list of allowed extensions.
# Inputs: file_path (str)
# Returns: bool
def validate_file_type(file_path: str) -> bool:
    allowed_extensions = {'.txt', '.pdf', '.docx'}
    _, extension = os.path.splitext(file_path)
    if extension.lower() in allowed_extensions:
        logging.info(f"File type {extension} is valid.")
        return True
    else:
        logging.warning(f"File type {extension} is not supported.")
        return False

# Function: validate_file_size
# Purpose: Validates the file size against a maximum allowed size.
# Inputs: file_path (str), max_size (int)
# Returns: bool
def validate_file_size(file_path: str, max_size: int = 10 * 1024 * 1024) -> bool:
    file_size = os.path.getsize(file_path)
    if file_size <= max_size:
        logging.info(f"File size {file_size} bytes is within the allowed limit.")
        return True
    else:
        logging.warning(f"File size {file_size} bytes exceeds the maximum limit of {max_size} bytes.")
        return False

# Function: upload_file
# Purpose: Handles the upload process, validating the file before saving it.
# Inputs: file_path (str)
# Returns: dict
def upload_file(file_path: str) -> dict:
    upload_results = {
        "file": file_path,
        "status": "unknown",
        "message": None
    }

    if not os.path.isfile(file_path):
        logging.error(f"File not found: {file_path}")
        upload_results["status"] = "error"
        upload_results["message"] = "File not found"
        return upload_results

    if not validate_file_type(file_path):
        upload_results["status"] = "error"
        upload_results["message"] = "Unsupported file type"
        return upload_results

    if not validate_file_size(file_path):
        upload_results["status"] = "error"
        upload_results["message"] = "File size exceeds limit"
        return upload_results

    try:
        destination_path = os.path.join('uploads', os.path.basename(file_path))
        with open(file_path, 'rb') as file_data:
            save_file(file_data.read(), destination_path)
        upload_results["status"] = "success"
        upload_results["message"] = "File uploaded successfully"
        logging.info(f"File uploaded to {destination_path}")
    except Exception as e:
        upload_results["status"] = "error"
        upload_results["message"] = str(e)
        logging.error(f"Error uploading file: {e}")

    return upload_results

# Function: save_file
# Purpose: Saves the file data to the specified destination path.
# Inputs: file_data (bytes), destination_path (str)
# Returns: None
def save_file(file_data: bytes, destination_path: str) -> None:
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(destination_path, 'wb') as file:
        file.write(file_data)
    logging.info(f"File saved to {destination_path}")

# Entry point for testing (for development purposes)
if __name__ == "__main__":
    # Example file path for testing
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_file = os.path.join(project_root, "resources", "sample1.txt")
    results = upload_file(test_file)
    print(f"Upload Results: {results}")
