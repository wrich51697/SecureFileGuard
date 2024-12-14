# SecureFileGuard Project

## Author
**William Richmond**

## Date
**2024-11-17**

## Class
**CYBR-260-45: Security Scripting with Python**

## Assignment
**Final Project: Secure File Storage and Malware Scanning**

## Description
SecureFileGuard is a Python-based security application designed to handle user-uploaded files securely. It features a 
hybrid malware scanning approach using both ClamAV and VirusTotal, along with file encryption, network monitoring, 
and email notifications. The project aims to provide a comprehensive solution for platforms managing sensitive user 
documents, ensuring safe file handling and robust threat detection.

### Key Features
- **Hybrid Malware Scanning**: Utilizes ClamAV for local detection and VirusTotal API for cloud-based verification.
- **File Encryption and Decryption**: Secures files using PyCryptodome, protecting sensitive data during storage and retrieval.
- **Port Scanning and Network Monitoring**: Uses Scapy for analyzing network traffic and identifying suspicious activity.
- **Email Notifications**: Sends alerts to administrators when malware threats are detected.
- **Detailed Logging**: Maintains comprehensive logs for auditing and troubleshooting.

## Project Structure
```text
SecureFileGuard/
├── .venv/                 # Virtual environment for project dependencies
├── Docs/                  # Documentation files
│   ├── DeveloperDocumentation.md
│   ├── InstallationGuide.md
│   ├── ProjectOverview.md
│   └── UserGuide.md
├── frontend/              # Frontend files for user interface
│   ├── index.html         # Main HTML file
│   ├── scripts/           # JavaScript files
│   │   └── main.js
│   └── styles.css         # CSS file for styling
├── lib/                   # Placeholder for external libraries
│   └── __init__.py
├── logs/                  # Centralized directory for logs
├── resources/             # Sample resources for testing
│   ├── sample.txt
│   └── test_file.txt
├── sandbox/               # Temporary storage for uploaded files
├── src/                   # Core application source files
│   ├── core/              # Core modules
│   │   ├── __init__.py
│   │   └── processing.py
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
├── tests/                 # Unit tests
│   ├── sandbox/           # Test sandbox files
│   │   └── ...
│   ├── test_clamav_connection.py
│   ├── test_db.py
│   ├── test_encryption.py
│   ├── test_env.py
│   ├── test_file_upload.py
│   ├── test_malware_scan.py
│   └── test_notification.py
├── main.py                # Main entry point for the application
├── requirements.txt       # List of dependencies
├── README.md              # Project overview and usage instructions
├── LICENSE                # License information
├── .env                   # Environment variables
└── file_metadata.db       # SQLite database for file metadata

```

## Requirements
- Python 3.8 or higher
- **Dependencies:** `pyclamd`, `pycryptodome`, `scapy`, `requests`, `Flask` or `FastAPI`, `python-dotenv`
Other Software: ClamAV (with `clamd` daemon)

## Installation
1. Clone the repository or download the project files:
    ```bash
    git clone https://github.com/yourusername/SecureFileGuard.git
    cd SecureFileGuard
    ```
   
2. Follow the Installation Guide: [Installation Guide](docs/Installation_Guide.md) for setup instructions.

## Usage

Add details for frontend usage since the project includes both a CLI and a web-based interface.

1. Start the ClamAV daemon (`clamd`).

2. Running the Frontend:
   ```Bash
   cd frontend
   python -m http.server 8080
   ```
   - Access the frontend via your browser at http://127.0.0.1:8080.

3. Running the Backend:
   ```Bash
   uvicorn src.gateway.app:app --host 127.0.0.1 --port 8000 --reload
   ```
   
4. Launch SecureFileGuard CLI:
    ```bash
    python main.py
    ```

4. Upload a file to scan and view the results.

## Logging
**Log files are stored in the `logs/` directory:**
- `upload_endpoint.log`: Logs related to file uploads via the API.
- `file_upload.log`: Logs for file validation and storage processes.
- `db.log`: Logs related to database interactions.
- `encryption.log`: Logs for file encryption activities.
- `malware_scan.log`: Logs for malware scanning events.

## Environment Variables
The `.env` file should contain the following variables:
- `VT_API_KEY`: Your VirusTotal API key for cloud-based threat scanning.
- `SMTP_SERVER`: The SMTP server for sending notifications.
- `SMTP_PORT`: The SMTP port (e.g., 587 for TLS).
- `SENDER_EMAIL`: The email address used to send notifications.
- `SENDER_PASSWORD`: The password for the sender email account.
- `ENCRYPTION_KEY`: A secure passphrase for file encryption.


## Resources

- VirusTotal API Documentation: [VirusTotal API Documentation](https://developers.virustotal.com/)
- ClamAV Documentation: [ClamAV Documentation](https://docs.clamav.net/)

## Future Enhancements
- Implement machine learning capabilities using TensorFlow for advanced threat detection.
- Enable remote scanning and cloud storage integration for scalability.

## Credits
- Author: William Richmond
- VirusTotal Integration Suggested By: Volodymyr Krushynskyi

## License
This project is licensed under MIT.

___
Last Updated: December 8, 2024 
