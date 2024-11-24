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
├── lib/                   # External libraries or helper scripts
├── logs/                  # Log files directory
├── src/                   # Core application source files
│   ├── encryption.py
│   ├── file_upload.py
│   ├── logger.py
│   ├── malware_scan.py
│   └── notification.py
├── tests/                 # Unit tests and testing scripts
│   └── library_test.py
├── main.py                # Main entry point for the application
├── requirements.txt       # List of dependencies
├── README.md              # Project overview and usage instructions
└── LICENSE                # License information
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

1. Start the ClamAV daemon (`clamd`).

2. Run the API Gateway:
    ```bash
    python gateway/app.py
    ```
   
3. Launch SecureFileGuard:
    ```bash
    python main.py
    ```

4. Upload a file to scan and view the results.

## Logging

**Log files are stored in the `logs/` directory:**

- `app_log.txt`: Logs related to the main application processes.
- `gateway_log.txt`: Logs for the API Gateway and VirusTotal integration.
- `scan_log.txt`: Detailed logs of malware scans and results.

## Resources

- VirusTotal API Documentation: [VirusTotal API Documentation](https://developers.virustotal.com/)
- ClamAV Documentation: [ClamAV Documentation](https://docs.clamav.net/)

## Future Enhancements
- Implement machine learning capabilities using TensorFlow for advanced threat detection.
- Add a graphical user interface (GUI) for improved user experience.
- Enable remote scanning and cloud storage integration for scalability.

## Credits
- Author: William Richmond
- VirusTotal Integration Suggested By: Volodymyr Krushynskyi

## License
This project is licensed under MIT.
