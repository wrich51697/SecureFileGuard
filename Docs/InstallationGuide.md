# SecureFileGuard Installation Guide

## Overview

Welcome to the SecureFileGuard Installation Guide!  
This guide provides step-by-step instructions to set up SecureFileGuard on your system,  
including prerequisites, dependencies, and testing.  
It also covers setting up both the CLI and the web-based frontend for secure file uploads.

---

## Prerequisites

- **Operating System:** Compatible with Windows 10/11 or a UNIX-like OS.
- **Python:** Python 3.8 or higher.
- **Permissions:** Administrator permissions for installing ClamAV and configuring the environment.
- **API Key:** Obtain a free VirusTotal API key (optional but recommended).

---

## Dependencies

- **Python Libraries:**
    - `pyclamd`: Integration with ClamAV.
    - `pycryptodome`: File encryption and decryption.
    - `scapy`: Network packet analysis and port scanning.
    - `requests`: API calls for VirusTotal integration.
    - `fastapi` or `flask`: API Gateway for communication.
    - `python-dotenv`: Secure storage of environment variables.

- **External Software:**
    - ClamAV: Local malware scanner (requires `clamd` and `freshclam`).

---

## Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/SecureFileGuard.git
   cd SecureFileGuard
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment**
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up ClamAV**
    - Download and install ClamAV from the official website.
    - Configure the `clamd.conf` file to point to the correct database directory.
    - Update virus definitions:
      ```bash
      freshclam
      ```
    - Start the ClamAV daemon:
      ```bash
      clamd
      ```

6. **Configure VirusTotal API Key**
    - Obtain an API key from [VirusTotal](https://www.virustotal.com).
    - Save the key in a `.env` file:
      ```bash
      echo "VT_API_KEY=your_api_key_here" > .env
      ```

7. **Run the Backend (FastAPI Gateway)**
   ```bash
   uvicorn src.gateway.app:app --host 127.0.0.1 --port 8000 --reload
   ```

8. **Set Up the Frontend**
    - Navigate to the `frontend` directory:
      ```bash
      cd ~\frontend
      python -m http.server 8080
      ```
    - Access the web interface via a browser:
      [http://127.0.0.1:8080](http://127.0.0.1:8080).

9. **Run the CLI**
    - For terminal-based usage:
      ```bash
      python main.py
      ```

---

## Testing Installation

1. **Run Unit Tests:**
   ```bash
   cd tests
   python -m unittest discover
   ```

2. **Check ClamAV Connection:**
   ```bash
   python tests/test_clamav_connection.py
   ```

3. **Test VirusTotal Integration:**
   ```bash
   python tests/test_virustotal_integration.py
   ```

4. **Verify Frontend Functionality:**
    - Drag and drop a file or click the upload button to test functionality.

---

## Common Issues and Solutions

- **Permissions Errors:**  
  Run commands with elevated privileges (e.g., use `sudo` or run as Administrator).

- **ClamAV Not Starting:**  
  Verify the `clamd.conf` file and run `freshclam` to update definitions.

- **VirusTotal API Issues:**  
  Ensure the `.env` file contains the correct API key. Monitor for API rate limits.

- **Frontend Issues:**  
  Verify the server is running on port 8080. Check the browser console for errors.

---

## Notes

- **Environment Variables:** Ensure sensitive data (e.g., API keys, SMTP credentials) are stored in the `.env` file.
- **Logging:** All logs are saved in the `logs/` directory for auditing and troubleshooting.
- **Git Ignore:** Log files, `.venv`, and dynamically generated files (e.g., `file_metadata.db`) are excluded.

---

## Document Last Updated: December 13, 2024
