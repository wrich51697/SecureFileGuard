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

---

## 1. Introduction

### Project Overview:
SecureFileGuard is a robust, security-focused application designed to handle file uploads securely and scan for malware. It leverages a hybrid malware scanning approach combining local scanning with ClamAV and cloud-based intelligence with VirusTotal. The system automates workflows for scanning, logging, and alerting while emphasizing data security and privacy.

### Target Audience:
Developers involved in maintaining, enhancing, or troubleshooting SecureFileGuard.

### Acknowledgment:
Integration of VirusTotal for enhanced malware detection is based on a suggestion by Volodymyr, ensuring a balance between enhanced threat detection and privacy considerations.

---

## 2. System Architecture

### Overview of Components:
- **SecureFileGuard** integrates several libraries, including:
    - **ClamAV:** Local malware scanning.
    - **VirusTotal API:** Cloud-based threat analysis.
    - **PyCryptodome:** AES encryption for file storage and transfer.
    - **FastAPI:** API Gateway for managing secure API calls.
    - **psutil:** Automated detection and management of the ClamAV daemon (`clamd`).
    - **Scapy:** Real-time network analysis for port scanning.
    - **smtplib:** Email notifications for malicious file detections.

### Workflow Summary:
1. Files are uploaded and validated.
2. Files are scanned locally with ClamAV for malware.
3. Inconclusive or suspicious results are sent to VirusTotal for further analysis.
4. Files are encrypted and securely stored in SQLite.
5. Malicious files are quarantined, and administrators are notified via email.
6. Network activity is monitored and logged.

---

## 3. Code Structure and Organization

### Directory Structure
```text
SecureFileGuard/
├── frontend/              # Frontend files for the web interface
│   ├── index.html         # Main HTML file
│   ├── scripts/           # JavaScript files
│   │   └── main.js
│   └── styles.css         # CSS file for styling
├── src/                   # Core application source files
│   ├── gateway/           # API Gateway modules
│   │   ├── app.py
│   │   └── endpoints/
│   │       ├── notify.py
│   │       └── upload_endpoint.py
│   ├── encryption.py      # Encryption handling
│   ├── file_upload.py     # File upload and validation
│   ├── logger_config.py   # Logger configuration
│   ├── malware_scan.py    # Malware scanning logic
│   ├── notification.py    # Notification handling
│   ├── db.py              # Database operations
├── tests/                 # Unit and integration tests
│   ├── test_clamav_connection.py
│   ├── test_file_upload.py
│   ├── test_encryption.py
│   ├── test_malware_scan.py
│   └── test_notification.py
├── logs/                  # Logging directory
├── sandbox/               # Temporary storage for uploaded files
├── file_metadata.db       # SQLite database for metadata
├── requirements.txt       # List of dependencies
├── README.md              # Project overview and usage instructions
├── LICENSE                # License information
└── .env                   # Environment variables
```

### Key Files and Directories:
- **`src/`:** Contains core application modules for scanning, file handling, and notifications.
- **`frontend/`:** HTML, CSS, and JavaScript files for the web-based interface.
- **`tests/`:** Unit tests for core functionalities like file upload, scanning, and encryption.

---

## 4. Installation Guide
Refer to the [Installation Guide](Docs/InstallationGuide.md) for step-by-step setup instructions, including:
1. Installing Python and project dependencies.
2. Configuring ClamAV and VirusTotal.
3. Running the frontend and backend servers.

---

## 5. Configuration

### Environment Variables:
Set up a `.env` file in the project root with the following variables:
```bash
VIRUSTOTAL_API_KEY=your_api_key_here
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SENDER_EMAIL=admin@example.com
SENDER_PASSWORD=your_password_here
ENCRYPTION_KEY=your_secure_key_here
```

### ClamAV Configuration:
1. Install ClamAV and update virus definitions using `freshclam`.
2. Start the ClamAV daemon (`clamd`) before running the application.

---

## 6. Testing and Debugging

### Unit Testing:
Run unit tests using:
```bash
python -m unittest discover tests
```
Tests cover:
- File upload functionality.
- Malware scanning with ClamAV and VirusTotal.
- Encryption and notification systems.

### Debugging Steps:
1. Check logs in the `logs/` directory for detailed error messages.
2. Test ClamAV with:
   ```bash
   clamdscan <file_path>
   ```
3. Verify VirusTotal API connectivity:
   ```bash
   python tests/test_virustotal_integration.py
   ```

---

## 7. Maintenance and Troubleshooting

### Regular Maintenance:
1. Update ClamAV virus definitions with `freshclam`.
2. Archive old logs to prevent excessive disk usage.
3. Rotate API keys periodically for security.

### Common Issues:
- **ClamAV not running:** Check `clamd` status or configuration.
- **API errors:** Ensure the VirusTotal API key is valid and within rate limits.
- **Database errors:** Verify permissions and integrity of `file_metadata.db`.

---

## 8. Hybrid Malware Scanning Approach

- **Local Scanning with ClamAV:** Quick scans with low privacy risks.
- **Cloud-based Analysis with VirusTotal:** Comprehensive threat detection.

---

## 9. API Gateway Integration

- **Role:** Centralized handling of VirusTotal API requests.
- **Features:**
    - Rate-limiting to prevent API overuse.
    - Secure, anonymized communication using HTTPS.

---

## 10. Network Functionality Enhancements

### Automated ClamAV Management:
Uses `psutil` to check and start `clamd` automatically.

### Enhanced Logging:
Captures detailed records for API and network activities.

---

Document Last Updated: December 13, 2024
