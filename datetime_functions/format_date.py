"""Date formatting functionality."""

from datetime import date, datetime


def format_date(date_obj: datetime | date, format_string: str = "%Y-%m-%d") -> str:
    """
    Format a datetime or date object into a string.

    Parameters
    ----------
    date_obj : datetime or date
        The datetime or date object to format.
    format_string : str, optional
        The format string to use (default: '%Y-%m-%d').

    Returns
    -------
    str
        Formatted date string.

    Raises
    ------
    TypeError
        If date_obj is not a datetime or date object, or format_string is not a string.
    ValueError
        If format_string is invalid or empty.

    Examples
    --------
    >>> from datetime import date
    >>> format_date(date(2023, 12, 25))
    '2023-12-25'
    >>> format_date(date(2023, 12, 25), '%B %d, %Y')
    'December 25, 2023'
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")

    if not isinstance(format_string, str):
        raise TypeError("format_string must be a string")

    if not format_string.strip():
        raise ValueError("format_string cannot be empty")

    try:
        return date_obj.strftime(format_string)
    except ValueError as e:
        raise ValueError(f"Invalid format string: {e}")
