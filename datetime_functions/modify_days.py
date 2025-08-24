"""Modify days on a date or datetime object."""

from datetime import datetime, date, timedelta
from typing import Union


def modify_days(date_obj: Union[datetime, date], days: int) -> Union[datetime, date]:
    """
    Add or subtract a specified number of days from a datetime or date object.
    
    Parameters
    ----------
    date_obj : datetime or date
        The datetime or date object to modify.
    days : int
        Number of days to add (positive) or subtract (negative).
        
    Returns
    -------
    datetime or date
        New datetime or date object with days modified.
        
    Raises
    ------
    TypeError
        If date_obj is not a datetime or date object, or days is not an integer.
    ValueError
        If days value is invalid or causes overflow.
        
    Examples
    --------
    >>> from datetime import date
    >>> modify_days(date(2023, 12, 25), 7)
    datetime.date(2024, 1, 1)
    >>> modify_days(date(2023, 12, 25), -5)
    datetime.date(2023, 12, 20)
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")
    
    if not isinstance(days, int):
        raise TypeError("days must be an integer")
    
    try:
        delta = timedelta(days=days)
        return date_obj + delta
    except (ValueError, OverflowError) as e:
        raise ValueError(f"Invalid days value: {e}")
