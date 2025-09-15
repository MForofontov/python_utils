def polyline_encoding_list_of_ints(list_of_ints: list[int]) -> str:
    """
    Encode a list of integers using polyline encoding.

    Parameters
    ----------
    list_of_ints : list[int]
        List of integers to be encoded.

    Returns
    -------
    str
        The encoded polyline string.

    Raises
    ------
    ValueError
        If the input list is empty.

    Examples
    --------
    >>> polyline_encoding_list_of_ints([1, 2])
    'AAA'
    """
    if not list_of_ints:
        raise ValueError("Input list cannot be empty.")

    encoded_text: str = ""
    last_number: int = 0

    for number in list_of_ints:
        delta: int = number - last_number
        last_number = number

        # Encode the delta using the polyline encoding scheme
        delta = ~(delta << 1) if delta < 0 else (delta << 1)
        while delta >= 0x20:
            encoded_text += chr((0x20 | (delta & 0x1F)) + 63)
            delta >>= 5
        encoded_text += chr(delta + 63)

    return encoded_text


__all__ = ["polyline_encoding_list_of_ints"]
