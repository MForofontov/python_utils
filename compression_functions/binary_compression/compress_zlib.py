import base64
import zlib


def compress_zlib(data: bytes) -> bytes:
    """
    Compress data using zlib and encode it with base64.

    Parameters
    ----------
    data : bytes
        The data to be compressed.

    Returns
    -------
    bytes
        The compressed and base64-encoded data as bytes.

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
        # Compress the data using zlib
        compressed: bytes = zlib.compress(data)
        # Encode the compressed data with base64
        encoded: bytes = base64.b64encode(compressed)
        return encoded
    except Exception as exc:
        # Raise a ValueError if an error occurs during compression
        raise ValueError(f"An error occurred during compression: {exc}") from exc


__all__ = ["compress_zlib"]
