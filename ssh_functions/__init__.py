"""
ssh_functions: Utilities for SSH operations.

This module provides functions for executing commands and managing SSH connections.
Includes both local (subprocess-based) and remote (paramiko-based) implementations.

Usage:
    # For local SSH execution (using system ssh/scp commands)
    from ssh_functions.local import ssh_execute_command, ssh_copy_file
    
    # For remote SSH execution (using paramiko library)
    from ssh_functions.remote import ssh_execute_command, ssh_copy_file
"""

# Import submodules for easy access
from . import local, remote

# Import from local by default for backward compatibility
from .ssh_check_connection import ssh_check_connection
from .ssh_copy_file import ssh_copy_file
from .ssh_execute_command import ssh_execute_command
from .ssh_execute_script import ssh_execute_script

__all__ = [
    "ssh_execute_command",
    "ssh_copy_file",
    "ssh_check_connection",
    "ssh_execute_script",
    "local",
    "remote",
]

