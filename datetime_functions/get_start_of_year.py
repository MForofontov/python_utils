"""Get the start of year for a given date."""

from datetime import date, datetime


def get_start_of_year(date_obj: datetime | date) -> datetime | date:
    """
    Get the first day of the year for a given date.

    Args:
        date_obj: The date object to get start of year for

    Returns:
        Date object representing January 1st of the same year

    Raises:
        TypeError: If date_obj is not a datetime or date object
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")

    if isinstance(date_obj, datetime):
        return date_obj.replace(month=1, day=1)
    else:
        return date_obj.replace(month=1, day=1)
