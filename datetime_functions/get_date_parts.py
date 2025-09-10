"""Get date parts from a date object."""

from datetime import datetime, date


def get_date_parts(date_obj: datetime | date) -> dict[str, int]:
    """Return key date attributes in a dictionary.

    Parameters
    ----------
    date_obj : datetime | date
        The date object to extract parts from.

    Returns
    -------
    dict[str, int]
        Dictionary containing ``year``, ``month``, ``day``, ``weekday``
        (0=Monday) and ``day_of_year``.

    Raises
    ------
    TypeError
        If ``date_obj`` is not a ``datetime`` or ``date`` instance.
    """
    if not isinstance(date_obj, (datetime, date)):
        raise TypeError("date_obj must be a datetime or date object")

    # Convert datetime to date if needed
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()

    return {
        "year": date_obj.year,
        "month": date_obj.month,
        "day": date_obj.day,
        "weekday": date_obj.weekday(),
        "day_of_year": date_obj.timetuple().tm_yday,
    }
