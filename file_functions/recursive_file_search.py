"""
Recursive file search utilities.

This module provides functions for recursively searching files and directories
with various filtering and matching capabilities.
"""

import os
import re
from pathlib import Path
from typing import Generator, Pattern, Any
from collections.abc import Callable


def find_files_by_extension(
    directory: str | Path,
    extension: str,
    recursive: bool = True,
) -> list[Path]:
    """
    Find all files with a specific extension in a directory.

    Parameters
    ----------
    directory : str | Path
        The directory to search in.
    extension : str
        The file extension to search for (with or without leading dot).
    recursive : bool, optional
        Whether to search recursively in subdirectories (by default True).

    Returns
    -------
    list[Path]
        List of Path objects for files with the specified extension.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If directory doesn't exist or extension is empty.

    Examples
    --------
    >>> find_files_by_extension("/path/to/dir", ".py")
    [Path('/path/to/dir/file1.py'), Path('/path/to/dir/subdir/file2.py')]
    >>> find_files_by_extension("/path/to/dir", "txt", recursive=False)
    [Path('/path/to/dir/file.txt')]

    Notes
    -----
    Extension matching is case-insensitive.

    Complexity
    ----------
    Time: O(n), Space: O(m) where n is number of files/dirs, m is matching files
    """
    # Input validation
    if not isinstance(directory, (str, Path)):
        raise TypeError(f"directory must be str or Path, got {type(directory).__name__}")
    if not isinstance(extension, str):
        raise TypeError(f"extension must be a string, got {type(extension).__name__}")
    if not isinstance(recursive, bool):
        raise TypeError(f"recursive must be a boolean, got {type(recursive).__name__}")
    
    directory_path = Path(directory)
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not directory_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    if not extension.strip():
        raise ValueError("Extension cannot be empty")
    
    # Normalize extension (ensure it starts with a dot)
    if not extension.startswith('.'):
        extension = '.' + extension
    
    extension = extension.lower()
    
    # Search for files
    if recursive:
        pattern = f"**/*{extension}"
        files = list(directory_path.glob(pattern))
    else:
        pattern = f"*{extension}"
        files = list(directory_path.glob(pattern))
    
    # Filter to only include files (not directories)
    return [f for f in files if f.is_file()]


def find_files_by_pattern(
    directory: str | Path,
    pattern: str,
    recursive: bool = True,
    case_sensitive: bool = False,
) -> list[Path]:
    """
    Find files matching a regex pattern in their names.

    Parameters
    ----------
    directory : str | Path
        The directory to search in.
    pattern : str
        The regex pattern to match against filenames.
    recursive : bool, optional
        Whether to search recursively in subdirectories (by default True).
    case_sensitive : bool, optional
        Whether pattern matching is case-sensitive (by default False).

    Returns
    -------
    list[Path]
        List of Path objects for files matching the pattern.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If directory doesn't exist or pattern is invalid.

    Examples
    --------
    >>> find_files_by_pattern("/path/to/dir", r"test_.*\.py")
    [Path('/path/to/dir/test_file.py'), Path('/path/to/dir/test_utils.py')]
    >>> find_files_by_pattern("/path/to/dir", r"^config", recursive=False)
    [Path('/path/to/dir/config.json')]

    Notes
    -----
    Uses Python regex patterns for filename matching.

    Complexity
    ----------
    Time: O(n*m), Space: O(k) where n=files, m=pattern complexity, k=matches
    """
    # Input validation
    if not isinstance(directory, (str, Path)):
        raise TypeError(f"directory must be str or Path, got {type(directory).__name__}")
    if not isinstance(pattern, str):
        raise TypeError(f"pattern must be a string, got {type(pattern).__name__}")
    if not isinstance(recursive, bool):
        raise TypeError(f"recursive must be a boolean, got {type(recursive).__name__}")
    if not isinstance(case_sensitive, bool):
        raise TypeError(f"case_sensitive must be a boolean, got {type(case_sensitive).__name__}")
    
    directory_path = Path(directory)
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not directory_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    if not pattern.strip():
        raise ValueError("Pattern cannot be empty")
    
    # Compile regex pattern
    try:
        flags = 0 if case_sensitive else re.IGNORECASE
        compiled_pattern = re.compile(pattern, flags)
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {e}")
    
    # Search for files
    matching_files = []
    search_pattern = "**/*" if recursive else "*"
    
    for file_path in directory_path.glob(search_pattern):
        if file_path.is_file() and compiled_pattern.search(file_path.name):
            matching_files.append(file_path)
    
    return matching_files


def find_files_by_size(
    directory: str | Path,
    min_size: int | None = None,
    max_size: int | None = None,
    recursive: bool = True,
) -> list[tuple[Path, int]]:
    """
    Find files within a specific size range.

    Parameters
    ----------
    directory : str | Path
        The directory to search in.
    min_size : int | None, optional
        Minimum file size in bytes (by default None).
    max_size : int | None, optional
        Maximum file size in bytes (by default None).
    recursive : bool, optional
        Whether to search recursively in subdirectories (by default True).

    Returns
    -------
    list[tuple[Path, int]]
        List of tuples containing (file_path, file_size_bytes).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If directory doesn't exist or size parameters are invalid.

    Examples
    --------
    >>> find_files_by_size("/path/to/dir", min_size=1024)
    [(Path('/path/to/dir/large_file.txt'), 2048)]
    >>> find_files_by_size("/path/to/dir", max_size=1000)
    [(Path('/path/to/dir/small_file.txt'), 512)]

    Notes
    -----
    File sizes are returned in bytes.

    Complexity
    ----------
    Time: O(n), Space: O(m) where n is number of files, m is matching files
    """
    # Input validation
    if not isinstance(directory, (str, Path)):
        raise TypeError(f"directory must be str or Path, got {type(directory).__name__}")
    if min_size is not None and not isinstance(min_size, int):
        raise TypeError(f"min_size must be an integer or None, got {type(min_size).__name__}")
    if max_size is not None and not isinstance(max_size, int):
        raise TypeError(f"max_size must be an integer or None, got {type(max_size).__name__}")
    if not isinstance(recursive, bool):
        raise TypeError(f"recursive must be a boolean, got {type(recursive).__name__}")
    
    directory_path = Path(directory)
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not directory_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    if min_size is not None and min_size < 0:
        raise ValueError(f"min_size must be non-negative, got {min_size}")
    if max_size is not None and max_size < 0:
        raise ValueError(f"max_size must be non-negative, got {max_size}")
    if min_size is not None and max_size is not None and min_size > max_size:
        raise ValueError("min_size cannot be greater than max_size")
    
    # Search for files
    matching_files = []
    search_pattern = "**/*" if recursive else "*"
    
    for file_path in directory_path.glob(search_pattern):
        if file_path.is_file():
            try:
                file_size = file_path.stat().st_size
                
                # Check size constraints
                if min_size is not None and file_size < min_size:
                    continue
                if max_size is not None and file_size > max_size:
                    continue
                
                matching_files.append((file_path, file_size))
            except OSError:
                # Skip files that can't be accessed
                continue
    
    return matching_files


def walk_directory_tree(
    directory: str | Path,
    filter_func: Callable[[Path], bool] | None = None,
) -> Generator[Path, None, None]:
    """
    Walk through directory tree yielding file paths.

    Parameters
    ----------
    directory : str | Path
        The directory to walk through.
    filter_func : Callable[[Path], bool] | None, optional
        Optional filter function to apply to each path (by default None).

    Yields
    ------
    Path
        File paths in the directory tree.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If directory doesn't exist.

    Examples
    --------
    >>> list(walk_directory_tree("/path/to/dir"))
    [Path('/path/to/dir/file1.txt'), Path('/path/to/dir/subdir/file2.py')]
    >>> py_filter = lambda p: p.suffix == '.py'
    >>> list(walk_directory_tree("/path/to/dir", py_filter))
    [Path('/path/to/dir/subdir/file2.py')]

    Notes
    -----
    Uses a generator for memory-efficient directory traversal.

    Complexity
    ----------
    Time: O(n), Space: O(d) where n is number of files, d is directory depth
    """
    # Input validation
    if not isinstance(directory, (str, Path)):
        raise TypeError(f"directory must be str or Path, got {type(directory).__name__}")
    if filter_func is not None and not callable(filter_func):
        raise TypeError("filter_func must be callable or None")
    
    directory_path = Path(directory)
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not directory_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    # Walk through directory tree
    for root, dirs, files in os.walk(directory_path):
        root_path = Path(root)
        
        for file_name in files:
            file_path = root_path / file_name
            
            # Apply filter if provided
            if filter_func is None or filter_func(file_path):
                yield file_path


def find_duplicate_files(
    directory: str | Path,
    compare_content: bool = False,
    recursive: bool = True,
) -> dict[str, list[Path]]:
    """
    Find duplicate files in a directory based on name or content.

    Parameters
    ----------
    directory : str | Path
        The directory to search in.
    compare_content : bool, optional
        Whether to compare file contents for duplicates (by default False).
    recursive : bool, optional
        Whether to search recursively in subdirectories (by default True).

    Returns
    -------
    dict[str, list[Path]]
        Dictionary mapping duplicate identifiers to lists of file paths.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If directory doesn't exist.

    Examples
    --------
    >>> find_duplicate_files("/path/to/dir")
    {'file.txt': [Path('/path/to/dir/file.txt'), Path('/path/to/dir/copy/file.txt')]}
    >>> find_duplicate_files("/path/to/dir", compare_content=True)
    {'content_hash_123': [Path('/path/to/dir/file1.txt'), Path('/path/to/dir/file2.txt')]}

    Notes
    -----
    When compare_content=True, uses file content hashing for comparison.

    Complexity
    ----------
    Time: O(n*m), Space: O(n) where n=files, m=avg file size (if comparing content)
    """
    # Input validation
    if not isinstance(directory, (str, Path)):
        raise TypeError(f"directory must be str or Path, got {type(directory).__name__}")
    if not isinstance(compare_content, bool):
        raise TypeError(f"compare_content must be a boolean, got {type(compare_content).__name__}")
    if not isinstance(recursive, bool):
        raise TypeError(f"recursive must be a boolean, got {type(recursive).__name__}")
    
    directory_path = Path(directory)
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not directory_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    # Group files by identifier
    file_groups: dict[str, list[Path]] = {}
    search_pattern = "**/*" if recursive else "*"
    
    for file_path in directory_path.glob(search_pattern):
        if file_path.is_file():
            try:
                if compare_content:
                    # Use content hash as identifier
                    import hashlib
                    hasher = hashlib.md5()
                    with open(file_path, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hasher.update(chunk)
                    identifier = hasher.hexdigest()
                else:
                    # Use filename as identifier
                    identifier = file_path.name
                
                if identifier not in file_groups:
                    file_groups[identifier] = []
                file_groups[identifier].append(file_path)
            except (OSError, IOError):
                # Skip files that can't be accessed
                continue
    
    # Return only groups with duplicates
    return {k: v for k, v in file_groups.items() if len(v) > 1}


__all__ = [
    'find_files_by_extension',
    'find_files_by_pattern',
    'find_files_by_size',
    'walk_directory_tree',
    'find_duplicate_files',
]
