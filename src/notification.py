# notification.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Provides functions for sending email notifications for SecureFileGuard.
# Revised on: 2024-11-17

import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

# Ensure the logs directory exists
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_directory, 'notification.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function: load_email_config
# Purpose: Loads email configuration from environment variables.
# Inputs: None
# Returns: dict - Dictionary with SMTP server settings.
def load_email_config() -> dict:
    config = {
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "sender_email": os.getenv("SENDER_EMAIL", "youremail@gmail.com"),
        "sender_password": os.getenv("SENDER_PASSWORD", "yourpassword"),
        "recipient_email": os.getenv("RECIPIENT_EMAIL", "admin@example.com")
    }
    logging.info("Email configuration loaded successfully.")
    return config

# Function: send_email_notification
# Purpose: Sends an email notification with the specified subject and message.
# Inputs: subject (str), message (str), recipient (str)
# Returns: bool - Returns True if email is sent successfully, False otherwise.
def send_email_notification(subject: str, message: str, recipient: str) -> bool:
    config = load_email_config()
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = config["sender_email"]
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Connect to the SMTP server
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.starttls()
            server.login(config["sender_email"], config["sender_password"])
            server.send_message(msg)

        logging.info(f"Email sent successfully to {recipient} with subject: {subject}")
        return True
    except smtplib.SMTPException as smtp_error:
        print(f"SMTPException caught: {smtp_error}")
        logging.error(f"SMTP error while sending email: {smtp_error}")
        return False
    except Exception as general_error:
        print(f"General Exception caught: {general_error}")
        logging.error(f"General error while sending email: {general_error}")
        return False

