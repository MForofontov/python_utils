"""Get the end of week for a given date."""

from datetime import datetime, date, timedelta
from typing import Union


def get_end_of_week(date_obj: Union[datetime, date], start_of_week: int = 0) -> Union[datetime, date]:
    """
    Get the last day of the week for a given date.
    
    Args:
        date_obj: The date object to get end of week for
        start_of_week: Day of week that starts the week (0=Monday, 6=Sunday)
        
    Returns:
        Date object representing the last day of the week
        
    Raises:
        TypeError: If date_obj is not a datetime or date object
        ValueError: If start_of_week is not between 0 and 6
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")
    
    if not isinstance(start_of_week, int) or start_of_week < 0 or start_of_week > 6:
        raise ValueError("start_of_week must be an integer between 0 and 6")
    
    # Calculate days to add to reach end of week
    current_weekday = date_obj.weekday()  # 0=Monday, 6=Sunday
    end_of_week_day = (start_of_week + 6) % 7  # Last day of week
    
    if current_weekday <= end_of_week_day:
        days_to_add = end_of_week_day - current_weekday
    else:
        days_to_add = 7 - (current_weekday - end_of_week_day)
    
    if isinstance(date_obj, datetime):
        return date_obj + timedelta(days=days_to_add)
    else:
        return date_obj + timedelta(days=days_to_add)
