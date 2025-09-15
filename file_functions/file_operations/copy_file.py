"""
File copying utility.

This module provides a function to copy files from source to destination,
preserving file contents and overwriting existing files.
"""

import shutil
import os


def copy_file(source: str, destination: str) -> None:
    """
    Copy a file from source to destination path.

    Parameters
    ----------
    source : str
        Path to the source file.
    destination : str
        Path to the destination file.

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.
    FileNotFoundError
        If source file does not exist.

    Examples
    --------
    >>> copy_file("source.txt", "destination.txt")
    >>> copy_file("/path/to/file.txt", "/new/location/file.txt")

    Notes
    -----
    This function will overwrite the destination file if it already exists.
    The destination directory will be created if it doesn't exist.

    Complexity
    ----------
    Time: O(n), Space: O(1) where n is the size of the file
    """
    # Input validation
    if not isinstance(source, str):
        raise TypeError(f"source must be a string, got {type(source).__name__}")
    if not isinstance(destination, str):
        raise TypeError(f"destination must be a string, got {type(destination).__name__}")
    
    # Value validation
    if not source:
        raise ValueError("source path cannot be empty")
    if not destination:
        raise ValueError("destination path cannot be empty")
    
    # Check if source file exists
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source file not found: {source}")
    
    if not os.path.isfile(source):
        raise ValueError(f"Source is not a file: {source}")
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(destination)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Copy the file
    shutil.copy2(source, destination)


__all__ = ["copy_file"]
