import pytest
import bz2
import gzip
import lzma
import snappy
import zstandard as zstd
from compression_functions.binary_compression.compress_data import compress_data


def test_compress_data_gzip() -> None:
    """
    Test case 1: Test the compress_data function with gzip compression.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_data(data, algorithm="gzip")
    expected_compressed_data: bytes = gzip.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected gzip compression"
    )


def test_compress_data_bz2() -> None:
    """
    Test case 2: Test the compress_data function with bz2 compression.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_data(data, algorithm="bz2")
    expected_compressed_data: bytes = bz2.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected bz2 compression"
    )


def test_compress_data_lzma() -> None:
    """
    Test case 3: Test the compress_data function with lzma compression.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_data(data, algorithm="lzma")
    expected_compressed_data: bytes = lzma.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected lzma compression"
    )


def test_compress_data_snappy() -> None:
    """
    Test case 4: Test the compress_data function with snappy compression.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_data(data, algorithm="snappy")
    expected_compressed_data: bytes = snappy.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected snappy compression"
    )


def test_compress_data_zstd() -> None:
    """
    Test case 5: Test the compress_data function with zstd compression.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_data(data, algorithm="zstd", level=4)
    compressor = zstd.ZstdCompressor(level=4)
    expected_compressed_data: bytes = compressor.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected zstd compression"
    )


def test_compress_data_invalid_algorithm() -> None:
    """
    Test case 6: Test the compress_data function with an unsupported algorithm.
    """
    data: bytes = b"hello world"
    with pytest.raises(ValueError):
        compress_data(data, algorithm="unsupported")


def test_compress_data_invalid_type() -> None:
    """
    Test case 7: Test the compress_data function with invalid data type.
    """
    with pytest.raises(TypeError):
        compress_data("not bytes", algorithm="gzip")  # type: ignore


def test_compress_data_invalid_level() -> None:
    """
    Test case 8: Test the compress_data function with invalid compression level.
    """
    data: bytes = b"hello world"
    with pytest.raises(TypeError):
        compress_data(data, algorithm="zstd", level="not an integer")  # type: ignore
