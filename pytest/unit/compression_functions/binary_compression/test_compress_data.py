import pytest
import bz2
import gzip
import lzma
import snappy
import zstandard as zstd
from compression_functions.binary_compression.compress_data import compress_data


def test_compress_data_gzip() -> None:
    """
    Test the compress_data function with gzip compression.
    """
    # Test case 1: Gzip compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_data(data, algorithm="gzip")
    expected_compressed_data: bytes = gzip.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected gzip compression"


def test_compress_data_bz2() -> None:
    """
    Test the compress_data function with bz2 compression.
    """
    # Test case 2: Bz2 compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_data(data, algorithm="bz2")
    expected_compressed_data: bytes = bz2.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected bz2 compression"


def test_compress_data_lzma() -> None:
    """
    Test the compress_data function with lzma compression.
    """
    # Test case 3: Lzma compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_data(data, algorithm="lzma")
    expected_compressed_data: bytes = lzma.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected lzma compression"


def test_compress_data_snappy() -> None:
    """
    Test the compress_data function with snappy compression.
    """
    # Test case 4: Snappy compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_data(data, algorithm="snappy")
    expected_compressed_data: bytes = snappy.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected snappy compression"


def test_compress_data_zstd() -> None:
    """
    Test the compress_data function with zstd compression.
    """
    # Test case 5: Zstd compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_data(data, algorithm="zstd", level=4)
    compressor = zstd.ZstdCompressor(level=4)
    expected_compressed_data: bytes = compressor.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected zstd compression"


def test_compress_data_invalid_algorithm() -> None:
    """
    Test the compress_data function with an unsupported algorithm.
    """
    # Test case 6: Unsupported algorithm
    data: bytes = b"hello world"
    with pytest.raises(ValueError):
        compress_data(data, algorithm="unsupported")


def test_compress_data_invalid_type() -> None:
    """
    Test the compress_data function with invalid data type.
    """
    # Test case 7: Invalid data type (non-bytes)
    with pytest.raises(TypeError):
        compress_data("not bytes", algorithm="gzip")  # type: ignore


def test_compress_data_invalid_level() -> None:
    """
    Test the compress_data function with invalid compression level.
    """
    # Test case 8: Invalid compression level (non-integer)
    data: bytes = b"hello world"
    with pytest.raises(TypeError):
        compress_data(data, algorithm="zstd", level="not an integer")  # type: ignore
