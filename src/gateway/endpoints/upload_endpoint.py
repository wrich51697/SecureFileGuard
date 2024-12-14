# src/gateway/endpoints/upload_endpoint.py
# Author: William Richmond
# Date: 2024-12-08
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Upload endpoint for SecureFileGuard FastAPI backend.
# Revised on: 2024-12-08

from fastapi import APIRouter, UploadFile, HTTPException
from src.core.processing import process_file
from src.db import DatabaseManager

router = APIRouter()

metadata_manager = DatabaseManager("file_metadata.db")
secure_storage_manager = DatabaseManager("secure_storage.db")
metadata_manager.initialize()
secure_storage_manager.initialize(is_secure_storage=True)

@router.post("/upload")
async def upload_file(file: UploadFile):
    try:
        temp_file_path = f"resources/{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        result = process_file(metadata_manager, secure_storage_manager, temp_file_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
