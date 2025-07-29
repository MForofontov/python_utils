import snappy


def compress_snappy(data: bytes) -> bytes:
    """
    Compress data using Snappy.

    Parameters
    ----------
    data : bytes
        The data to be compressed.

    Returns
    -------
    bytes
        The compressed data as bytes.

    Raises
    ------
    TypeError
        If data is not bytes.
    ValueError
        If an error occurs during compression.
    """
    # Check if data is bytes
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")

    try:
        # Compress the data using Snappy
        compressed: bytes = snappy.compress(data)
        return compressed
    except Exception as e:
        # Raise a ValueError if an error occurs during compression
        raise ValueError(f"An error occurred during compression: {e}")

__all__ = ['compress_snappy']
