"""Compare two datetime objects."""

from datetime import datetime


def compare_dates(date1: datetime, date2: datetime) -> int:
    """
    Compare two datetime objects.

    Parameters
    ----------
    date1 : datetime
        First datetime to compare.
    date2 : datetime
        Second datetime to compare.

    Returns
    -------
    int
        -1 if date1 < date2, 0 if equal, 1 if date1 > date2

    Raises
    ------
    TypeError
        If either argument is not a ``datetime`` instance.

    Examples
    --------
    >>> from datetime import datetime
    >>> compare_dates(datetime(2020, 1, 1), datetime(2020, 1, 2))
    -1
    >>> compare_dates(datetime(2020, 1, 2), datetime(2020, 1, 2))
    0
    >>> compare_dates(datetime(2020, 1, 3), datetime(2020, 1, 2))
    1
    """
    if not isinstance(date1, datetime):
        raise TypeError(f"date1 must be a datetime, got {type(date1).__name__}")
    if not isinstance(date2, datetime):
        raise TypeError(f"date2 must be a datetime, got {type(date2).__name__}")
    if date1 < date2:
        return -1
    elif date1 > date2:
        return 1
    return 0
