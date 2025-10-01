"""Get the end of month for a given date."""

from calendar import monthrange
from datetime import date, datetime


def get_end_of_month(date_obj: datetime | date) -> datetime | date:
    """
    Get the last day of the month for a given date.

    Args:
        date_obj: The date object to get end of month for

    Returns:
        Date object representing the last day of the month

    Raises:
        TypeError: If date_obj is not a datetime or date object
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")

    # Get the last day of the month
    last_day = monthrange(date_obj.year, date_obj.month)[1]

    # Return the same type as input
    if isinstance(date_obj, datetime):
        return date_obj.replace(day=last_day)
    else:
        return date(date_obj.year, date_obj.month, last_day)
