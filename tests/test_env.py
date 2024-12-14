# test_env.py
# Author: William Richmond
# Date: 2024-12-01
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Verifies that environment variables are loaded successfully using python-dotenv.
# Revised on: 2024-12-01

import os
from dotenv import load_dotenv

# Function: test_env_variables
# Purpose: Tests the loading of environment variables from the .env file.
# Inputs: None
# Returns: None
def test_env_variables():
    """
    Verifies that environment variables are successfully loaded from the .env file.
    """
    # Load environment variables
    load_dotenv()

    # Fetch variables
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    # Print results
    print("SMTP_SERVER:", smtp_server)
    print("SMTP_PORT:", smtp_port)
    print("SENDER_EMAIL:", sender_email)
    print("SENDER_PASSWORD:", "********")  # Mask the actual password
    print("RECIPIENT_EMAIL:", recipient_email)

    # Assert variables are loaded
    assert smtp_server, "SMTP_SERVER is not loaded."
    assert smtp_port, "SMTP_PORT is not loaded."
    assert sender_email, "SENDER_EMAIL is not loaded."
    assert sender_password, "SENDER_PASSWORD is not loaded."
    assert recipient_email, "RECIPIENT_EMAIL is not loaded."

# Entry point for testing environment variables
if __name__ == "__main__":
    test_env_variables()
