from compression_functions.decompress_number import decompress_number


def polyline_decoding_list_of_ints(encoded_text: str) -> list[float]:
    """
    Decode a list of integers compressed with polyline encoding.

    Parameters
    ----------
    encoded_text : str
        String representing a compressed list of numbers.

    Returns
    -------
    List[float]
        List with the decoded numbers.

    Raises
    ------
    ValueError
        If the encoded_text is empty or improperly formatted.
    """
    if not encoded_text:
        raise ValueError("Encoded text cannot be empty.")

    decoded_numbers: list[int] = []
    index: int = 0
    last_number: int = 0

    # Extract precision from the first character
    precision: int = ord(encoded_text[index]) - 63
    index += 1

    while index < len(encoded_text):
        try:
            index, difference = decompress_number(encoded_text, index)
        except Exception as e:
            raise ValueError(f"Error decompressing number at index {index}: {e}")

        last_number += difference
        decoded_numbers.append(last_number)

    # Adjust numbers for precision
    scale_factor: float = 10 ** (-precision)
    return [round(number * scale_factor, precision) for number in decoded_numbers]

__all__ = ['polyline_decoding_list_of_ints']
