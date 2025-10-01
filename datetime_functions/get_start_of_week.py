"""Get the start of week for a given date."""

from datetime import date, datetime, timedelta


def get_start_of_week(date_obj: datetime, start_of_week: int = 0) -> datetime:
    """
    Get the first day of the week for a given datetime.

    Parameters
    ----------
    date_obj : datetime
        The datetime object to get start of week for.
    start_of_week : int, optional
        Day of week that starts the week (0=Monday, 6=Sunday)

    Returns
    -------
    datetime
        Datetime representing the first day of the week (time preserved).

    Raises
    ------
    TypeError
        If date_obj is not a datetime object.
    ValueError
        If start_of_week is not between 0 and 6.

    Examples
    --------
    >>> from datetime import datetime
    >>> get_start_of_week(datetime(2023, 6, 7, 14, 30, 45))
    datetime(2023, 6, 5, 14, 30, 45)
    """
    if not isinstance(date_obj, datetime):
        raise TypeError(f"date_obj must be a datetime, got {type(date_obj).__name__}")
    if not isinstance(start_of_week, int) or start_of_week < 0 or start_of_week > 6:
        raise ValueError("start_of_week must be an integer between 0 and 6")
    current_weekday = date_obj.weekday()  # 0=Monday, 6=Sunday
    if current_weekday >= start_of_week:
        days_to_subtract = current_weekday - start_of_week
    else:
        days_to_subtract = current_weekday + (7 - start_of_week)
    result_date = date_obj - timedelta(days=days_to_subtract)
    return date_obj.replace(year=result_date.year, month=result_date.month, day=result_date.day)
