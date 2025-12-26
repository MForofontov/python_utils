"""Format byte sizes into human-readable strings."""


def format_file_size(
    size_bytes: int | float,
    binary: bool = True,
    precision: int = 2,
) -> str:
    """
    Format a byte size into a human-readable string.

    Parameters
    ----------
    size_bytes : int | float
        The size in bytes to format.
    binary : bool, optional
        Use binary units (1024) if True, decimal units (1000) if False (by default True).
    precision : int, optional
        Number of decimal places to display (by default 2).

    Returns
    -------
    str
        Formatted size string (e.g., "1.50 MB", "2.34 GiB").

    Raises
    ------
    TypeError
        If size_bytes is not a number, binary is not a boolean, or precision is not an integer.
    ValueError
        If size_bytes is negative or precision is negative.

    Examples
    --------
    >>> format_file_size(1536)
    '1.50 KiB'
    >>> format_file_size(1536, binary=False)
    '1.54 KB'
    >>> format_file_size(1073741824)
    '1.00 GiB'
    >>> format_file_size(1000000000, binary=False)
    '1.00 GB'
    >>> format_file_size(0)
    '0 B'
    >>> format_file_size(512, precision=0)
    '1 KiB'

    Notes
    -----
    Binary units (1024-based): B, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB
    Decimal units (1000-based): B, KB, MB, GB, TB, PB, EB, ZB, YB

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Input validation
    if not isinstance(size_bytes, (int, float)):
        raise TypeError(
            f"size_bytes must be a number, got {type(size_bytes).__name__}"
        )
    if not isinstance(binary, bool):
        raise TypeError(f"binary must be a boolean, got {type(binary).__name__}")
    if not isinstance(precision, int):
        raise TypeError(f"precision must be an integer, got {type(precision).__name__}")

    if size_bytes < 0:
        raise ValueError(f"size_bytes must be non-negative, got {size_bytes}")
    if precision < 0:
        raise ValueError(f"precision must be non-negative, got {precision}")

    # Define units
    if binary:
        units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
        divisor = 1024
    else:
        units = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
        divisor = 1000

    # Handle zero case
    if size_bytes == 0:
        return "0 B"

    # Find appropriate unit
    size = float(size_bytes)
    unit_index = 0

    while size >= divisor and unit_index < len(units) - 1:
        size /= divisor
        unit_index += 1

    # Format result
    if unit_index == 0:  # Bytes - no decimal places
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.{precision}f} {units[unit_index]}"


__all__ = ["format_file_size"]
