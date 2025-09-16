"""Get the end of year for a given date."""

from datetime import date, datetime


def get_end_of_year(date_obj: datetime | date) -> datetime | date:
    """
    Get the last day of the year for a given date.

    Args:
        date_obj: The date object to get end of year for

    Returns:
        Date object representing December 31st of the same year

    Raises:
        TypeError: If date_obj is not a datetime or date object
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")

    if isinstance(date_obj, datetime):
        return date_obj.replace(month=12, day=31)
    else:
        return date_obj.replace(month=12, day=31)
