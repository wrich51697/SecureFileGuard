# notify.py
# Author: William Richmond
# Date: 2024-12-01
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Defines the email notification endpoint for the FastAPI gateway.
# Revised on: 2024-12-08

from fastapi import APIRouter, HTTPException
from src.notification import NotificationManager
from src.logger_config import LoggerConfig

# Initialize logger for this module
logger = LoggerConfig(name="notify", log_filename="notify.log").get_logger()

# Initialize the router and NotificationManager
router = APIRouter()
notification_manager = NotificationManager()

# Function: notify_endpoint
# Purpose: Sends a test email notification to verify email functionality.
# Inputs: None
# Returns: dict - Status and message of the notification process.
@router.post("/send", response_model=dict)
async def notify_endpoint():
    """
    Endpoint to send a test email notification.

    Returns:
        dict: Contains the status and message of the operation.
    """
    try:
        subject = "Test Notification"
        message = "This is a test notification from SecureFileGuard."
        recipient = None  # Use default recipient from environment variables

        logger.info("Attempting to send a test notification.")
        success = notification_manager.send_email(subject, message, recipient)

        if success:
            logger.info("Test notification sent successfully.")
            return {"status": "success", "message": "Notification sent successfully"}
        else:
            logger.error("Failed to send test notification.")
            return {"status": "error", "message": "Failed to send notification"}
    except Exception as e:
        logger.error(f"Unexpected error while sending notification: {e}")
        raise HTTPException(status_code=500, detail=f"Notification failed: {str(e)}")
