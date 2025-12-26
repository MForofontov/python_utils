"""Format datetime object as string."""

from datetime import datetime


def format_date(date_obj: datetime, format_string: str = "%Y-%m-%d") -> str:
    """
    Format a datetime object into a string.

    Parameters
    ----------
    date_obj : datetime
        The datetime object to format.
    format_string : str, optional
        The format string to use (default: '%Y-%m-%d').

    Returns
    -------
    str
        Formatted date string.

    Raises
    ------
    TypeError
        If date_obj is not a datetime object, or format_string is not a string.
    ValueError
        If format_string is invalid or empty.

    Examples
    --------
    >>> from datetime import datetime
    >>> format_date(datetime(2023, 12, 25))
    '2023-12-25'
    >>> format_date(datetime(2023, 12, 25), '%B %d, %Y')
    'December 25, 2023'
    """
    if not isinstance(date_obj, datetime):
        raise TypeError("date_obj must be a datetime object")
    if not isinstance(format_string, str):
        raise TypeError("format_string must be a string")
    if not format_string.strip():
        raise ValueError("format_string cannot be empty")
    return date_obj.strftime(format_string)
