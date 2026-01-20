"""Calculate the power of a number."""


def power(base: int | float, exponent: int | float) -> int | float:
    """
    Calculate base raised to the power of exponent.

    Parameters
    ----------
    base : int | float
        The base number.
    exponent : int | float
        The exponent.

    Returns
    -------
    int | float
        The result of base^exponent. Returns int if both inputs are int and
        result is a whole number, otherwise returns float.

    Raises
    ------
    TypeError
        If base or exponent is not numeric.

    Examples
    --------
    >>> power(2, 3)
    8
    >>> power(2.5, 2)
    6.25
    >>> power(9, 0.5)
    3.0
    >>> power(10, -1)
    0.1
    """
    if not isinstance(base, (int, float)):
        raise TypeError("base must be numeric (int or float)")

    if not isinstance(exponent, (int, float)):
        raise TypeError("exponent must be numeric (int or float)")

    result = base**exponent

    # Return int if both inputs are int and result is a whole number
    if (
        isinstance(base, int)
        and isinstance(exponent, int)
        and isinstance(result, (int, float))
    ):
        if result == int(result):
            return int(result)

    return result


__all__ = ["power"]
