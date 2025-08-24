"""Get current date and time in ISO format."""

from datetime import datetime
import pytz


def get_current_datetime_iso() -> str:
    """
    Get the current date and time in ISO 8601 format.
    
    Returns:
        Current datetime in ISO format string
    """
    return datetime.now().isoformat()


def get_current_datetime_iso_utc() -> str:
    """
    Get the current date and time in UTC ISO 8601 format.
    
    Returns:
        Current UTC datetime in ISO format string
    """
    return datetime.now(pytz.UTC).isoformat()
