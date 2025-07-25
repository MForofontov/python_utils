import zlib
import base64


def decompress_zlib(compressed_data: bytes) -> bytes:
    """
    Decompress a base64-encoded, zlib-compressed string.

    Parameters
    ----------
    compressed_data : bytes
        The compressed and base64-encoded data as bytes.

    Returns
    -------
    bytes
        The decompressed data as bytes.

    Raises
    ------
    TypeError
        If compressed_data is not bytes.
    ValueError
        If an error occurs during decompression.
    """
    # Check if compressed_data is bytes
    if not isinstance(compressed_data, bytes):
        raise TypeError("compressed_data must be bytes")

    try:
        # Decode the base64-encoded data
        compressed: bytes = base64.b64decode(compressed_data)
        # Decompress the data using zlib
        decompressed: bytes = zlib.decompress(compressed)
        return decompressed
    except Exception as e:
        # Raise a ValueError if an error occurs during decompression
        raise ValueError(f"An error occurred during decompression: {e}")
