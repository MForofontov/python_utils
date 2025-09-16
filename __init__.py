"""
Python Utilities Library.

A comprehensive collection of reusable Python functions, classes, and decorators
organized into specialized modules for enterprise-grade utility libraries.
"""

# Import all modules
try:
    from asyncio_functions import *
    from compression_functions import *
    from data_types import *
    from data_validation import *
    from datetime_functions import *
    from decorators import *
    from env_config_functions import *
    from file_functions import *
    from http_functions import *
    from iterable_functions import *
    from json_functions import *
    from linux_functions import *
    from logger_functions import *
    from logging_debugging import *
    from mathematical_functions import *
    from multiprocessing_functions import *
    from print_functions import *
    from security_functions import *
    from ssh_functions import *
    from strings_utility import *
except ImportError:
    # Fallback for when importing as a package
    from .asyncio_functions import *
    from .compression_functions import *
    from .data_types import *
    from .data_validation import *
    from .datetime_functions import *
    from .decorators import *
    from .env_config_functions import *
    from .file_functions import *
    from .http_functions import *
    from .iterable_functions import *
    from .json_functions import *
    from .linux_functions import *
    from .logger_functions import *
    from .logging_debugging import *
    from .mathematical_functions import *
    from .multiprocessing_functions import *
    from .print_functions import *
    from .security_functions import *
    from .ssh_functions import *
    from .strings_utility import *

# Version information
__version__ = "1.0.0"
__author__ = "Python Utils Contributors"
__license__ = "MIT"
