"""Date parsing functionality."""

from datetime import datetime, date
from typing import Union, Optional, List


def parse_date(date_string: str, formats: Optional[List[str]] = None) -> Union[datetime, date]:
    """
    Parse a date string into a datetime or date object.
    
    Args:
        date_string: The date string to parse
        formats: Optional list of date formats to try. If None, uses common formats.
        
    Returns:
        Parsed datetime or date object
        
    Raises:
        TypeError: If date_string is not a string
        ValueError: If date_string cannot be parsed with any format
    """
    if not isinstance(date_string, str):
        raise TypeError("date_string must be a string")
    
    if not date_string.strip():
        raise ValueError("date_string cannot be empty")
    
    # Default formats to try
    if formats is None:
        formats = [
            '%Y-%m-%d',
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d',
            '%Y/%m/%d %H:%M:%S',
            '%m/%d/%Y',
            '%m/%d/%Y %H:%M:%S',
            '%d/%m/%Y',
            '%d/%m/%Y %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%d-%m-%Y',
            '%d-%m-%Y %H:%M:%S',
            '%B %d, %Y',
            '%b %d, %Y',
            '%d %B %Y',
            '%d %b %Y',
        ]
    
    date_string = date_string.strip()
    
    # Try each format
    for fmt in formats:
        try:
            parsed = datetime.strptime(date_string, fmt)
            # If format contains time components, return datetime
            if any(component in fmt for component in ['%H', '%M', '%S', '%f']):
                return parsed
            else:
                # Return date object for date-only formats
                return parsed.date()
        except ValueError:
            continue
    
    # If none of the formats worked, raise an error
    raise ValueError(f"Unable to parse date string '{date_string}' with any of the provided formats")
