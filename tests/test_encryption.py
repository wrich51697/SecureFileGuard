# test_encryption.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Unit tests for the encryption module of SecureFileGuard.
# Revised on: 2024-12-01

import unittest
from datetime import datetime
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

    # Function: test_encrypt_empty_data
    # Purpose: Ensures encryption and decryption of empty data works.
    # Inputs: None
    # Returns: None
    def test_encrypt_empty_data(self):
        empty_data = b""
        encrypted_data = encrypt_file(empty_data, self.key)
        decrypted_data = decrypt_file(encrypted_data, self.key)
        self.assertEqual(decrypted_data, empty_data, "Decryption should work for empty data.")

    # Function: test_decrypt_tampered_data
    # Purpose: Ensures tampered data raises an exception during decryption.
    # Inputs: None
    # Returns: None
    def test_decrypt_tampered_data(self):
        encrypted_data = encrypt_file(self.data, self.key)
        tampered_data = encrypted_data[:-1] + b"0"  # Alter the encrypted data
        with self.assertRaises(ValueError, msg="Tampered data should raise an exception."):
            decrypt_file(tampered_data, self.key)

    # Function: test_encryption_performance
    # Purpose: Measures encryption and decryption performance.
    # Inputs: None
    # Returns: None
    def test_encryption_performance(self):
        large_data = b"A" * (10 * 1024 * 1024)  # 10 MB of data
        start_time = datetime.now()
        encrypted_data = encrypt_file(large_data, self.key)
        decrypted_data = decrypt_file(encrypted_data, self.key)
        end_time = datetime.now()
        self.assertEqual(decrypted_data, large_data, "Decrypted data should match original data.")
        self.assertLess((end_time - start_time).total_seconds(), 5, "Encryption/decryption should complete within 5 seconds.")

    # Function: test_unique_key_and_salt
    # Purpose: Validates that unique keys and salts are generated for different passwords.
    # Inputs: None
    # Returns: None
    def test_unique_key_and_salt(self):
        key1, salt1 = generate_key("Password1")
        key2, salt2 = generate_key("Password2")
        self.assertNotEqual(key1, key2, "Keys generated for different passwords should not match.")
        self.assertNotEqual(salt1, salt2, "Salts generated for different passwords should not match.")

    # Function: test_multi_user_encryption
    # Purpose: Ensures encryption and decryption work correctly in a multi-user scenario.
    # Inputs: None
    # Returns: None
    def test_multi_user_encryption(self):
        user1_key, _ = generate_key("User1Pass")
        user2_key, _ = generate_key("User2Pass")
        user1_encrypted = encrypt_file(self.data, user1_key)
        user2_encrypted = encrypt_file(self.data, user2_key)
        self.assertNotEqual(user1_encrypted, user2_encrypted, "Encrypted data for different users should differ.")
        self.assertEqual(decrypt_file(user1_encrypted, user1_key), self.data, "User1 decryption should succeed.")
        self.assertEqual(decrypt_file(user2_encrypted, user2_key), self.data, "User2 decryption should succeed.")

if __name__ == "__main__":
    unittest.main()
