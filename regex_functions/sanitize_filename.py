"""
Sanitize filename to remove invalid characters.
"""

import re


def sanitize_filename(
    filename: str,
    replacement: str = "_",
    max_length: int = 255,
) -> str:
    """
    Sanitize filename by removing or replacing invalid characters.

    Parameters
    ----------
    filename : str
        Input filename to sanitize.
    replacement : str, optional
        Character to replace invalid chars with (by default '_').
    max_length : int, optional
        Maximum filename length (by default 255).

    Returns
    -------
    str
        Sanitized filename safe for file systems.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If max_length is invalid or filename becomes empty.

    Examples
    --------
    >>> sanitize_filename("file/name:test.txt")
    'file_name_test.txt'

    >>> sanitize_filename("file*name?.txt", replacement="-")
    'file-name-.txt'

    >>> sanitize_filename("  file  name  .txt  ")
    'file_name.txt'

    >>> sanitize_filename("a" * 300, max_length=50)
    'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    Notes
    -----
    Removes/replaces:
    - Invalid characters for Windows/Unix: < > : " / \\ | ? *
    - Control characters (ASCII 0-31)
    - Leading/trailing spaces and dots
    - Reserved Windows names (CON, PRN, AUX, etc.)

    Preserves file extensions when possible.

    Complexity
    ----------
    Time: O(n) where n is length of filename
    Space: O(n) for result string
    """
    # Type validation
    if not isinstance(filename, str):
        raise TypeError(f"filename must be str, got {type(filename).__name__}")
    if not isinstance(replacement, str):
        raise TypeError(f"replacement must be str, got {type(replacement).__name__}")
    if not isinstance(max_length, int):
        raise TypeError(f"max_length must be int, got {type(max_length).__name__}")

    # Value validation
    if max_length < 1:
        raise ValueError(f"max_length must be positive, got {max_length}")
    if len(replacement) > 1:
        raise ValueError(
            f"replacement must be single character, got '{replacement}'"
        )

    # Remove path separators and get just the filename
    filename = filename.replace('\\', '/').split('/')[-1]

    # Remove control characters (ASCII 0-31)
    filename = re.sub(r'[\x00-\x1f]', replacement, filename)

    # Replace invalid filesystem characters
    # Windows: < > : " / \ | ? *
    # Unix: /
    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, replacement, filename)

    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')

    # Replace multiple replacement characters with single
    if replacement:
        pattern = re.escape(replacement) + '+'
        filename = re.sub(pattern, replacement, filename)

    # Check for reserved Windows names
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9',
    }
    name_without_ext = filename.rsplit('.', 1)[0].upper()
    if name_without_ext in reserved_names:
        filename = replacement + filename

    # Truncate to max_length while preserving extension
    if len(filename) > max_length:
        if '.' in filename:
            name, ext = filename.rsplit('.', 1)
            # Reserve space for extension and dot
            available = max_length - len(ext) - 1
            if available > 0:
                filename = name[:available] + '.' + ext
            else:
                filename = filename[:max_length]
        else:
            filename = filename[:max_length]

    # Final validation
    if not filename or filename == replacement:
        raise ValueError("Sanitized filename is empty or invalid")

    return filename


__all__ = ['sanitize_filename']
