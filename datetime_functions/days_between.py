"""Calculate days between two dates."""

from datetime import datetime, date


def days_between(date1: datetime | date, date2: datetime | date) -> int:
    """
    Calculate the number of days between two dates.
    
    Parameters
    ----------
    date1 : datetime or date
        First date.
    date2 : datetime or date
        Second date.
        
    Returns
    -------
    int
        Number of days between the dates (positive if date2 is after date1).
        
    Raises
    ------
    TypeError
        If either date is not a datetime or date object.
        
    Examples
    --------
    >>> from datetime import date
    >>> days_between(date(2023, 12, 25), date(2024, 1, 1))
    7
    >>> days_between(date(2024, 1, 1), date(2023, 12, 25))
    -7
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
