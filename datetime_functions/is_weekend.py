"""Check if a date is a weekend."""

from datetime import date, datetime


def is_weekend(date_obj: datetime | date) -> bool:
    """
    Check if a given date is a weekend (Saturday or Sunday).

    Args:
        date_obj: The date object to check

    Returns:
        True if the date is a weekend, False otherwise

    Raises:
        TypeError: If date_obj is not a datetime or date object
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")

    # Convert to date for comparison
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()

    # weekday() returns 0=Monday, 6=Sunday
    # Weekend is Saturday (5) and Sunday (6)
    weekday = date_obj.weekday()
    return weekday >= 5
