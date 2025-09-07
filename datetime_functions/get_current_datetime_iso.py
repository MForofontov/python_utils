"""Get current date and time in ISO format."""

from datetime import datetime


def get_current_datetime_iso() -> str:
    """
    Get the current date and time in ISO 8601 format.

    Parameters
    ----------
    None

    Returns
    -------
    str
        Current datetime in ISO 8601 format.

    Raises
    ------
    None

    Examples
    --------
    >>> get_current_datetime_iso()  # doctest: +SKIP
    '2024-01-01T00:00:00.000000'
    """
    return datetime.now().isoformat()


__all__ = ['get_current_datetime_iso']
