"""Human-readable time differences functionality - future dates."""

from datetime import datetime, date


def time_until(
    future_date: datetime | date,
    reference_date: datetime | date | None = None
) -> str:
    """
    Get a human-readable description of how long until a future date.
    
    Args:
        future_date: The future date to compare
        reference_date: The reference date to compare against (default: now)
        
    Returns:
        Human-readable time difference string (e.g., "in 2 hours", "in 3 days")
        
    Raises:
        TypeError: If future_date is not a datetime or date object
        ValueError: If future_date is in the past relative to reference_date
    """
    if not isinstance(future_date, (datetime, date)):
        raise TypeError("future_date must be a datetime or date object")
    
    if reference_date is None:
        if isinstance(future_date, datetime):
            reference_date = datetime.now()
            if future_date.tzinfo is not None:
                # If future_date is timezone-aware, make reference_date timezone-aware too
                import pytz
                reference_date = reference_date.replace(tzinfo=pytz.UTC)
                if future_date.tzinfo != pytz.UTC:
                    reference_date = reference_date.astimezone(future_date.tzinfo)
        else:
            reference_date = date.today()
    
    if not isinstance(reference_date, (datetime, date)):
        raise TypeError("reference_date must be a datetime or date object")
    
    # Ensure both dates are the same type for comparison
    if isinstance(future_date, datetime) and isinstance(reference_date, date):
        reference_date = datetime.combine(reference_date, datetime.min.time())
        if future_date.tzinfo is not None:
            reference_date = reference_date.replace(tzinfo=future_date.tzinfo)
    elif isinstance(future_date, date) and isinstance(reference_date, datetime):
        future_date = datetime.combine(future_date, datetime.min.time())
        if reference_date.tzinfo is not None:
            future_date = future_date.replace(tzinfo=reference_date.tzinfo)
    
    # Calculate the difference
    if future_date < reference_date:
        raise ValueError("future_date cannot be in the past relative to reference_date")
    
    diff = future_date - reference_date
    
    # Handle different time scales
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "in a moment" if seconds < 10 else f"in {int(seconds)} seconds"
    
    minutes = seconds / 60
    if minutes < 60:
        return f"in {int(minutes)} minute{'s' if int(minutes) != 1 else ''}"
    
    hours = minutes / 60
    if hours < 24:
        return f"in {int(hours)} hour{'s' if int(hours) != 1 else ''}"
    
    days = diff.days
    if days < 7:
        return f"in {days} day{'s' if days != 1 else ''}"
    
    weeks = days // 7
    if weeks < 4:
        return f"in {weeks} week{'s' if weeks != 1 else ''}"
    
    months = days // 30  # Approximate
    if months < 12:
        return f"in {months} month{'s' if months != 1 else ''}"
    
    years = days // 365  # Approximate
    return f"in {years} year{'s' if years != 1 else ''}"
