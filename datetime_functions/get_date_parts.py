"""Get date parts from a date object."""

from datetime import datetime, date
from typing import Union, NamedTuple


class DateParts(NamedTuple):
    """Named tuple for date parts."""
    year: int
    month: int
    day: int
    weekday: int  # 0=Monday, 6=Sunday
    day_of_year: int


def get_date_parts(date_obj: Union[datetime, date]) -> DateParts:
    """
    Get various parts of a date as a named tuple.
    
    Args:
        date_obj: The date object to extract parts from
        
    Returns:
        DateParts named tuple with year, month, day, weekday, day_of_year
        
    Raises:
        TypeError: If date_obj is not a datetime or date object
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")
    
    # Convert datetime to date if needed
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    return DateParts(
        year=date_obj.year,
        month=date_obj.month,
        day=date_obj.day,
        weekday=date_obj.weekday(),
        day_of_year=date_obj.timetuple().tm_yday
    )
