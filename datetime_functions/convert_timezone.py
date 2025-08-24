"""Timezone conversion functionality."""

from datetime import datetime
from typing import Union, Optional
import pytz


def convert_timezone(
    dt: datetime, 
    to_timezone: Union[str, pytz.BaseTzInfo], 
    from_timezone: Optional[Union[str, pytz.BaseTzInfo]] = None
) -> datetime:
    """
    Convert a datetime object from one timezone to another.
    
    Args:
        dt: The datetime object to convert
        to_timezone: Target timezone (string name or pytz timezone object)
        from_timezone: Source timezone (string name or pytz timezone object).
                      If None and dt is naive, assumes UTC.
        
    Returns:
        Datetime object converted to the target timezone
        
    Raises:
        TypeError: If dt is not a datetime object
        ValueError: If timezone names are invalid
    """
    if not isinstance(dt, datetime):
        raise TypeError("dt must be a datetime object")
    
    # Convert timezone strings to pytz objects
    if isinstance(to_timezone, str):
        try:
            to_tz = pytz.timezone(to_timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Unknown timezone: {to_timezone}")
    else:
        to_tz = to_timezone
    
    # Handle source timezone
    if dt.tzinfo is None:
        # Naive datetime
        if from_timezone is None:
            # Assume UTC
            from_tz = pytz.UTC
        elif isinstance(from_timezone, str):
            try:
                from_tz = pytz.timezone(from_timezone)
            except pytz.exceptions.UnknownTimeZoneError:
                raise ValueError(f"Unknown timezone: {from_timezone}")
        else:
            from_tz = from_timezone
        
        # Localize the naive datetime
        dt = from_tz.localize(dt)
    
    # Convert to target timezone
    return dt.astimezone(to_tz)
