"""Get the number of days in a month."""

from datetime import datetime, date
from typing import Union
from calendar import monthrange


def get_days_in_month(date_obj: Union[datetime, date, None] = None, year: int = None, month: int = None) -> int:
    """
    Get the number of days in a month.
    
    Args:
        date_obj: Date object to get month from (optional if year/month provided)
        year: Year (optional if date_obj provided)
        month: Month (optional if date_obj provided)
        
    Returns:
        Number of days in the month
        
    Raises:
        TypeError: If invalid input types
        ValueError: If neither date_obj nor year/month are provided, or if values are invalid
    """
    if date_obj is not None:
        if not isinstance(date_obj, (datetime, date)):
            raise TypeError("date_obj must be a datetime or date object")
        year = date_obj.year
        month = date_obj.month
    elif year is not None and month is not None:
        if not isinstance(year, int) or not isinstance(month, int):
            raise TypeError("year and month must be integers")
        if month < 1 or month > 12:
            raise ValueError("month must be between 1 and 12")
    else:
        raise ValueError("Either date_obj or both year and month must be provided")
    
    return monthrange(year, month)[1]
