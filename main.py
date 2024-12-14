# main.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: CLI for SecureFileGuard. Uses centralized logic from processing.py.
# Revised on: 2024-12-08

from src.core.processing import process_file, print_colored
from src.db import DatabaseManager

def main():
    try:
        metadata_manager = DatabaseManager("file_metadata.db")
        secure_storage_manager = DatabaseManager("secure_storage.db")
        metadata_manager.initialize()
        secure_storage_manager.initialize(is_secure_storage=True)

        file_path = input("Enter the path of the file to upload: ").strip()
        result = process_file(metadata_manager, secure_storage_manager, file_path)
    except Exception as e:
        print_colored(f"An error occurred: {e}", "error")

if __name__ == "__main__":
    main()
