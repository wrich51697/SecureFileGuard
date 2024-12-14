# src/core/processing.py
# Author: William Richmond
# Date: 2024-12-08
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Centralized processing logic for SecureFileGuard workflows.
# Revised on: 2024-12-08

import os
import hashlib
from datetime import datetime
from colorama import Fore, Style, init
from src.file_upload import FileUploader
from src.malware_scan import MalwareScanner
from src.notification import NotificationManager
from src.encryption import encrypt_file, generate_key
from src.logger_config import LoggerConfig

# Initialize Colorama for cross-platform compatibility
init()

# Initialize logger for this module
logger = LoggerConfig(name="processing", log_filename="processing.log").get_logger()

# Function: print_colored
# Purpose: Prints messages to the terminal with colored output based on log level.
# Inputs:
#   - message (str): The message to print.
#   - level (str): The log level ("info", "warning", "error").
# Returns: None
def print_colored(message, level="info"):
    color_map = {
        "info": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED
    }
    color = color_map.get(level, Fore.WHITE)
    print(f"{color}{message}{Style.RESET_ALL}")

# Function: process_file
# Purpose: Orchestrates the full workflow: upload, scan, encrypt, store, and notify.
# Inputs:
#   - metadata_manager (DatabaseManager): Instance for metadata operations.
#   - secure_storage_manager (DatabaseManager): Instance for secure storage operations.
#   - file_path (str): Path of the file to process.
# Returns: dict - Processing results (status, message).
def process_file(metadata_manager, secure_storage_manager, file_path: str) -> dict:
    try:
        file_uploader = FileUploader(metadata_manager)
        malware_scanner = MalwareScanner()
        notification_manager = NotificationManager()

        # Step 1: File Upload
        upload_results = file_uploader.upload_file(file_path)
        if upload_results["status"] != "success":
            metadata_manager.log_audit_event("File Upload", f"Failed to upload {file_path}. Error: {upload_results['message']}", "failure")
            print_colored(f"Upload failed: {upload_results['message']}", "error")
            return {"status": "failure", "message": upload_results["message"]}

        metadata_manager.log_audit_event("File Upload", f"Uploaded {file_path} to sandbox.", "success")
        print_colored(f"File uploaded successfully: {upload_results['sandbox_path']}", "info")

        # Step 2: Malware Scan
        scan_results = malware_scanner.scan_file(upload_results["sandbox_path"])
        if scan_results["status"] == "suspicious":
            metadata_manager.log_audit_event("Malware Scan", f"Suspicious file detected: {scan_results['threat']}", "failure")
            quarantine_dir = "quarantine"
            os.makedirs(quarantine_dir, exist_ok=True)
            quarantine_path = os.path.join(quarantine_dir, os.path.basename(upload_results["sandbox_path"]))
            os.rename(upload_results["sandbox_path"], quarantine_path)
            notification_manager.send_email(
                subject="Malware Alert",
                message=f"A suspicious file was detected and quarantined: {quarantine_path}\nThreat: {scan_results['threat']}",
            )
            print_colored(f"File quarantined: {quarantine_path}", "warning")
            return {"status": "failure", "message": f"Suspicious file detected: {scan_results['threat']}"}

        metadata_manager.log_audit_event("Malware Scan", f"File scanned successfully: {file_path}", "success")
        print_colored("Malware scan passed.", "info")

        # Step 3: Encrypt the file
        with open(upload_results["sandbox_path"], 'rb') as file:
            file_data = file.read()

        encryption_key, key_salt = generate_key("SecurePassword123")
        encrypted_file_data = encrypt_file(file_data, encryption_key)
        encryption_key_hash = hashlib.sha256(encryption_key).hexdigest()

        # Metadata for file
        metadata = {
            "original_filename": os.path.basename(file_path),
            "file_size": len(file_data),
            "upload_time": datetime.now().isoformat(),
            "encryption_key_hash": encryption_key_hash,
            "encrypted_file_path": os.path.join('secure_storage', os.path.basename(file_path))
        }
        metadata_manager.store_metadata(metadata)
        secure_storage_manager.store_secure_file(encrypted_file_data, metadata)

        metadata_manager.log_audit_event("Encryption", f"File encrypted: {file_path}", "success")
        metadata_manager.log_audit_event("File Move", f"File moved to secure storage: {metadata['encrypted_file_path']}", "success")

        print_colored(f"File successfully encrypted and stored: {metadata['encrypted_file_path']}", "info")
        return {"status": "success", "message": "File processed successfully"}
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        metadata_manager.log_audit_event("Unexpected Error", str(e), "failure")
        print_colored(f"An unexpected error occurred: {e}", "error")
        return {"status": "error", "message": str(e)}
