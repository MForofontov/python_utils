

from datetime import datetime


def parse_date(date_string: str, formats: list[str] | None = None) -> datetime:
    """
    Parse a date string into a datetime object.

    Parameters
    ----------
    date_string : str
        The date string to parse.
    formats : list of str, optional
        List of date formats to try. If None, uses common formats.

    Returns
    -------
    datetime
        Parsed datetime object.

    Raises
    ------
    TypeError
        If date_string is not a string.
    ValueError
        If date_string cannot be parsed with any format.

    Examples
    --------
    >>> parse_date('2023-12-25 15:30:00')
    datetime(2023, 12, 25, 15, 30)
    >>> parse_date('2023-12-25')
    datetime(2023, 12, 25, 0, 0)

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if not isinstance(date_string, str):
        raise TypeError("date_string must be a string")
    if not date_string.strip():
        raise ValueError("date_string cannot be empty")
    # Default formats to try
    if formats is None:
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S.%f",
            "%m/%d/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S.%f",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M:%S.%f",
            "%d-%m-%Y %H:%M:%S",
            "%d-%m-%Y %H:%M:%S.%f",
            "%B %d, %Y %H:%M:%S",
            "%b %d, %Y %H:%M:%S",
            "%d %B %Y %H:%M:%S",
            "%d %b %Y %H:%M:%S",
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
        ]
    date_string = date_string.strip()
    for fmt in formats:
        try:
            parsed = datetime.strptime(date_string, fmt)
            return parsed
        except ValueError:
            continue
    raise ValueError(
        f"Unable to parse date string '{date_string}' with any of the provided formats"
    )
