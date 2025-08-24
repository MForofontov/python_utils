import gzip
import io


def compress_gzip(data: bytes) -> bytes:
    """
    Compress data using gzip.

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
        # Create a buffer to hold the compressed data
        buffer = io.BytesIO()
        # Open a gzip file object in write mode
        with gzip.GzipFile(fileobj=buffer, mode="wb") as gzip_file:
            # Write the data to the gzip file
            gzip_file.write(data)
        # Return the compressed data
        return buffer.getvalue()
    except Exception as e:
        # Raise a ValueError if an error occurs during compression
        raise ValueError(f"An error occurred during compression: {e}")


__all__ = ['compress_gzip']
