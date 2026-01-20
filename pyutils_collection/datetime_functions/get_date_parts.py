"""Extract date components (year, month, day)."""

from datetime import datetime


def get_date_parts(date_obj: datetime) -> dict[str, int]:
    """
    Return key date attributes in a dictionary from a datetime object.

    Parameters
    ----------
    date_obj : datetime
        The datetime object to extract parts from.

    Returns
    -------
    dict[str, int]
        Dictionary containing ``year``, ``month``, ``day``, ``weekday``
        (0=Monday) and ``day_of_year``.

    Raises
    ------
    TypeError
        If ``date_obj`` is not a ``datetime`` instance.
    """
    if not isinstance(date_obj, datetime):
        raise TypeError("date_obj must be a datetime object")
    return {
        "year": date_obj.year,
        "month": date_obj.month,
        "day": date_obj.day,
        "weekday": date_obj.weekday(),
        "day_of_year": date_obj.timetuple().tm_yday,
    }
