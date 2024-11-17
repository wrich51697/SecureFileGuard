# test_encryption.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Unit tests for the encryption module of SecureFileGuard.
# Revised on: 2024-11-17

import unittest
from src.encryption import generate_key, encrypt_file, decrypt_file

class TestEncryption(unittest.TestCase):
    """Unit tests for encryption and decryption functions."""

    def setUp(self):
        """Set up test data and key for encryption."""
        self.password = "SecurePass123"
        self.data = b"This is a test file content."
        self.key, self.salt = generate_key(self.password)

    # Function: test_generate_key
    # Purpose: Tests key generation using PBKDF2.
    # Inputs: None
    # Returns: None
    def test_generate_key(self):
        key, salt = generate_key(self.password)
        self.assertEqual(len(key), 32, "Key length should be 32 bytes for AES-256.")
        self.assertEqual(len(salt), 16, "Salt length should be 16 bytes.")

    # Function: test_encrypt_and_decrypt_file
    # Purpose: Tests the encryption and decryption process.
    # Inputs: None
    # Returns: None
    def test_encrypt_and_decrypt_file(self):
        encrypted_data = encrypt_file(self.data, self.key)
        decrypted_data = decrypt_file(encrypted_data, self.key)
        self.assertEqual(decrypted_data, self.data, "Decrypted data does not match original data.")

if __name__ == "__main__":
    unittest.main()

