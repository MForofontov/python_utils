"""Get the week number of the year."""

from datetime import datetime, date


def get_week_number(date_obj: datetime | date) -> int:
    """
    Get the ISO week number of the year for a given date.

    Args:
        date_obj: The date object to get week number for

    Returns:
        Week number (1-53)

    Raises:
        TypeError: If date_obj is not a datetime or date object
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")

    # Convert to date for calculation
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()

    # Get ISO week number
    return date_obj.isocalendar()[1]
