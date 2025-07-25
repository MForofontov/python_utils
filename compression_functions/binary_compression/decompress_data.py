from .decompress_gzip import decompress_gzip
from .decompress_bz2 import decompress_bz2
from .decompress_lzma import decompress_lzma
from .decompress_snappy import decompress_snappy
from .decompress_zstd import decompress_zstd


def decompress_data(compressed_data: bytes, algorithm: str = "gzip") -> bytes:
    """
    Decompress binary data using the specified algorithm.

    Parameters
    ----------
    compressed_data : bytes
        Compressed binary data.
    algorithm : str, optional
        Compression algorithm to use ('gzip', 'bz2', 'lzma', 'snappy', 'zstd').

    Returns
    -------
    bytes
        Decompressed binary data.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported.
    """
    if not isinstance(compressed_data, bytes):
        raise TypeError("data must be bytes")

    if algorithm == "gzip":
        return decompress_gzip(compressed_data)
    elif algorithm == "bz2":
        return decompress_bz2(compressed_data)
    elif algorithm == "lzma":
        return decompress_lzma(compressed_data)
    elif algorithm == "snappy":
        return decompress_snappy(compressed_data)
    elif algorithm == "zstd":
        return decompress_zstd(compressed_data)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
