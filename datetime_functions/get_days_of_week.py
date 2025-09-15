"""Utilities for retrieving day names."""


def get_days_of_week(short_names: bool = False) -> list[str]:
    """
    Get the days of the week.

    Parameters
    ----------
    short_names : bool, optional
        If ``True``, return abbreviated names (``Mon``, ``Tue``, etc.); if
        ``False``, return full names (``Monday``, ``Tuesday``, etc.).

    Returns
    -------
    list[str]
        List of day names starting with Monday.

    Raises
    ------
    TypeError
        If ``short_names`` is not a boolean.

    Examples
    --------
    >>> get_days_of_week()
    ['Monday', 'Tuesday', 'Wednesday',
     'Thursday', 'Friday', 'Saturday', 'Sunday']
    >>> get_days_of_week(short_names=True)
    ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    """
    if not isinstance(short_names, bool):
        raise TypeError("short_names must be a boolean")

    if short_names:
        return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
