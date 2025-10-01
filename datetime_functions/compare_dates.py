"""Compare two dates."""

from datetime import date, datetime
from typing import Literal


def compare_dates(
    date1: datetime | date,
    date2: datetime | date,
) -> Literal[-1, 0, 1]:
    """
    Compare two dates.

    Parameters
    ----------
    date1 : datetime | date
        First date to compare.
    date2 : datetime | date
        Second date to compare.

    Returns
    -------
    Literal[-1, 0, 1]
        ``-1`` if ``date1`` is earlier than ``date2``; ``0`` if they are
        equal; ``1`` if ``date1`` is later.

    Raises
    ------
    TypeError
        If either argument is not a ``datetime`` or ``date`` instance.

    Examples
    --------
    >>> compare_dates(date(2020, 1, 1), date(2020, 1, 2))
    -1
    >>> compare_dates(date(2020, 1, 2), date(2020, 1, 2))
    0
    >>> compare_dates(date(2020, 1, 3), date(2020, 1, 2))
    1
    """
    if not isinstance(date1, (datetime, date)):
        raise TypeError("date1 must be a datetime or date object")

    if not isinstance(date2, (datetime, date)):
        raise TypeError("date2 must be a datetime or date object")

    # If either is datetime, compare as datetime (preserve time info)
    if isinstance(date1, datetime) or isinstance(date2, datetime):
        # Convert both to datetime for fair comparison
        dt1 = date1 if isinstance(date1, datetime) else datetime.combine(date1, datetime.min.time())
        dt2 = date2 if isinstance(date2, datetime) else datetime.combine(date2, datetime.min.time())
        if dt1 < dt2:
            return -1
        if dt1 > dt2:
            return 1
        return 0
    # Otherwise, compare as date
    if date1 < date2:
        return -1
    if date1 > date2:
        return 1
    return 0
