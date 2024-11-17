# Developer Documentation for SecureFileGuard

## Table of Contents

1. Introduction
2. System Architecture
3. Code Structure and Organization
4. Installation Guide
5. Configuration
6. Testing and Debugging
7. Maintenance and Troubleshooting
8. Hybrid Malware Scanning Approach
9. API Gateway Integration
10. Network Functionality Enhancements

________________________________________________________________________________________________________________________

## 1. Introduction
- ### Project Overview:

  SecureFileGuard is a security-focused application designed to securely handle file uploads and scans for malware using a hybrid approach with ClamAV and VirusTotal. It automates the scanning, logging, and notification of potentially harmful files. This document is intended to guide developers through understanding, configuring, and extending the codebase.
    - ### Target Audience:

      Developers working on maintenance, enhancement, or troubleshooting of SecureFileGuard.

- ### Acknowledgment:

  The idea to integrate VirusTotal for enhanced malware detection was suggested by a classmate, **Volodymyr**. This hybrid approach has been adopted to balance enhanced threat intelligence with data privacy considerations.
________________________________________________________________________________________________________________________

## 2. System Architecture

- ### Overview of Components:

    - SecureFileGuard integrates several libraries, including:

        - ClamAV for local malware scanning.
        - VirusTotal API for additional cloud-based malware analysis.
        - Scapy for packet analysis and port scanning.
        - PyCryptodome for encryption/decryption.
        - API Gateway (Flask/FastAPI) for managing API requests and handling secure communication.

    - ### Workflow Summary:

        1. Files are uploaded to the system.
        2. ClamAV scans the files locally for malware signatures.
        3. If further analysis is needed, the file hash is sent to VirusTotal via the API Gateway.
        4. Scanned files are logged and stored securely.
        5. Optional notifications alert the admin to malicious files.
        6. Network logging captures all external API calls and suspicious network activity.
________________________________________________________________________________________________________________________

## 3. Code Structure and Organization

- Directory Structure
   ```text
    SecureFileGuard/
    ├── app/              # Core application files
    ├── tests/            # Unit tests and testing scripts
    ├── Docs/             # Documentation folder
    │   ├── ProjectOverview.md
    │   └── DeveloperDocumentation.md
    ├── config/           # Configuration files
    ├── lib/              # External libraries or scripts
    ├── logs/             # Log files
    └── gateway/          # API Gateway components
    ```

    - ## Key Files and Directories:
        - `app/`: Contains primary modules for file handling, scanning, encryption.
        - `gateway/`: Manages API requests for VirusTotal integration.
        - `tests/`: Contains test scripts for each major function.
        - `config/`: Configuration files, including ClamAV and environment settings.
        - `Docs/`: Project and developer documentation.
________________________________________________________________________________________________________________________

## 8. Hybrid Malware Scanning Approach

- **Local Scanning with ClamAV**:
    - ClamAV is used as the primary scanner for local file analysis, ensuring data privacy by processing files within the system.
- **VirusTotal API Integration**:
    - If ClamAV results are inconclusive, the file hash (e.g., SHA-256) is sent to VirusTotal through the API Gateway for additional verification.
- **Privacy Measures**:
    - Only file hashes are sent to VirusTotal, not the full file contents, reducing the risk of exposing sensitive user data.

________________________________________________________________________________________________________________________

## 9. API Gateway Integration

- The API Gateway (implemented using Flask or FastAPI) serves as a centralized entry point for all external API calls, handling:
    - **Rate Limiting**: Controls the frequency of requests to prevent exceeding API limits.
    - **Data Privacy**: Hashes the file data before sending to external services, ensuring no sensitive information is exposed.
    - **Secure Communication**: Uses HTTPS for encrypted data transmission.

________________________________________________________________________________________________________________________

## 10. Network Functionality Enhancements

- **Email Notifications**:
    - Uses `smtplib` to send real-time alerts to administrators when malware is detected.
- **Port Scanning with Scapy**:
    - Implements basic port scanning using `Scapy` to detect suspicious network behavior.
- **Network Logging**:
    - Captures details of all API calls and network activities using Python’s `socket` and `logging` libraries.
- **VirusTotal API Integration**:
    - Uses the `requests` library to query the VirusTotal API for additional threat intelligence.

________________________________________________________________________________________________________________________

Document Last Updated: November 17, 2024


