from datetime import date, datetime


def get_start_of_month(input_date: date | datetime) -> date:
    """
    Get the first day of the month for the given date.
    
    Args:
        input_date: A date or datetime object
        
    Returns:
        date: The first day of the month (day=1) for the given date
        
    Raises:
        TypeError: If input_date is not a date or datetime object
        
    Examples:
        >>> from datetime import date, datetime
        >>> get_start_of_month(date(2023, 6, 15))
        datetime.date(2023, 6, 1)
        >>> get_start_of_month(datetime(2023, 12, 31, 23, 59, 59))
        datetime.date(2023, 12, 1)
    """
    if not isinstance(input_date, (date, datetime)):
        raise TypeError("input_date must be a date or datetime object")
    
    # Extract the date part if it's a datetime
    if isinstance(input_date, datetime):
        input_date = input_date.date()
    
    # Return the first day of the month
    return date(input_date.year, input_date.month, 1)
