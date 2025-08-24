"""Compare two dates."""

from datetime import datetime, date
from typing import Union, Literal


def compare_dates(
    date1: Union[datetime, date],
    date2: Union[datetime, date],
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

    # Convert to date objects for comparison if needed
    if isinstance(date1, datetime):
        date1 = date1.date()
    if isinstance(date2, datetime):
        date2 = date2.date()

    if date1 < date2:
        return -1
    if date1 > date2:
        return 1
    return 0
