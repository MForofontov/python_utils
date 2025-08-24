"""Modify weeks on a date or datetime object."""

from datetime import datetime, date, timedelta
from typing import Union


def modify_weeks(date_obj: Union[datetime, date], weeks: int) -> Union[datetime, date]:
    """
    Add or subtract a specified number of weeks from a datetime or date object.
    
    Args:
        date_obj: The datetime or date object to modify
        weeks: Number of weeks to add (positive) or subtract (negative)
        
    Returns:
        New datetime or date object with weeks modified
        
    Raises:
        TypeError: If date_obj is not a datetime or date object
        TypeError: If weeks is not an integer
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")
    
    if not isinstance(weeks, int):
        raise TypeError("weeks must be an integer")
    
    try:
        delta = timedelta(weeks=weeks)
        return date_obj + delta
    except (ValueError, OverflowError) as e:
        raise ValueError(f"Invalid weeks value: {e}")
