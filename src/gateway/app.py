# app.py
# Author: William Richmond
# Date: 2024-12-01
# Class: CYBR-260-45
# Assignment: Final Project
# Description: API Gateway for handling file uploads, notifications, and integrations.
# Revised on: 2024-12-08

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.gateway.endpoints import upload_endpoint, notify
from src.logger_config import LoggerConfig

# Initialize logger for this module
logger = LoggerConfig(name="app", log_filename="app.log").get_logger()

# Initialize FastAPI app
app = FastAPI()

# Middleware: Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
try:
    app.include_router(upload_endpoint.router, prefix="/api/upload", tags=["Upload"])
    logger.info("Upload endpoint router registered successfully.")
except Exception as e:
    logger.error(f"Failed to register upload endpoint router: {e}")

try:
    app.include_router(notify.router, prefix="/api/notify", tags=["Notification"])
    logger.info("Notification endpoint router registered successfully.")
except Exception as e:
    logger.error(f"Failed to register notification endpoint router: {e}")


# Function: root
# Purpose: Health check endpoint.
# Inputs: None
# Returns: dict - Confirmation message that the API is running.
@app.get("/")
async def root():
    """
    Health check endpoint to verify that the API is running.
    """
    logger.info("Health check endpoint accessed.")
    return {"message": "SecureFileGuard API is running"}


# Entry Point: Main script to run the FastAPI application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    try:
        logger.info("Starting the FastAPI application with Uvicorn.")
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        logger.error(f"Error occurred while starting the application: {e}")
