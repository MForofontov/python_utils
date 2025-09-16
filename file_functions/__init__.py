"""
File functions module: Comprehensive file and directory utilities.

This module provides organized utilities for file and directory operations,
path manipulation, data format handling, recursive search, file hashing,
and temporary file management.
"""

# Import from organized modules
from .data_format_operations import *
from .directory_operations import *
from .file_hashing import *
from .file_operations import *
from .path_operations import *
from .recursive_search import *
from .temp_management import *

__all__ = [
    # Path operations
    "file_basename",
    "get_paths_dict",
    "get_paths_in_directory",
    "get_paths_in_directory_with_suffix",
    "join_paths",
    # Directory operations
    "cleanup",
    "copy_folder",
    "create_directory",
    "merge_folders",
    # File operations
    "check_and_delete_file",
    "concat_files",
    "copy_file",
    "read_lines",
    "write_lines",
    "write_to_file",
    # Data format operations
    "json_to_dict",
    "read_tabular",
    "tsv_to_dict",
    "write_dict_to_json",
    "write_dict_to_tsv",
    # Recursive search functions
    "find_files_by_extension",
    "find_files_by_pattern",
    "find_files_by_size",
    "find_files_by_mtime",
    # File hashing functions
    "calculate_md5_hash",
    "calculate_sha1_hash",
    "calculate_sha256_hash",
    "compare_file_hashes",
    # Temporary management functions
    "create_temp_file",
    "create_temp_directory",
    "cleanup_temp_files",
    "get_temp_dir_info",
]
