"""
Find files by size criteria recursively in a directory.
"""

import os
from pathlib import Path


def find_files_by_size(
    directory: str | Path,
    min_size: int = 0,
    max_size: int | None = None,
) -> list[tuple[str, int]]:
    """
    Find all files within specified size range recursively in a directory.

    Parameters
    ----------
    directory : str | Path
        The directory path to search in.
    min_size : int, optional
        Minimum file size in bytes (by default 0).
    max_size : int | None, optional
        Maximum file size in bytes, None for no limit (by default None).

    Returns
    -------
    list[tuple[str, int]]
        List of tuples containing (file_path, file_size_bytes).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If directory doesn't exist or size parameters are invalid.
    OSError
        If there's an error accessing files.

    Examples
    --------
    >>> find_files_by_size("/path/to/dir", min_size=1024)
    [('/path/to/dir/large_file.txt', 2048), ('/path/to/dir/image.jpg', 5120)]
    >>> find_files_by_size("/path/to/dir", max_size=500)
    [('/path/to/dir/small.txt', 256)]

    Notes
    -----
    The function follows symbolic links and includes their target size.
    Files that cannot be accessed are skipped without raising an error.

    Complexity
    ----------
    Time: O(n), Space: O(m) where n is total files and m is matching files.
    """
    # Input validation
    if not isinstance(directory, (str, Path)):
        raise TypeError(f"directory must be a string or Path, got {type(directory).__name__}")
    if not isinstance(min_size, int):
        raise TypeError(f"min_size must be an integer, got {type(min_size).__name__}")
    if max_size is not None and not isinstance(max_size, int):
        raise TypeError(f"max_size must be an integer or None, got {type(max_size).__name__}")
    
    # Convert to Path object
    dir_path = Path(directory)
    
    # Validate directory exists
    if not dir_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    # Validate size parameters
    if min_size < 0:
        raise ValueError(f"min_size must be non-negative, got {min_size}")
    if max_size is not None and max_size < 0:
        raise ValueError(f"max_size must be non-negative, got {max_size}")
    if max_size is not None and max_size < min_size:
        raise ValueError(f"max_size ({max_size}) must be >= min_size ({min_size})")
    
    matching_files: list[tuple[str, int]] = []
    
    try:
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    file_size = file_path.stat().st_size
                    
                    # Check size criteria
                    if file_size >= min_size:
                        if max_size is None or file_size <= max_size:
                            matching_files.append((str(file_path), file_size))
                except OSError:
                    # Skip files that cannot be accessed (permissions, broken links, etc.)
                    continue
    except OSError as e:
        raise OSError(f"Error accessing directory {directory}: {e}") from e
    
    return matching_files


__all__ = ['find_files_by_size']
