"""Compare two dates."""

from datetime import datetime, date
from typing import Union, Literal


def compare_dates(
    date1: Union[datetime, date], 
    date2: Union[datetime, date]
) -> Literal[-1, 0, 1]:
    """
    Compare two dates.
    
    Args:
        date1: First date to compare
        date2: Second date to compare
        
    Returns:
        -1 if date1 < date2, 0 if date1 == date2, 1 if date1 > date2
        
    Raises:
        TypeError: If either date is not a datetime or date object
    """
    if not isinstance(date1, (datetime, date)):
        raise TypeError("date1 must be a datetime or date object")
    
    if not isinstance(date2, (datetime, date)):
        raise TypeError("date2 must be a datetime or date object")
    
    # Convert to date objects for comparison if needed
    if isinstance(date1, datetime):
        date1 = date1.date()
    if isinstance(date2, datetime):
        date2 = date2.date()
    
    if date1 < date2:
        return -1
    elif date1 > date2:
        return 1
    else:
        return 0
