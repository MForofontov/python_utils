"""Get the end of month for a given date."""

from calendar import monthrange
from datetime import datetime


def get_end_of_month(date_obj: datetime) -> datetime:
    """
    Get the last day of the month for a given datetime.

    Parameters
    ----------
    date_obj : datetime
        The datetime object to get end of month for.

    Returns
    -------
    datetime
        Datetime representing the last day of the month (time preserved).

    Raises
    ------
    TypeError
        If date_obj is not a datetime object.

    Examples
    --------
    >>> from datetime import datetime
    >>> get_end_of_month(datetime(2023, 1, 15, 10, 30))
    datetime(2023, 1, 31, 10, 30)
    """
    if not isinstance(date_obj, datetime):
        raise TypeError(f"date_obj must be a datetime, got {type(date_obj).__name__}")
    last_day = monthrange(date_obj.year, date_obj.month)[1]
    return date_obj.replace(day=last_day)
