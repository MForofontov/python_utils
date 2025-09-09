"""
Find files by modification time criteria recursively in a directory.
"""

import os
from datetime import datetime, timedelta
from pathlib import Path


def find_files_by_mtime(
    directory: str | Path,
    days_old: int | None = None,
    newer_than: datetime | None = None,
    older_than: datetime | None = None,
) -> list[tuple[str, datetime]]:
    """
    Find files by modification time criteria recursively in a directory.

    Parameters
    ----------
    directory : str | Path
        The directory path to search in.
    days_old : int | None, optional
        Find files modified exactly N days ago (by default None).
    newer_than : datetime | None, optional
        Find files modified after this datetime (by default None).
    older_than : datetime | None, optional
        Find files modified before this datetime (by default None).

    Returns
    -------
    list[tuple[str, datetime]]
        List of tuples containing (file_path, modification_datetime).

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If directory doesn't exist or time parameters are invalid.
    OSError
        If there's an error accessing files.

    Examples
    --------
    >>> find_files_by_mtime("/path/to/dir", days_old=7)
    [('/path/to/dir/old_file.txt', datetime(2023, 1, 1, 12, 0))]
    >>> from datetime import datetime
    >>> cutoff = datetime(2023, 6, 1)
    >>> find_files_by_mtime("/path/to/dir", newer_than=cutoff)
    [('/path/to/dir/recent.txt', datetime(2023, 6, 15, 10, 30))]

    Notes
    -----
    If multiple time criteria are specified, all must be satisfied.
    The function uses modification time (mtime), not creation or access time.

    Complexity
    ----------
    Time: O(n), Space: O(m) where n is total files and m is matching files.
    """
    # Input validation
    if not isinstance(directory, (str, Path)):
        raise TypeError(f"directory must be a string or Path, got {type(directory).__name__}")
    if days_old is not None and not isinstance(days_old, int):
        raise TypeError(f"days_old must be an integer or None, got {type(days_old).__name__}")
    if newer_than is not None and not isinstance(newer_than, datetime):
        raise TypeError(f"newer_than must be a datetime or None, got {type(newer_than).__name__}")
    if older_than is not None and not isinstance(older_than, datetime):
        raise TypeError(f"older_than must be a datetime or None, got {type(older_than).__name__}")
    
    # Convert to Path object
    dir_path = Path(directory)
    
    # Validate directory exists
    if not dir_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    # Validate time parameters
    if days_old is not None and days_old < 0:
        raise ValueError(f"days_old must be non-negative, got {days_old}")
    if newer_than is not None and older_than is not None and newer_than >= older_than:
        raise ValueError("newer_than must be before older_than")
    
    # At least one time criterion must be specified
    if days_old is None and newer_than is None and older_than is None:
        raise ValueError("At least one time criterion must be specified")
    
    # Calculate time ranges
    current_time = datetime.now()
    
    if days_old is not None:
        target_date = current_time - timedelta(days=days_old)
        # For days_old, we want files from that specific day (24-hour window)
        day_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
    
    matching_files: list[tuple[str, datetime]] = []
    
    try:
        for root, _, files in os.walk(dir_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    mtime_timestamp = file_path.stat().st_mtime
                    mtime = datetime.fromtimestamp(mtime_timestamp)
                    
                    # Check time criteria
                    matches = True
                    
                    if days_old is not None:
                        if not (day_start <= mtime < day_end):
                            matches = False
                    
                    if newer_than is not None and mtime <= newer_than:
                        matches = False
                    
                    if older_than is not None and mtime >= older_than:
                        matches = False
                    
                    if matches:
                        matching_files.append((str(file_path), mtime))
                        
                except OSError:
                    # Skip files that cannot be accessed
                    continue
    except OSError as e:
        raise OSError(f"Error accessing directory {directory}: {e}") from e
    
    return matching_files


__all__ = ['find_files_by_mtime']
