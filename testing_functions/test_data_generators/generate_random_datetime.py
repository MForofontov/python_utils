"""
Generate random datetime for testing.
"""

import random
from datetime import datetime

from .generate_random_date import generate_random_date


def generate_random_datetime(
    start_year: int = 2000,
    end_year: int = 2025,
) -> datetime:
    """
    Generate a random datetime between specified years.

    Parameters
    ----------
    start_year : int, optional
        Starting year (by default 2000).
    end_year : int, optional
        Ending year (by default 2025).

    Returns
    -------
    datetime
        Random datetime object.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If start_year > end_year.

    Examples
    --------
    >>> result = generate_random_datetime(2020, 2021)
    >>> 2020 <= result.year <= 2021
    True
    >>> result = generate_random_datetime(2000, 2000)
    >>> result.year
    2000

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(start_year, int):
        raise TypeError(
            f"start_year must be an integer, got {type(start_year).__name__}"
        )
    if not isinstance(end_year, int):
        raise TypeError(f"end_year must be an integer, got {type(end_year).__name__}")

    if start_year > end_year:
        raise ValueError(f"start_year ({start_year}) must be <= end_year ({end_year})")

    random_date = generate_random_date(start_year, end_year)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)

    return datetime.combine(random_date, datetime.min.time()).replace(
        hour=random_hour, minute=random_minute, second=random_second
    )


__all__ = ["generate_random_datetime"]
