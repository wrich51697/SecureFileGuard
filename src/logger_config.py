# logger_config.py
# Author: William Richmond
# Date: 2024-12-08
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Centralized logger configuration class for SecureFileGuard, providing standardized logging across modules.
# Revised on: 2024-12-08

import logging
import os
from logging.handlers import RotatingFileHandler


class LoggerConfig:
    """
    A class for configuring and creating loggers for different modules.
    """

    # Function: __init__
    # Purpose: Initializes the LoggerConfig class with the logger name and log file.
    # Inputs:
    #   - name (str): Name of the logger, typically the module name.
    #   - log_filename (str): Name of the log file where logs will be written.
    # Returns: None
    def __init__(self, name: str, log_filename: str):
        self.name = name
        self.log_filename = log_filename

        # Set the log directory relative to the project root
        self.log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")

        # Ensure the log directory exists
        os.makedirs(self.log_directory, exist_ok=True)

    # Function: get_logger
    # Purpose: Creates and returns a logger with the specified name and log file configuration.
    # Inputs: None
    # Returns: logging.Logger - Configured logger object.
    def get_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        if not logger.handlers:  # Prevent duplicate handlers
            handler = RotatingFileHandler(
                os.path.join(self.log_directory, self.log_filename),
                maxBytes=5 * 1024 * 1024,  # 5MB max log file size
                backupCount=3  # Keep up to 3 backup files
            )
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
