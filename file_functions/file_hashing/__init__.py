"""
File hashing module: Calculate and compare file hashes.

This module provides utilities for calculating various hash values
(MD5, SHA1, SHA256) for files and comparing files by their hashes.
"""

from .calculate_md5_hash import calculate_md5_hash
from .calculate_sha1_hash import calculate_sha1_hash
from .calculate_sha256_hash import calculate_sha256_hash
from .compare_file_hashes import compare_file_hashes

__all__ = [
    'calculate_md5_hash',
    'calculate_sha1_hash',
    'calculate_sha256_hash',
    'compare_file_hashes',
]

__version__ = '1.0.0'
