# test_notification.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Unit tests for the notification module of SecureFileGuard.
# Revised on: 2024-11-17

import unittest
from unittest.mock import patch, MagicMock
from src.notification import send_email_notification
import smtplib

class TestNotification(unittest.TestCase):
    """Unit tests for send_email_notification function."""

    # Function: test_send_email_notification_failure
    # Purpose: Tests failure case for email sending with SMTPException.
    # Inputs: Mocked send_message method, subject, message, and recipient email.
    # Returns: Asserts False when SMTPException is raised.
    @patch("smtplib.SMTP.send_message", side_effect=smtplib.SMTPException("Mock SMTP failure"))
    def test_send_email_notification_failure(self, mock_send):
        print("\nRunning test_send_email_notification_failure...")
        result = send_email_notification(
            "Test Failure Subject", "Test Failure Message", "admin@example.com"
        )
        print(f"Test result (failure case): {result}")
        self.assertFalse(result, "Expected False when SMTPException is raised.")

    # Function: test_send_email_notification_success
    # Purpose: Tests success case for email sending.
    # Inputs: Mocked send_message method, subject, message, and recipient email.
    # Returns: Asserts True when email is sent successfully.
    @patch("smtplib.SMTP.send_message", return_value=True)
    def test_send_email_notification_success(self, mock_send):
        print("\nRunning test_send_email_notification_success...")
        result = send_email_notification(
            "Test Success Subject", "Test Success Message", "admin@example.com"
        )
        print(f"Test result (success case): {result}")
        self.assertTrue(result, "Expected True when email is sent successfully.")

if __name__ == "__main__":
    unittest.main()