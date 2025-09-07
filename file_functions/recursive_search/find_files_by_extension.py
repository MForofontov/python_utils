"""
Find files by extension recursively in a directory.
"""

import os
from pathlib import Path
from typing import Any


def find_files_by_extension(
    directory: str | Path,
    extension: str,
    case_sensitive: bool = False,
) -> list[str]:
    """
    Find all files with a specific extension recursively in a directory.

    Parameters
    ----------
    directory : str | Path
        The directory path to search in.
    extension : str
        The file extension to search for (with or without leading dot).
    case_sensitive : bool, optional
        Whether the search should be case sensitive (by default False).

    Returns
    -------
    list[str]
        List of absolute file paths with the specified extension.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If directory doesn't exist or extension is empty.
    OSError
        If there's an error accessing the directory.

    Examples
    --------
    >>> find_files_by_extension("/path/to/dir", ".py")
    ['/path/to/dir/script.py', '/path/to/dir/subdir/module.py']
    >>> find_files_by_extension("/path/to/dir", "txt", case_sensitive=True)
    ['/path/to/dir/file.txt']

    Notes
    -----
    The function searches recursively through all subdirectories.
    Hidden files and directories are included in the search.

    Complexity
    ----------
    Time: O(n), Space: O(m) where n is total files and m is matching files.
    """
    # Input validation
    if not isinstance(directory, (str, Path)):
        raise TypeError(f"directory must be a string or Path, got {type(directory).__name__}")
    if not isinstance(extension, str):
        raise TypeError(f"extension must be a string, got {type(extension).__name__}")
    if not isinstance(case_sensitive, bool):
        raise TypeError(f"case_sensitive must be a boolean, got {type(case_sensitive).__name__}")
    
    # Convert to Path object
    dir_path = Path(directory)
    
    # Validate directory exists
    if not dir_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    # Validate extension
    if not extension.strip():
        raise ValueError("Extension cannot be empty")
    
    # Normalize extension (ensure it starts with a dot)
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # Normalize case if not case sensitive
    if not case_sensitive:
        extension = extension.lower()
    
    matching_files: list[str] = []
    
    try:
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_ext = Path(file).suffix
                if not case_sensitive:
                    file_ext = file_ext.lower()
                
                if file_ext == extension:
                    matching_files.append(str(Path(root) / file))
    except OSError as e:
        raise OSError(f"Error accessing directory {directory}: {e}") from e
    
    return matching_files


__all__ = ['find_files_by_extension']
