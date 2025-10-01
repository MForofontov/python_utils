"""Get the start of year for a given date."""


from datetime import datetime


def get_start_of_year(date_obj: datetime) -> datetime:
    """
    Get the first day of the year for a given datetime.

    Parameters
    ----------
    date_obj : datetime
        The datetime object to get start of year for.

    Returns
    -------
    datetime
        Datetime representing January 1st of the same year (time preserved).

    Raises
    ------
    TypeError
        If date_obj is not a datetime object.

    Examples
    --------
    >>> from datetime import datetime
    >>> get_start_of_year(datetime(2023, 5, 10, 12, 0))
    datetime(2023, 1, 1, 12, 0)

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(date_obj, datetime):
        raise TypeError("date_obj must be a datetime object")
    return date_obj.replace(month=1, day=1)
