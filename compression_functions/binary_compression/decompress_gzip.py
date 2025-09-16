import gzip
import io


def decompress_gzip(compressed_data: bytes) -> bytes:
    """
    Decompress gzip-compressed data.

    Parameters
    ----------
    compressed_data : bytes
        The compressed data as bytes.

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

    Examples
    --------
    >>> from .compress_gzip import compress_gzip
    >>> compressed = compress_gzip(b"data")
    >>> decompress_gzip(compressed)
    b"data"
    """
    # Check if compressed_data is bytes
    if not isinstance(compressed_data, bytes):
        raise TypeError("compressed_data must be bytes")

    try:
        # Create a buffer from the compressed data
        buf = io.BytesIO(compressed_data)
        # Open a gzip file object in read mode
        with gzip.GzipFile(fileobj=buf, mode="rb") as f:
            # Read and return the decompressed data
            return f.read()
    except Exception as exc:
        # Raise a ValueError if an error occurs during decompression
        raise ValueError(
            f"An error occurred during decompression: {exc}"
        ) from exc


__all__ = ["decompress_gzip"]
