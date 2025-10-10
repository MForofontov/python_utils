from datetime import datetime


def days_between(date1: datetime, date2: datetime) -> int:
    """
    Calculate the number of days between two datetimes.

    Parameters
    ----------
    date1 : datetime
        First datetime.
    date2 : datetime
        Second datetime.

    Returns
    -------
    int
        Number of days between the datetimes (positive if date2 is after date1).

    Raises
    ------
    TypeError
        If either argument is not a datetime object.

    Examples
    --------
    >>> from datetime import datetime
    >>> days_between(datetime(2023, 12, 25), datetime(2024, 1, 1))
    7
    >>> days_between(datetime(2024, 1, 1), datetime(2023, 12, 25))
    -7
    """
    if not isinstance(date1, datetime):
        raise TypeError("date1 must be a datetime object")
    if not isinstance(date2, datetime):
        raise TypeError("date2 must be a datetime object")
    diff = date2 - date1
    return diff.days
