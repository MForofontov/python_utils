"""
CLI (Command Line Interface) and system utility functions for cross-platform
system information, process management, file operations, and command execution.

This module provides utilities that work across different operating systems
using cross-platform libraries like psutil and standard library modules.
"""

from .check_command_exists import check_command_exists
from .execute_command import execute_command
from .get_cpu_info import get_cpu_info
from .get_current_user import get_current_user
from .get_disk_usage import get_disk_usage
from .get_environment_variable import get_environment_variable
from .get_file_size import get_file_size
from .get_hostname import get_hostname
from .get_memory_info import get_memory_info
from .get_network_info import get_network_info
from .get_uptime import get_uptime
from .is_process_running import is_process_running
from .kill_process import kill_process
from .list_directories import list_directories
from .list_files import list_files
from .set_environment_variable import set_environment_variable

__all__ = [
    # Command execution
    "execute_command",
    "check_command_exists",
    # Environment variables
    "get_environment_variable",
    "set_environment_variable",
    # System information
    "get_cpu_info",
    "get_disk_usage",
    "get_memory_info",
    "get_network_info",
    "get_uptime",
    "get_current_user",
    "get_hostname",
    # Process management
    "is_process_running",
    "kill_process",
    # File operations
    "get_file_size",
    "list_files",
    "list_directories",
]

from _version import __version__
