# notification.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Provides functions for sending email notifications for SecureFileGuard.
# Revised on: 2024-12-07

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from src.logger_config import LoggerConfig

# Initialize logger for this module
logger = LoggerConfig(name="notification", log_filename="notification.log").get_logger()

# Load environment variables
load_dotenv()


class NotificationManager:
    """Handles sending email notifications."""

    # Function: __init__
    # Purpose: Initializes the NotificationManager with email configuration.
    # Inputs: None
    # Returns: None
    def __init__(self):
        self.config = self._load_email_config()

    # Function: _load_email_config
    # Purpose: Loads email configuration from environment variables.
    # Inputs: None
    # Returns: dict - Dictionary with SMTP server settings or raises ValueError.
    @staticmethod
    def _load_email_config() -> dict:
        """Load email configuration from environment variables."""
        config = {
            "smtp_server": os.getenv("SMTP_SERVER"),
            "smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "sender_email": os.getenv("SENDER_EMAIL"),
            "sender_password": os.getenv("SENDER_PASSWORD"),
            "recipient_email": os.getenv("RECIPIENT_EMAIL")
        }

        # Validate required fields
        for key, value in config.items():
            if not value:
                logger.error(f"Missing environment variable for: {key}")
                raise ValueError(f"Missing environment variable: {key}")

        logger.info("Email configuration loaded successfully.")
        return config

    # Function: send_email
    # Purpose: Sends an email notification with the specified subject and message.
    # Inputs: subject (str), message (str), recipient (str)
    # Returns: bool - Returns True if email is sent successfully, False otherwise.
    def send_email(self, subject: str, message: str, recipient: str = None) -> bool:
        """Send an email notification."""
        if recipient is None:
            recipient = self.config["recipient_email"]

        try:
            # Create the email message
            msg = MIMEMultipart()
            msg["From"] = self.config["sender_email"]
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            # Connect to the SMTP server
            with smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"]) as server:
                server.starttls()
                server.login(self.config["sender_email"], self.config["sender_password"])
                server.send_message(msg)

            logger.info(f"Email sent successfully to {recipient} with subject: {subject}")
            return True  # Explicitly indicate success
        except smtplib.SMTPException as smtp_error:
            logger.error(f"SMTP error while sending email to {recipient}: {smtp_error}")
            return False
        except Exception as general_error:
            logger.error(f"Error while sending email to {recipient}: {general_error}")
            return False

if __name__ == "__main__":
    logger = LoggerConfig("notification", "notification.log").get_logger()
    logger.info("Test log entry for notification.py")
