# main.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Main script for SecureFileGuard. Integrates file upload, malware scanning, encryption, and notifications.
# Revised on: 2024-11-17

import logging
import os
from src.file_upload import upload_file
from src.malware_scan import scan_file
from src.encryption import encrypt_file
from src.notification import send_email_notification

# Ensure the logs directory exists
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_directory, 'main.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function: main
# Purpose: Main function that coordinates the file upload, malware scan, encryption, and notifications.
# Inputs: None (user input for file path)
# Returns: None
def main():
    try:
        # Step 1: File Upload
        print("Starting file upload...")
        file_path = input("Enter the path of the file to upload: ")
        upload_results = upload_file(file_path)
        logging.info(f"Upload Results: {upload_results}")

        if upload_results['status'] != 'success':
            print(f"Upload failed: {upload_results['message']}")
            return

        print(f"File uploaded successfully: {upload_results['file']}")

        # Step 2: Malware Scan
        print("Scanning file for malware...")
        scan_results = scan_file(upload_results['file'])
        logging.info(f"Scan Results: {scan_results}")

        if scan_results['status'] == 'infected':
            print(f"File is infected: {scan_results['threat']}")
            subject = "Malware Alert: Infected File Detected"
            message = f"An infected file was detected: {upload_results['file']}\nThreat: {scan_results['threat']}"
            notification_result = send_email_notification(subject, message, os.getenv("RECIPIENT_EMAIL"))
            print(f"Notification sent: {notification_result}")
            return

        print("File is clean, proceeding to encryption...")

        # Step 3: Encrypt the File
        with open(upload_results['file'], 'rb') as file:
            file_data = file.read()

        encryption_key = b'Sixteen byte key'  # AES key must be 16, 24, or 32 bytes
        encrypted_data = encrypt_file(file_data, encryption_key)

        encrypted_file_path = upload_results['file'] + ".enc"
        with open(encrypted_file_path, 'wb') as enc_file:
            enc_file.write(encrypted_data)

        logging.info(f"File encrypted and saved as: {encrypted_file_path}")
        print(f"File successfully encrypted: {encrypted_file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

# Example usage (for running the script directly)
if __name__ == "__main__":
    main()
