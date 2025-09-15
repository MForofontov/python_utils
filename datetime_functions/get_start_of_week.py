"""Get the start of week for a given date."""

from datetime import datetime, date, timedelta


def get_start_of_week(
    date_obj: datetime | date, start_of_week: int = 0
) -> datetime | date:
    """
    Get the first day of the week for a given date.

    Args:
        date_obj: The date object to get start of week for
        start_of_week: Day of week that starts the week (0=Monday, 6=Sunday)

    Returns:
        Date object representing the first day of the week

    Raises:
        TypeError: If date_obj is not a datetime or date object
        ValueError: If start_of_week is not between 0 and 6
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")

    if not isinstance(start_of_week, int) or start_of_week < 0 or start_of_week > 6:
        raise ValueError("start_of_week must be an integer between 0 and 6")

    # Calculate days to subtract to reach start of week
    current_weekday = date_obj.weekday()  # 0=Monday, 6=Sunday

    if current_weekday >= start_of_week:
        days_to_subtract = current_weekday - start_of_week
    else:
        days_to_subtract = current_weekday + (7 - start_of_week)

    if isinstance(date_obj, datetime):
        return date_obj - timedelta(days=days_to_subtract)
    else:
        return date_obj - timedelta(days=days_to_subtract)
