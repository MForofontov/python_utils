"""
Security utilities for password hashing, token generation, and encryption.

This module provides comprehensive security utilities including:
- Password hashing and verification (bcrypt, PBKDF2)
- Token generation (secure tokens, URL-safe tokens, JWT)
- Encryption and decryption helpers (AES, XOR)
"""


from .password_hashing.hash_password_bcrypt import hash_password_bcrypt
from .password_hashing.verify_password_bcrypt import verify_password_bcrypt
from .password_hashing.hash_password_pbkdf2 import hash_password_pbkdf2
from .password_hashing.verify_password_pbkdf2 import verify_password_pbkdf2

from .token_generation.generate_secure_token import generate_secure_token
from .token_generation.generate_url_safe_token import generate_url_safe_token
from .token_generation.generate_jwt_token import generate_jwt_token
from .token_generation.verify_jwt_token import verify_jwt_token

from .encryption_helpers.encrypt_data_aes import encrypt_data_aes
from .encryption_helpers.decrypt_data_aes import decrypt_data_aes
from .encryption_helpers.encrypt_xor import encrypt_xor
from .encryption_helpers.decrypt_xor import decrypt_xor

__all__ = [
    # Password hashing
    "hash_password_bcrypt",
    "verify_password_bcrypt",
    "hash_password_pbkdf2",
    "verify_password_pbkdf2",
    # Token generation
    "generate_secure_token",
    "generate_url_safe_token",
    "generate_jwt_token",
    "verify_jwt_token",
    # Encryption helpers
    "encrypt_data_aes",
    "decrypt_data_aes",
    "encrypt_xor",
    "decrypt_xor",
]
