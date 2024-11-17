# SecureFileGuard User Guide

1. ## Introduction
   SecureFileGuard is a powerful application designed to ensure safe file handling by offering secure file uploads, 
   malware scanning, and network analysis capabilities. By integrating a hybrid malware scanning approach with ClamAV 
   and VirusTotal, it provides robust threat detection, making it ideal for users seeking a comprehensive and reliable 
   file management solution.

   ## Key Features

   - **Secure File Upload:** Upload files with confidence, knowing they will be securely processed.
   - **Hybrid Malware Scanning:** Scans files upon upload using both ClamAV (local) and VirusTotal (cloud-based) for 
     enhanced threat detection.
   - **Network Analysis:** Uses Scapy for port scanning and real-time network monitoring to detect suspicious activity.
   - **Notifications:** Automated email alerts notify users and administrators if a malware threat is detected.

2. ## Getting Started

   ### Prerequisites

   - Operating System: Compatible with Windows 10 and later, or Linux.
   - Software: Ensure Python 3.8+ and ClamAV are installed.
   - Dependencies: Python libraries including `pyclamd`, `scapy`, `tensorflow`, `pycryptodome`, `requests`, and `Flask` or 
     `FastAPI`. (For detailed installation steps, refer to the Installation Guide.)

   ### Installation Instructions

   Follow the steps in the Installation Guide to set up SecureFileGuard and ensure all dependencies are correctly installed.

   ### Launching SecureFileGuard

   - Start the ClamAV daemon (`clamd`) if it is not already running.
   - Start the API Gateway for handling VirusTotal API requests:
   ```bash
   python gateway/app.py
   ```
   
   - Run SecureFileGuard from your terminal:
   ```Bash
    python main.py
   ```
   
   - The application will initialize, and you will be ready to begin uploading and scanning files.

3. ## Using SecureFileGuard

   ### Uploading Files

   - Launch the application as outlined in the Getting Started section.
   - Use the Upload File option to browse and select the file you want to upload.
   - Confirm your selection to proceed with the upload.
   
   ### Scanning Files for Malware

   - Once a file is uploaded, SecureFileGuard will automatically initiate a hybrid malware scan.
      - Step 1: The file is first scanned locally using ClamAV.
      - Step 2: If additional verification is needed, the file hash is sent to VirusTotal for a secondary scan via 
        the API Gateway.
   - The scan may take a few moments depending on file size and network conditions.
   - If any threats are detected, a notification will appear with detailed information about the infected file.
   
   ### Viewing Scan Results

   - After a scan is completed, you’ll see one of the following results:
      - **Clean:** The file is safe and free from malware.
      - **Infected:** The file contains threats. Details will be displayed, including threat type and recommended 
        action.
   - For additional details, you can view a full report in the Scan Results section.
   
   ### Managing Files

   - **Download:** Once a file is scanned, it can be securely downloaded if desired.
   - **Delete:** You may delete any scanned file that you no longer need to keep on the server.
   
4. ## Troubleshooting

   ### Common Issues and Solutions
   Issue: "Could not connect to clamd server"

   - Solution: Verify that the ClamAV daemon (`clamd`) is running. You may need to restart it and try again.
   
   Issue: "VirusTotal API error"

   - Solution: Ensure your API key is correctly configured in the `.env` file. Check for API rate limits if you 
   encounter errors.
   
   Issue: "File upload error"

   - Solution: Ensure the file meets any size or format restrictions as per system requirements. Retry the upload and 
   confirm you have sufficient permissions.
   
   Issue: "Scan results not displaying"

   - Solution: Check that ClamAV is fully updated. Running `freshclam` can ensure you have the latest virus definitions.
   
5. ## Contact and Support

   This contact information is currently a placeholder and will be updated in the final release.

   - Email: support@securefileguard.com
   - Website: www.securefileguard.com/support
________________________________________________________________________________________________________________________
Document Last Updated: November 17, 2024

