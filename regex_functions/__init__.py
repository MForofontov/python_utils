"""
Regular Expression Utilities Module.

This module provides essential regex-based utilities for common text processing tasks,
including email/URL extraction, HTML cleaning, and filename sanitization.
"""

# Extraction functions
from .extract_emails import extract_emails
from .extract_urls import extract_urls

# Cleaning functions
from .remove_html_tags import remove_html_tags
from .remove_extra_whitespace import remove_extra_whitespace
from .sanitize_filename import sanitize_filename


__all__ = [
    # Extraction
    'extract_emails',
    'extract_urls',
    # Cleaning
    'remove_html_tags',
    'remove_extra_whitespace',
    'sanitize_filename',
]

from .._version import __version__
