# SecureFileGuard Installation Guide

## Overview

Welcome to the SecureFileGuard Installation Guide! This guide will walk you through the steps needed to set up SecureFileGuard on your system, including prerequisites, dependencies, and testing the setup. This version includes updates for integrating the API Gateway and using the VirusTotal API for enhanced malware detection.

## Prerequisites

Before installing SecureFileGuard, ensure the following prerequisites are met:

- **Operating System:** Compatible with Windows 10/11 or a UNIX-like OS
- **Python:** Python 3.8 or higher
- **Permissions:** Administrator permissions for certain installation steps, especially for setting up ClamAV
- **API Key:** A free VirusTotal API key (optional but recommended)

## Dependencies
SecureFileGuard relies on several Python libraries and external software. Here’s a list of essential dependencies:

- **Python Libraries:**

  - `pyclamd` (ClamAV integration)
  - `tensorflow` (future ML capabilities)
  - `pycryptodome` (encryption/decryption)
  - `scapy` (network packet analysis and port scanning)
  - `requests` (API calls for VirusTotal integration)
  - `Flask` or `FastAPI` (API Gateway for handling external requests)
  - `python-dotenv` (manage environment variables for API keys)

- **Other Software:**

    - ClamAV: Required for local malware scanning. Ensure both `clamd` and `freshclam` are installed and configured.

## Installation Steps

1. **Clone the Repository**

    Clone the SecureFileGuard repository to your local system:
    ```bash
    git clone https://github.com/yourusername/SecureFileGuard.git
    cd SecureFileGuard
    ```
   
2. **Set Up a Virtual Environment**

   It is recommended to use a virtual environment to manage dependencies:
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

   Install all necessary Python libraries:
    ```bash
    pip install -r requirements.txt
    ```
   If you don’t have a requirements.txt, install each dependency manually:
    ```bash
    pip install pyclamd tensorflow pycryptodome scapy requests flask python-dotenv
    ```
   
5. **Setting Up ClamAV**

   - Download and install ClamAV from the official website.
   - Configure ClamAV by editing the `clamd.conf` file:
     - Ensure the database directory is specified.
     - Set the correct permissions for the `clamd.conf` file.
   - Update ClamAV signatures:
    ```bash
    freshclam
    ```
   - Start the ClamAV daemon:
    ```bash
    clamd
    ```

6. **Configure VirusTotal API Key**

    - Obtain a free API key from VirusTotal by signing up on their website.
    - Store the API key in a `.env` file for secure access:
    ```bash
    echo "VIRUSTOTAL_API_KEY=your_api_key_here" > .env
    ```

7. **Configure the API Gateway**

    - The API Gateway will handle requests for VirusTotal integration and manage secure communication.
    - Start the API Gateway using Flask:
    ```bash
     python gateway/app.py
    ```
   
8. **Configure ClamAV Connection Ensure the connection to ClamAV via the `pyclamd` library:**

    - Edit the relevant configuration in the code or setup file to match your ClamAV host and port 
     (default: `127.0.0.1:3310`).

## Testing Installation

1. **Navigate to the tests folder:**
    ```bash
    cd SecureFileGuard/tests
    ```
   
2. **Run the test suite:**
    ```bash
    python -m unittest discover -s tests
   ```
   
3. **Test the VirusTotal API Integration:**

    - Run a sample script to check API connectivity:
    ```bash
    python tests/test_virustotal_integration.py
    ```

If all tests pass, your installation is successful. Any failures may indicate configuration issues with ClamAV,
API Gateway, or missing dependencies.

## Common Issues and Solutions

- **Permissions Errors:** If you encounter permissions errors, try running the setup commands as an administrator.
- **ClamAV Not Starting:** Ensure `clamd.conf` is correctly configured and points to the proper database location. Run 
  `freshclam` before starting ClamAV.
- **Cannot Connect to ClamAV via pyclamd:** Ensure ClamAV is running and configured to listen on `127.0.0.1:3310`. You 
  may need to modify the `clamd.conf` file to specify the `TCPAddr` and `TCPSocket` values.
- **VirusTotal API Issues:** Verify that your API key is correctly set in the `.env` file. Check for API rate limits 
  and 
  try again later if you encounter errors.


________________________________________________________________________________________________________________________
Document Last Updated: November 17, 2024

