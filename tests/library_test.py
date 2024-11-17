# Author: William Richmond
# Date: 2024-11-03
# Class: CYBR-260-45
# Assignment: SecureFileGuard Library Tests
# Description: Unit tests for SecureFileGuard required libraries, testing compatibility and basic functionality.
# Revised: 2024-11-17

import pyclamd
from scapy.layers.inet import IP, TCP
import tensorflow as tf
from Cryptodome.Cipher import AES
import unittest
import subprocess
import time
import os
import ctypes

class TestSecureFileGuardLibraries(unittest.TestCase):
    """Unit tests for SecureFileGuard library compatibility and basic functions."""

    @classmethod
    def setUpClass(cls):
        """Initialize ClamAV daemon and check for admin privileges."""
        # Check if running with admin privileges
        if not ctypes.windll.shell32.IsUserAnAdmin():
            raise PermissionError("Tests must be run with administrator privileges for ClamAV access.")

        # Check ClamAV configuration
        config_path = r"C:\Program Files\ClamAV\clamd.conf"
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"ClamAV configuration file not found: {config_path}")

        with open(config_path, 'r') as config_file:
            config = config_file.read()
            if "TCPSocket" not in config or "TCPAddr" not in config:
                raise RuntimeError("ClamAV configuration is missing 'TCPSocket' and 'TCPAddr'. Please update clamd.conf.")

        # Start ClamAV daemon
        print("Starting ClamAV daemon (clamd)...")
        cls.clamd_process = subprocess.Popen(
            r"C:\Program Files\ClamAV\clamd.exe", shell=True
        )
        time.sleep(20)  # Allow time for clamd to initialize
        print("ClamAV daemon started.")

    @classmethod
    def tearDownClass(cls):
        """Stop ClamAV daemon after all tests have run."""
        cls.clamd_process.terminate()
        print("ClamAV daemon stopped.")

    # function: test_pyclamd
    # purpose: Tests connection to ClamAV via pyclamd
    # inputs: None
    # returns: None
    def test_pyclamd(self):
        print("\nTesting pyclamd...")
        try:
            cd = pyclamd.ClamdNetworkSocket('127.0.0.1', 3310)
            self.assertTrue(cd.ping(), "Could not ping the ClamAV server.")
            print("pyclamd connected successfully.")
        except Exception as e:
            self.fail(f"pyclamd connection error: {e}")

    # function: test_scapy
    # purpose: Tests packet creation with Scapy
    # inputs: None
    # returns: None
    def test_scapy(self):
        print("\nTesting Scapy...")
        try:
            ip = IP(dst="8.8.8.8")  # Test target: Google DNS
            syn = TCP(dport=80, flags="S")
            packet = ip / syn
            self.assertIsNotNone(packet, "Failed to create packet.")
            print("Scapy packet created successfully.")
        except Exception as e:
            self.fail(f"Scapy error: {e}")

    # function: test_tensorflow
    # purpose: Tests TensorFlow installation by printing version
    # inputs: None
    # returns: None
    def test_tensorflow(self):
        print("\nTesting TensorFlow...")
        try:
            version = tf.__version__
            self.assertIsInstance(version, str, "TensorFlow version not found.")
            print(f"TensorFlow version: {version}")
        except Exception as e:
            self.fail(f"TensorFlow error: {e}")

    # function: test_pycryptodome
    # purpose: Tests encryption and decryption with PyCryptodome
    # inputs: None
    # returns: None
    def test_pycryptodome(self):
        print("\nTesting PyCryptodome...")
        try:
            key = b'Sixteen byte key'  # AES key must be 16, 24, or 32 bytes
            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(b"Testing encryption")

            # Decrypt to verify functionality
            cipher = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            self.assertEqual(plaintext, b"Testing encryption", "Decryption failed.")
            print("PyCryptodome encryption and decryption successful.")
        except Exception as e:
            self.fail(f"PyCryptodome error: {e}")

if __name__ == "__main__":
    unittest.main()