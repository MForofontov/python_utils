"""Date formatting functionality."""

from datetime import datetime, date
from typing import Union


def format_date(date_obj: Union[datetime, date], format_string: str = '%Y-%m-%d') -> str:
    """
    Format a datetime or date object into a string.
    
    Args:
        date_obj: The datetime or date object to format
        format_string: The format string to use (default: '%Y-%m-%d')
        
    Returns:
        Formatted date string
        
    Raises:
        TypeError: If date_obj is not a datetime or date object
        TypeError: If format_string is not a string
        ValueError: If format_string is invalid
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")
    
    if not isinstance(format_string, str):
        raise TypeError("format_string must be a string")
    
    if not format_string.strip():
        raise ValueError("format_string cannot be empty")
    
    try:
        return date_obj.strftime(format_string)
    except ValueError as e:
        raise ValueError(f"Invalid format string: {e}")
