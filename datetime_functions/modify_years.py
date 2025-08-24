"""Modify years on a date or datetime object."""

from datetime import datetime, date
from typing import Union


def modify_years(date_obj: Union[datetime, date], years: int) -> Union[datetime, date]:
    """
    Add or subtract a specified number of years from a datetime or date object.
    
    Args:
        date_obj: The datetime or date object to modify
        years: Number of years to add (positive) or subtract (negative)
        
    Returns:
        New datetime or date object with years modified
        
    Raises:
        TypeError: If date_obj is not a datetime or date object
        TypeError: If years is not an integer
        ValueError: If the resulting date would be invalid (e.g., Feb 29 on non-leap year)
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")
    
    if not isinstance(years, int):
        raise TypeError("years must be an integer")
    
    new_year = date_obj.year + years
    
    try:
        if isinstance(date_obj, datetime):
            return date_obj.replace(year=new_year)
        else:
            return date_obj.replace(year=new_year)
    except ValueError:
        # Handle Feb 29 on non-leap year
        if date_obj.month == 2 and date_obj.day == 29:
            if isinstance(date_obj, datetime):
                return date_obj.replace(year=new_year, day=28)
            else:
                return date_obj.replace(year=new_year, day=28)
        else:
            raise
