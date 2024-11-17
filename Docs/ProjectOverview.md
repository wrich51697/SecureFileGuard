# SecureFileGuard: Project Overview

## Project Name: SecureFileGuard

### Author: William Richmond

### Date: 2024-11-09

### Course: CYBR-260-45

### Revised: 2024-11-17

---

## 1. Introduction

- **Project Name**: SecureFileGuard
- **Objective**: To develop a Python-based application focused on secure file uploads and advanced malware scanning. 
   The tool provides a robust environment for handling user-uploaded files, utilizing a combination of local and 
  cloud-based threat detection, encryption, and network analysis.

## 2. Purpose and Goals

- **Purpose**: Enable secure file upload and automated malware scanning, ensuring that all files are safe for storage 
     and use while protecting user privacy.
- **Primary Goals**:
   - Offer real-time malware detection during file uploads using a **hybrid approach** with ClamAV and VirusTotal.
   - Ensure encrypted storage and secure retrieval of files.
   - Provide email notifications for flagged files and detailed logging for auditing.

## 3. Key Features

- **Hybrid Malware Scanning**:
   - Uses **ClamAV** for local malware detection and the **VirusTotal API** for enhanced cloud-based threat intelligence. 
     This hybrid approach balances privacy and comprehensive scanning capabilities.
- **File Encryption and Decryption**:
   - Utilizes **PyCryptodome** to encrypt files before storage, ensuring secure handling of sensitive data.
- **Port Scanning and Network Monitoring**:
   - Integrates **Scapy** for real-time network packet inspection and port scanning, helping detect suspicious activity 
     associated with uploaded files.
- **API Gateway Integration**:
   - Uses **Flask** or **FastAPI** as an API Gateway to manage requests, handle secure communication, and anonymize data 
     sent to external services like VirusTotal.
- **Notifications and Logging**:
   - Sends automated email alerts via `smtplib` when a malware threat is identified.
   - Maintains comprehensive logs of all file uploads, scans, and network activities for auditing and analysis.

## 4. Project Architecture

- **Backend Framework**: Python, following a modular structure to support seamless integration of additional libraries 
   and features.
- **Core Libraries**:
   - `pyclamd` for ClamAV integration
   - `requests` for VirusTotal API calls
   - `pycryptodome` for encryption
   - `scapy` for network analysis
   - `smtplib` for email notifications
   - `Flask` or `FastAPI` for the API Gateway
- **Security Measures**:
   - Secure encryption for all file handling
   - Use of environment variables for sensitive data (e.g., API keys)
   - Logging of all actions and network activities

## 5. Project Timeline

- **Week 1-2**: Set up project structure, install core libraries, and configure ClamAV.
- **Week 3-4**: Develop core functionality (file upload, ClamAV scanning, encryption).
- **Week 5**: Integrate VirusTotal API via the API Gateway, implement port scanning, and add email notifications.
- **Week 6**: Conduct comprehensive testing and debugging, refine features.
- **Week 7**: Finalize documentation, prepare the final report, and conduct final user acceptance testing.

## 6. Credit to Classmate

The integration of VirusTotal for enhanced malware scanning was suggested by my classmate, **Volodymyr**. 
His suggestion helped shape the hybrid scanning approach used in SecureFileGuard, providing a more comprehensive threat 
detection capability.

## 7. Expected Outcomes

- A functional and secure file upload system that incorporates both local and cloud-based malware scanning.
- Detailed documentation covering project implementation, design decisions, and best practices for secure file handling.
- Successful completion of extensive testing to confirm the program meets all functionality and security standards.

