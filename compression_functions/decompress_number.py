def decompress_number(text: str, index: int) -> tuple[int, int]:
    """
    Decompress a number from a polyline-encoded string.

    Parameters
    ----------
    text : str
        The polyline-encoded string.
    index : int
        The current index in the string to start decoding from.

    Returns
    -------
    tuple[int, int]
        Index to start decoding the next number and the number decoded
        in the current function call.

    Raises
    ------
    TypeError
        If text is not a string or index is not an integer.

    Examples
    --------
    >>> decompress_number('?', 0)
    (1, 0)
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(index, int):
        raise TypeError("index must be an integer")

    number: int = 0
    bitwise_shift: int = 0

    while True:
        n: int = ord(text[index]) - 63
        index += 1
        number |= (n & 0x1F) << bitwise_shift
        bitwise_shift += 5
        if n < 0x20:
            break

    return index, (~number >> 1) if (number & 1) else (number >> 1)


__all__ = ["decompress_number"]
