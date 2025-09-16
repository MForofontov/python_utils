"""Check if a date is today."""

from datetime import date, datetime


def is_today(date_obj: datetime | date) -> bool:
    """
    Check if a given date is today.

    Args:
        date_obj: The date object to check

    Returns:
        True if the date is today, False otherwise

    Raises:
        TypeError: If date_obj is not a datetime or date object
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")

    # Convert to date for comparison
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()

    return date_obj == date.today()
