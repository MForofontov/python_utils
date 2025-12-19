"""
Module for getting file size.
"""

import os


def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.

    Parameters
    ----------
    file_path : str
        Path to the file.

    Returns
    -------
    int
        File size in bytes.

    Raises
    ------
    TypeError
        If file_path is not a string.
    FileNotFoundError
        If file does not exist.
    IsADirectoryError
        If path points to a directory.

    Examples
    --------
    >>> # Assuming a file exists
    >>> size = get_file_size('/etc/passwd')
    >>> size > 0
    True
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")

    if os.path.isdir(file_path):
        raise IsADirectoryError(f"Path is a directory, not a file: {file_path}")

    return os.path.getsize(file_path)


__all__ = ['get_file_size']
