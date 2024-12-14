# SecureFileGuard: Project Overview

## Project Name: SecureFileGuard

## Author: William Richmond

## Date: 2024-11-09

## Course: CYBR-260-45

## Last Revised: 2024-12-08

___

## Introduction

- Project Name: SecureFileGuard

- Objective: Develop a Python-based application to provide a robust environment for securely uploading, scanning, and managing user files. The project integrates advanced malware scanning, encryption, and network analysis to ensure user safety and privacy.

___

## Purpose and Goals

- Purpose: To ensure secure file uploads and automated malware detection while prioritizing user data security and 
privacy.

- Primary Goals:
  - Enable real-time malware detection during file uploads with a hybrid scanning approach using ClamAV and VirusTotal.
  - Ensure encrypted file storage to protect sensitive data.
  - Provide email notifications for flagged files and maintain detailed audit logs for monitoring and analysis.
  - Implement advanced security features, including comprehensive logging and user-friendly error handling. 

___

## Key Features

- Hybrid Malware Scanning:

    - Combines ClamAV for local scanning and the VirusTotal API for cloud-based threat intelligence.
    - Balances comprehensive detection capabilities with data privacy.

- File Encryption and Secure Storage:

    - Implements PyCryptodome to encrypt files before storage and secure sensitive data.

- Real-Time Network Monitoring:

    - Integrates Scapy for network packet analysis and port scanning to detect suspicious activity.

- API Gateway Integration:

    - Utilizes FastAPI to manage secure communications and handle requests to external services (e.g., VirusTotal).

- Notifications and Logging:

    - Automated email alerts via `smtplib` notify administrators of detected threats.
    - Detailed logging tracks all file uploads, scans, and system events for auditing.

- User-Friendly Interface:

    - Built with HTML, CSS, and JavaScript, the interface simplifies file uploads and displays detailed scan results.

- Version Control with `.gitignore`:

    - Implements a `.gitignore` file to exclude sensitive and dynamically generated files (e.g., log files, `.venv`, and 
  database files) from version control.

___

## Project Architecture

- Backend Framework: Python with a modular structure for maintainability and scalability.

- Core Libraries:

    - `pyclamd` – Integration with ClamAV for local malware detection.
    - `requests` – API calls to VirusTotal.
    - `pycryptodome` – File encryption and decryption.
    - `scapy` – Network analysis for suspicious activity detection.
    - `smtplib` – Email notifications.
    - `FastAPI` – Lightweight and efficient API Gateway framework.

- Security Features:

    - Strong encryption for all stored files.
    - Sensitive information stored in environment variables (.env). 
    - Comprehensive logging to capture all activities and network events.
    - Enhanced error handling and user feedback mechanisms.

___

## Project Timeline

- Week 1-2:

    - Establish project structure.
    - Install dependencies and configure ClamAV.

- Week 3-4:

    - Develop core functionality: file upload, ClamAV integration, and encryption.

- Week 5:

    - Add VirusTotal API integration via the API Gateway.
    - Implement port scanning and email notifications.

- Week 6:

    - Conduct extensive testing and debugging.
    - Refine features based on test results.

- Week 7:

    - Finalize documentation, prepare reports, and complete user acceptance testing.

___

## Acknowledgment

Credit to Classmate: The hybrid scanning integration with VirusTotal was inspired by a suggestion from Volodymyr, whose insights enhanced the project’s malware detection capabilities.

___

## Expected Outcomes

- A secure, user-friendly file upload and malware scanning system incorporating local and cloud-based detection.
- Comprehensive documentation outlining design decisions, implementation details, and best practices for secure file 
  handling.
- Successful testing of functionality and security standards to ensure a reliable, production-ready application.
