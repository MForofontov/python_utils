def repeat_strings_in_a_list(string: str, times: int) -> list[str]:
    """
    Creates a list where a given string is repeated a specified number of times.

    Parameters
    ----------
    string : str
        The string to be repeated.
    times : int
        The number of times the string should be repeated.

    Returns
    -------
    list of str
        A list containing the string repeated 'times' times.

    Raises
    ------
    TypeError
        If string is not a string or times is not an integer.
    ValueError
        If times is negative.
    """
    if not isinstance(string, str):
        raise TypeError("string must be a string")
    if not isinstance(times, int):
        raise TypeError("times must be an integer")
    if times < 0:
        raise ValueError("times must be non-negative")

    return [string for _ in range(times)]


__all__ = ["repeat_strings_in_a_list"]
