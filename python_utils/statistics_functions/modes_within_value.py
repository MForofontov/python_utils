def modes_within_value(mode1: int | float, mode2: int | float, value: int | float) -> bool:
    """
    Check if the absolute difference between two modes is within a specified relative value.

    Parameters
    ----------
    mode1 : float
        The first mode value.
    mode2 : float
        The second mode value.
    value : float
        Non-negative fraction representing the tolerance.

    Returns
    -------
    bool
        True if the absolute difference between ``mode1`` and ``mode2`` is less than
        or equal to ``value`` times the maximum of their absolute values, False otherwise.

    Raises
    ------
    TypeError
        If ``mode1``, ``mode2``, or ``value`` are not numeric types.
    ValueError
        If ``value`` is negative.

    Examples
    --------
    >>> modes_within_value(10, 12, 0.2)
    True
    >>> modes_within_value(10, 15, 0.2)
    False
    >>> modes_within_value(-10, -12, 0.2)
    True
    """
    # Validate input types
    if not all(isinstance(x, (int, float)) for x in (mode1, mode2, value)):
        raise TypeError("mode1, mode2, and value must be numeric types.")

    # Ensure the tolerance value is non-negative
    if value < 0:
        raise ValueError("value must be non-negative.")

    # Calculate the absolute difference and allowable threshold
    difference = abs(mode1 - mode2)
    threshold = value * max(abs(mode1), abs(mode2))

    # Determine if the difference is within the allowable threshold
    return difference <= threshold


__all__ = ['modes_within_value']
