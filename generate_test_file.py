# generate_test_file.py
# Author: William Richmond
# Date: 2024-12-07
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Utility script to generate a test file for SecureFileGuard.
#              This file is used to test file upload, malware scanning,
#              encryption, and secure storage workflows.
# Revised on: 2024-12-07

import os

# Function: generate_test_file
# Purpose: Creates a simple text file with dummy content for testing SecureFileGuard functionality.
# Inputs: directory (str) - Directory where the file will be created.
#         filename (str) - Name of the test file to generate.
# Returns: None
def generate_test_file(directory="resources", filename="test_file.txt"):
    """
    Generates a simple text file with dummy content for testing SecureFileGuard.
    :param directory: Directory where the file will be created.
    :param filename: Name of the test file.
    """
    os.makedirs(directory, exist_ok=True)  # Ensure the resources directory exists
    file_path = os.path.join(directory, filename)

    content = """This is a test file for SecureFileGuard.
It is used to test file upload, malware scanning, encryption, and secure storage functionality.
"""

    with open(file_path, 'w') as file:
        file.write(content)

    print(f"Test file generated at: {file_path}")

# Entry point for generating the test file
if __name__ == "__main__":
    generate_test_file()
