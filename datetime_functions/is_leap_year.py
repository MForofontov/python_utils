"""Leap year functionality."""


def is_leap_year(year: int) -> bool:
    """
    Check if a given year is a leap year.
    
    A leap year is divisible by 4, except for years divisible by 100,
    unless they are also divisible by 400.
    
    Args:
        year: The year to check
        
    Returns:
        True if the year is a leap year, False otherwise
        
    Raises:
        TypeError: If year is not an integer
    """
    if not isinstance(year, int):
        raise TypeError("year must be an integer")
    
    # A year is a leap year if:
    # - It's divisible by 4 AND
    # - If it's divisible by 100, it must also be divisible by 400
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
