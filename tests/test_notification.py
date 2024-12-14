# test_notification.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Unit tests for the NotificationManager class of SecureFileGuard.
# Revised on: 2024-12-07

import os
import unittest
from unittest.mock import patch
from src.notification import NotificationManager
import smtplib


class TestNotificationManager(unittest.TestCase):
    """Unit tests for the NotificationManager class."""

    # Function: setUp
    # Purpose: Initializes the NotificationManager instance for use in each test.
    # Inputs: None
    # Returns: None
    @patch.dict(
        os.environ,
        {
            "SMTP_SERVER": "smtp.gmail.com",
            "SMTP_PORT": "587",
            "SENDER_EMAIL": "testsender@gmail.com",
            "SENDER_PASSWORD": "testpassword",
            "RECIPIENT_EMAIL": "testrecipient@gmail.com"
        }
    )
    def setUp(self):
        """Set up NotificationManager for tests."""
        self.notification_manager = NotificationManager()

    # Function: test_load_email_config
    # Purpose: Tests loading email configuration from environment variables.
    # Inputs: Mocked environment variables.
    # Returns: Asserts correct values are loaded.
    @patch.dict(
        os.environ,
        {
            "SMTP_SERVER": "smtp.gmail.com",
            "SMTP_PORT": "587",
            "SENDER_EMAIL": "testsender@gmail.com",
            "SENDER_PASSWORD": "testpassword",
            "RECIPIENT_EMAIL": "testrecipient@gmail.com"
        }
    )
    def test_load_email_config(self):
        """Test loading email configuration."""
        config = self.notification_manager.config
        self.assertEqual(config["smtp_server"], "smtp.gmail.com")
        self.assertEqual(config["smtp_port"], 587)
        self.assertEqual(config["sender_email"], "testsender@gmail.com")
        self.assertEqual(config["recipient_email"], "testrecipient@gmail.com")

    # Function: test_send_email_failure
    # Purpose: Tests failure case for email sending with SMTPException.
    # Inputs: Mocked send_message method, subject, message, and recipient email.
    # Returns: Asserts False when SMTPException is raised.
    @patch("smtplib.SMTP.send_message", side_effect=smtplib.SMTPException("Mock SMTP failure"))
    def test_send_email_failure(self, mock_send):
        """Test failure case for sending email."""
        result = self.notification_manager.send_email(
            "Test Failure Subject", "Test Failure Message", "admin@example.com"
        )
        self.assertFalse(result, "Expected False when SMTPException is raised.")

    # Function: test_send_email_success
    # Purpose: Tests success case for email sending.
    # Inputs: Mocked send_message method, subject, message, and recipient email.
    # Returns: Asserts True when email is sent successfully.
    @patch("smtplib.SMTP")
    def test_send_email_success(self, mock_smtp):
        """Test success case for sending email."""
        mock_server = mock_smtp.return_value  # Mock the SMTP server instance
        mock_server.send_message.return_value = None  # Simulate successful send_message

        result = self.notification_manager.send_email(
        "Test Success Subject", "Test Success Message", "admin@example.com"
        )
        print(f"Mock send_message called: {mock_server.send_message.called}")
        print(f"Result: {result}")
        self.assertTrue(result, "Expected True when email is sent successfully.")

    # Function: test_missing_environment_variables
    # Purpose: Tests behavior when required environment variables are missing.
    # Inputs: Empty environment variables.
    # Returns: Asserts ValueError is raised.
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_environment_variables(self):
        """Test behavior when environment variables are missing."""
        with self.assertRaises(ValueError):
            NotificationManager()


if __name__ == "__main__":
    unittest.main()
