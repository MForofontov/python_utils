"""Get current UTC date and time in ISO format."""

from datetime import datetime
import pytz


def get_current_datetime_iso_utc() -> str:
    """
    Get the current date and time in UTC ISO 8601 format.

    Parameters
    ----------
    None

    Returns
    -------
    str
        Current UTC datetime in ISO 8601 format.

    Raises
    ------
    None

    Examples
    --------
    >>> get_current_datetime_iso_utc()  # doctest: +SKIP
    '2024-01-01T00:00:00.000000+00:00'
    """
    return datetime.now(pytz.UTC).isoformat()


__all__ = ['get_current_datetime_iso_utc']
