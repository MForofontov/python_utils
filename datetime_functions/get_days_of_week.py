"""Get the days of the week."""

from typing import List


def get_days_of_week(short_names: bool = False) -> List[str]:
    """
    Get the days of the week.
    
    Args:
        short_names: If True, return abbreviated names (Mon, Tue, etc.)
                    If False, return full names (Monday, Tuesday, etc.)
        
    Returns:
        List of day names starting with Monday
        
    Raises:
        TypeError: If short_names is not a boolean
    """
    if not isinstance(short_names, bool):
        raise TypeError("short_names must be a boolean")
    
    if short_names:
        return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    else:
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
