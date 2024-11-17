# encryption.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Provides encryption and decryption functions using AES (PyCryptodome).
# Revised on: 2024-11-17

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
import base64

# Constants
SALT_SIZE = 16
KEY_SIZE = 32  # AES-256 (32 bytes)
NONCE_SIZE = 16
ITERATIONS = 100_000

# Function: generate_key
# Purpose: Derives a secure encryption key using PBKDF2.
# Inputs: password (str) - The password used for key derivation.
# Returns: tuple (key, salt) - The derived encryption key and salt.
def generate_key(password: str) -> tuple[bytes, bytes]:
    key_salt = get_random_bytes(SALT_SIZE)
    derived_key = PBKDF2(password, key_salt, dkLen=KEY_SIZE, count=ITERATIONS)
    return derived_key, key_salt

# Function: encrypt_file
# Purpose: Encrypts the file data using AES encryption (EAX mode).
# Inputs: file_data (bytes) - The file data to encrypt, encryption_key (bytes) - The encryption key.
# Returns: bytes - The encrypted file data.
def encrypt_file(file_data: bytes, encryption_key: bytes) -> bytes:
    cipher = AES.new(encryption_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    return base64.b64encode(cipher.nonce + tag + ciphertext)

# Function: decrypt_file
# Purpose: Decrypts the encrypted file data using AES encryption (EAX mode).
# Inputs: encrypted_bytes (bytes) - The encrypted file data, decryption_key (bytes) - The encryption key.
# Returns: bytes - The decrypted file data.
def decrypt_file(encrypted_bytes: bytes, decryption_key: bytes) -> bytes:
    decoded_data = base64.b64decode(encrypted_bytes)
    nonce = decoded_data[:NONCE_SIZE]
    tag = decoded_data[NONCE_SIZE:NONCE_SIZE + 16]
    ciphertext = decoded_data[NONCE_SIZE + 16:]
    cipher = AES.new(decryption_key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

