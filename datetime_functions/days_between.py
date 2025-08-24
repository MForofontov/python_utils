"""Calculate days between two dates."""

from datetime import datetime, date
from typing import Union


def days_between(date1: Union[datetime, date], date2: Union[datetime, date]) -> int:
    """
    Calculate the number of days between two dates.
    
    Args:
        date1: First date
        date2: Second date
        
    Returns:
        Number of days between the dates (positive if date2 is after date1)
        
    Raises:
        TypeError: If either date is not a datetime or date object
    """
    if not isinstance(date1, (datetime, date)):
        raise TypeError("date1 must be a datetime or date object")
    
    if not isinstance(date2, (datetime, date)):
        raise TypeError("date2 must be a datetime or date object")
    
    # Convert datetime objects to date objects for consistent comparison
    if isinstance(date1, datetime):
        date1 = date1.date()
    if isinstance(date2, datetime):
        date2 = date2.date()
    
    # Calculate the difference
    diff = date2 - date1
    return diff.days
