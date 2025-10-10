"""Check if a date is a weekend."""

from datetime import datetime


def is_weekend(date_obj: datetime) -> bool:
    """
    Check if a given datetime is a weekend (Saturday or Sunday).

    Parameters
    ----------
    date_obj : datetime
        The datetime object to check.

    Returns
    -------
    bool
        True if the datetime is a weekend, False otherwise.

    Raises
    ------
    TypeError
        If date_obj is not a datetime object.

    Examples
    --------
    >>> from datetime import datetime
    >>> is_weekend(datetime(2023, 10, 1))
    True
    >>> is_weekend(datetime(2023, 10, 2))
    False

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(date_obj, datetime):
        raise TypeError("date_obj must be a datetime object")
    # weekday() returns 0=Monday, 6=Sunday
    return date_obj.weekday() >= 5
