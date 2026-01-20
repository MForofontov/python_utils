"""Format seconds into human-readable duration strings."""


def format_duration(
    seconds: int | float,
    precision: int = 2,
    long_format: bool = False,
) -> str:
    """
    Format seconds into a human-readable duration string.

    Parameters
    ----------
    seconds : int | float
        Duration in seconds.
    precision : int, optional
        Maximum number of time units to display (by default 2).
    long_format : bool, optional
        Use long format ("2 hours 30 minutes") vs short ("2h 30m") (by default False).

    Returns
    -------
    str
        Formatted duration string.

    Raises
    ------
    TypeError
        If seconds is not a number, precision is not an integer, or long_format is not a boolean.
    ValueError
        If seconds is negative or precision is less than 1.

    Examples
    --------
    >>> format_duration(90)
    '1m 30s'
    >>> format_duration(90, long_format=True)
    '1 minute 30 seconds'
    >>> format_duration(3665)
    '1h 1m'
    >>> format_duration(3665, precision=3)
    '1h 1m 5s'
    >>> format_duration(86400)
    '1d 0h'
    >>> format_duration(90.5)
    '1m 30s'
    >>> format_duration(0)
    '0s'
    >>> format_duration(0, long_format=True)
    '0 seconds'

    Notes
    -----
    Time units used: years (365 days), weeks, days, hours, minutes, seconds

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    # Input validation
    if not isinstance(seconds, (int, float)):
        raise TypeError(f"seconds must be a number, got {type(seconds).__name__}")
    if not isinstance(precision, int):
        raise TypeError(f"precision must be an integer, got {type(precision).__name__}")
    if not isinstance(long_format, bool):
        raise TypeError(
            f"long_format must be a boolean, got {type(long_format).__name__}"
        )

    if seconds < 0:
        raise ValueError(f"seconds must be non-negative, got {seconds}")
    if precision < 1:
        raise ValueError(f"precision must be at least 1, got {precision}")

    # Handle zero case
    if seconds == 0:
        return "0 seconds" if long_format else "0s"

    # Convert to integer seconds
    total_seconds = int(seconds)

    # Define time units
    units = [
        ("year", "y", 365 * 24 * 60 * 60),
        ("week", "w", 7 * 24 * 60 * 60),
        ("day", "d", 24 * 60 * 60),
        ("hour", "h", 60 * 60),
        ("minute", "m", 60),
        ("second", "s", 1),
    ]

    # Calculate each unit
    parts = []
    remaining = total_seconds

    for unit_long, unit_short, unit_seconds in units:
        if remaining >= unit_seconds:
            value = remaining // unit_seconds
            remaining %= unit_seconds

            if long_format:
                # Pluralize if needed
                unit_name = unit_long if value == 1 else f"{unit_long}s"
                parts.append(f"{value} {unit_name}")
            else:
                parts.append(f"{value}{unit_short}")

            # Stop if we've reached precision limit
            if len(parts) >= precision:
                break

    # Join parts
    if long_format:
        return " ".join(parts)
    else:
        return " ".join(parts)


__all__ = ["format_duration"]
