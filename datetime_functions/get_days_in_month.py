from calendar import monthrange
from datetime import datetime


def get_days_in_month(date_obj: datetime) -> int:
    """
    Get the number of days in the month for a given datetime.

    Parameters
    ----------
    date_obj : datetime
        Datetime object to get month from.

    Returns
    -------
    int
        Number of days in the month.

    Raises
    ------
    TypeError
        If date_obj is not a datetime object.

    Examples
    --------
    >>> from datetime import datetime
    >>> get_days_in_month(datetime(2023, 2, 10))
    28
    >>> get_days_in_month(datetime(2020, 2, 10))
    29

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(date_obj, datetime):
        raise TypeError("date_obj must be a datetime object")
    year = date_obj.year
    month = date_obj.month
    return monthrange(year, month)[1]
