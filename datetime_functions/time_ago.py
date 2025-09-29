"""Human-readable time differences functionality - past dates."""

from datetime import date, datetime


def time_ago(
    past_date: datetime | date, reference_date: datetime | date | None = None
) -> str:
    """
    Get a human-readable description of how long ago a date was.

    Parameters
    ----------
    past_date : datetime or date
        The past date to compare.
    reference_date : datetime or date, optional
        The reference date to compare against (default: now).

    Returns
    -------
    str
        Human-readable time difference string (e.g., "2 hours ago", "3 days ago").

    Raises
    ------
    TypeError
        If past_date is not a datetime or date object.
    ValueError
        If past_date is in the future relative to reference_date.

    Examples
    --------
    >>> from datetime import datetime, timedelta
    >>> past = datetime.now() - timedelta(hours=2)
    >>> time_ago(past)
    '2 hours ago'
    >>> past = datetime.now() - timedelta(days=3)
    >>> time_ago(past)
    '3 days ago'
    """
    if not isinstance(past_date, (datetime, date)):
        raise TypeError("past_date must be a datetime or date object")

    if reference_date is None:
        if isinstance(past_date, datetime):
            reference_date = datetime.now()
            if past_date.tzinfo is not None:
                # If past_date is timezone-aware, make reference_date timezone-aware too
                import pytz

                reference_date = reference_date.replace(tzinfo=pytz.UTC)
                if past_date.tzinfo != pytz.UTC:
                    reference_date = reference_date.astimezone(past_date.tzinfo)
        else:
            reference_date = date.today()

    if not isinstance(reference_date, (datetime, date)):
        raise TypeError("reference_date must be a datetime or date object")

    # Ensure both dates are the same type for comparison
    if type(past_date) != type(reference_date):
        if isinstance(past_date, datetime) and isinstance(reference_date, date):
            reference_date = datetime.combine(reference_date, past_date.time())
            if past_date.tzinfo is not None:
                reference_date = reference_date.replace(tzinfo=past_date.tzinfo)
        elif isinstance(past_date, date) and isinstance(reference_date, datetime):
            past_date = datetime.combine(past_date, reference_date.time())
            if reference_date.tzinfo is not None:
                past_date = past_date.replace(tzinfo=reference_date.tzinfo)

    # Calculate the difference
    if past_date > reference_date:
        raise ValueError("past_date cannot be in the future relative to reference_date")

    diff = reference_date - past_date

    # Handle different time scales
    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now" if seconds < 10 else f"{int(seconds)} seconds ago"

    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)} minute{'s' if int(minutes) != 1 else ''} ago"

    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)} hour{'s' if int(hours) != 1 else ''} ago"

    days = diff.days
    if days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago"

    weeks = days // 7
    if weeks < 4:
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"

    months = days // 30  # Approximate
    if months < 12:
        return f"{months} month{'s' if months != 1 else ''} ago"

    years = days // 365  # Approximate
    return f"{years} year{'s' if years != 1 else ''} ago"
