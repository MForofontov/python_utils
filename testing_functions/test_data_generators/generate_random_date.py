"""
Generate random date for testing.
"""

import random
from datetime import date, timedelta


def generate_random_date(
    start_year: int = 2000,
    end_year: int = 2025,
) -> date:
    """
    Generate a random date between specified years.

    Parameters
    ----------
    start_year : int, optional
        Starting year (by default 2000).
    end_year : int, optional
        Ending year (by default 2025).

    Returns
    -------
    date
        Random date object.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If start_year > end_year.

    Examples
    --------
    >>> result = generate_random_date(2020, 2021)
    >>> 2020 <= result.year <= 2021
    True
    >>> result = generate_random_date(2000, 2000)
    >>> result.year
    2000

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    if not isinstance(start_year, int):
        raise TypeError(f"start_year must be an integer, got {type(start_year).__name__}")
    if not isinstance(end_year, int):
        raise TypeError(f"end_year must be an integer, got {type(end_year).__name__}")
    
    if start_year > end_year:
        raise ValueError(f"start_year ({start_year}) must be <= end_year ({end_year})")
    
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    
    return start_date + timedelta(days=random_days)


__all__ = ['generate_random_date']
