# SecureFileGuard User Guide

1. ## Introduction
   SecureFileGuard is a robust file security solution designed to streamline secure file uploads, hybrid malware scanning, and network monitoring. It combines local scanning (ClamAV) and cloud-based scanning (VirusTotal) to deliver a powerful defense against malware threats.

   ## Key Features
   - **Secure File Upload**: Safeguard your data with secure file handling protocols.
   - **Hybrid Malware Scanning**: Combines ClamAV's local scanning with VirusTotal's advanced cloud-based API for 
     enhanced accuracy.
   - **Notifications**: Automated email alerts notify users of detected threats.
   - **Detailed Logs**: Easily track application activity with user-friendly audit logs.
   - **Extensibility**: A modular design that allows for future enhancements.
___

2. ## Getting Started

   ### Prerequisites

      - Operating System: Windows 10+ or a compatible Linux distribution.
      - Software:
         - Python 3.8+
         - ClamAV (ensure `clamd` service is installed and running).
      - Environment Setup: Ensure the `.env` file contains your VirusTotal API key, email SMTP configuration, and other 
           environment variables.
   
      ## Installation
      Refer to the Installation Guide for step-by-step instructions on setting up SecureFileGuard and its dependencies.

   ## Launching SecureFileGuard

   1. Start ClamAV's `clamd` service (if not running):
      ```Bash
      clamd &
      ```
   2. Launch the backend API Gateway:
      ```Bash
      uvicorn src.gateway.app:app --host 127.0.0.1 --port 8000 --reload
      ```
   3. Start the frontend:
      ```Bash
      python -m http.server 8080
      ```
   4. (Optional) Use the CLI:
      ```Bash 
      python main.py
      ```
___

3. ## Features and Usage

   ### Uploading Files

      1. Drag and drop files into the designated area in the web interface or click "Upload."
   
      2. Alternatively, use the CLI to upload and scan files manually.
   
   ## Malware Scanning

   - Hybrid scanning automatically detects threats using:
      - ClamAV for local signature matching.
      - VirusTotal for advanced detection using cloud APIs.
     
   ## Notifications
   - If a threat is detected, SecureFileGuard sends an email alert to the configured admin address. 
___
   4. ## Troubleshooting

      ### Common Issues and Solutions

      Issue: "Could not connect to clamd server"

      - Solution: Ensure clamd is running and accessible. Restart with:
      ```bash 
      clamd restart
      ```
      Issue: "VirusTotal API error"

      - Solution: Verify your API key in the .env file. Ensure you haven’t exceeded the daily request limit.
      
      Issue: "File upload error"

      - Solution: Ensure the file is under the size limit (10MB) and in a supported format (.txt, .pdf, .docx).
___

5. ## Additional Resources

### Placeholders

   - Visit our website for more tutorials: www.securefileguard.com
   - Contact us: support@securefileguard.com
___
   Last Updated: December 8, 2024 

