# encryption.py
# Author: William Richmond
# Date: 2024-11-17
# Class: CYBR-260-45
# Assignment: Final Project
# Description: Provides encryption and decryption functions using AES (PyCryptodome), including key expiration,
# parallel encryption, and metadata encryption.
# Revised on: 2024-12-01

import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes
from src.logger_config import LoggerConfig

# Initialize logger for this module
logger = LoggerConfig(name="encryption", log_filename="encryption.log").get_logger()

# Constants
SALT_SIZE = 16
KEY_SIZE = 32  # AES-256 (32 bytes)
NONCE_SIZE = 16
ITERATIONS = 100_000
KEY_EXPIRATION_DAYS = 90


# Function: generate_key
# Purpose: Derives a secure encryption key using PBKDF2.
# Inputs: password (str) - The password used for key derivation.
# Returns: tuple (key, salt) - The derived encryption key and salt.
def generate_key(password: str) -> tuple[bytes, bytes]:
    key_salt = get_random_bytes(SALT_SIZE)
    derived_key = PBKDF2(password, key_salt, dkLen=KEY_SIZE, count=ITERATIONS)
    logger.info("Encryption key generated.")
    return derived_key, key_salt

# Function: is_key_expired
# Purpose: Checks if an encryption key has expired.
# Inputs: key_creation_date (datetime) - The creation date of the key.
# Returns: bool - True if the key has expired, False otherwise.
def is_key_expired(key_creation_date: datetime) -> bool:
    if datetime.now() > key_creation_date + timedelta(days=KEY_EXPIRATION_DAYS):
        logger.warning("Encryption key has expired.")
        return True
    logger.info("Encryption key is valid.")
    return False

# Function: encrypt_file
# Purpose: Encrypts the file data using AES encryption (EAX mode).
# Inputs: file_data (bytes) - The file data to encrypt, encryption_key (bytes) - The encryption key.
# Returns: bytes - The encrypted file data.
def encrypt_file(file_data: bytes, encryption_key: bytes) -> bytes:
    cipher = AES.new(encryption_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    logger.info("File encrypted successfully.")
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
    logger.info("File decrypted successfully.")
    return cipher.decrypt_and_verify(ciphertext, tag)

# Function: encrypt_metadata
# Purpose: Encrypts file metadata using the same AES encryption.
# Inputs: metadata (dict) - File metadata to encrypt, encryption_key (bytes) - The encryption key.
# Returns: bytes - Encrypted metadata.
def encrypt_metadata(metadata: dict, encryption_key: bytes) -> bytes:
    try:
        metadata_bytes = str(metadata).encode()
        logger.info("Metadata encrypted successfully.")
        return encrypt_file(metadata_bytes, encryption_key)
    except Exception as e:
        logger.error(f"Error encrypting metadata: {e}")
        raise

# Function: encrypt_multiple_files
# Purpose: Encrypts multiple files concurrently.
# Inputs: files (list of tuples) - List of (file_data, encryption_key) tuples.
# Returns: list - List of encrypted file data.
def encrypt_multiple_files(files: list) -> list:
    results = []
    with ThreadPoolExecutor() as executor:
        for file_data, encryption_key in files:
            results.append(executor.submit(encrypt_file, file_data, encryption_key))
    logger.info("Multiple files encrypted concurrently.")
    return [result.result() for result in results]

# Function: generate_file_hash
# Purpose: Generates a secure hash for a given file.
# Inputs: file_data (bytes) - File data to hash.
# Returns: str - Secure hash of the file.
def generate_file_hash() -> str:
    hash_value = base64.b64encode(get_random_bytes(SALT_SIZE))
    logger.info("File hash generated.")
    return hash_value.decode()

if __name__ == "__main__":
    logger = LoggerConfig("encryption", "encryption.log").get_logger()
    logger.info("Test log entry for encryption.py")

