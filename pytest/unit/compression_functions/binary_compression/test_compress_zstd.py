import pytest
import zstandard as zstd
from compression_functions.binary_compression.compress_zstd import compress_zstd


def test_compress_zstd_basic() -> None:
    """
    Test the compress_zstd function with basic input.
    """
    # Test case 1: Basic compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_zstd(data)
    compressor = zstd.ZstdCompressor(level=3)
    expected_compressed_data: bytes = compressor.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected zstd compression"


def test_compress_zstd_empty() -> None:
    """
    Test the compress_zstd function with empty byte string.
    """
    # Test case 2: Empty byte string
    data: bytes = b""
    compressed_data: bytes = compress_zstd(data)
    compressor = zstd.ZstdCompressor(level=3)
    expected_compressed_data: bytes = compressor.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected zstd compression"


def test_compress_zstd_large_data() -> None:
    """
    Test the compress_zstd function with large data.
    """
    # Test case 3: Large data compression
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressed_data: bytes = compress_zstd(data)
    compressor = zstd.ZstdCompressor(level=3)
    expected_compressed_data: bytes = compressor.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected zstd compression"


def test_compress_zstd_special_characters() -> None:
    """
    Test the compress_zstd function with special characters.
    """
    # Test case 4: Special characters
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressed_data: bytes = compress_zstd(data)
    compressor = zstd.ZstdCompressor(level=3)
    expected_compressed_data: bytes = compressor.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected zstd compression"


def test_compress_zstd_binary_data() -> None:
    """
    Test the compress_zstd function with binary data.
    """
    # Test case 5: Binary data
    data: bytes = bytes(range(256))
    compressed_data: bytes = compress_zstd(data)
    compressor = zstd.ZstdCompressor(level=3)
    expected_compressed_data: bytes = compressor.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected zstd compression"


def test_compress_zstd_small_data() -> None:
    """
    Test the compress_zstd function with very small data.
    """
    # Test case 6: Very small data
    data: bytes = b"a"
    compressed_data: bytes = compress_zstd(data)
    compressor = zstd.ZstdCompressor(level=3)
    expected_compressed_data: bytes = compressor.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected zstd compression"


def test_compress_zstd_already_compressed_data() -> None:
    """
    Test the compress_zstd function with already compressed data.
    """
    # Test case 7: Already compressed data
    compressor = zstd.ZstdCompressor(level=3)
    data: bytes = compressor.compress(b"hello world")
    compressed_data: bytes = compress_zstd(data)
    expected_compressed_data: bytes = compressor.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected zstd compression"


def test_compress_zstd_unicode_data() -> None:
    """
    Test the compress_zstd function with Unicode data.
    """
    # Test case 8: Unicode data
    data: bytes = "你好，世界".encode()
    compressed_data: bytes = compress_zstd(data)
    compressor = zstd.ZstdCompressor(level=3)
    expected_compressed_data: bytes = compressor.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected zstd compression"


def test_compress_zstd_different_level() -> None:
    """
    Test the compress_zstd function with a different compression level.
    """
    # Test case 9: Different compression level
    data: bytes = b"hello world"
    compressed_data: bytes = compress_zstd(data, level=5)
    compressor = zstd.ZstdCompressor(level=5)
    expected_compressed_data: bytes = compressor.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected zstd compression with level 5"


def test_compress_zstd_invalid_type() -> None:
    """
    Test the compress_zstd function with invalid data type.
    """
    # Test case 10: Invalid data type (non-bytes)
    with pytest.raises(TypeError):
        compress_zstd("not bytes")  # type: ignore


def test_compress_zstd_invalid_level() -> None:
    """
    Test the compress_zstd function with invalid compression level.
    """
    # Test case 11: Invalid compression level (non-integer)
    with pytest.raises(TypeError):
        compress_zstd(b"hello world", level="not an integer")  # type: ignore


def test_compress_zstd_compression_error() -> None:
    """
    Test the compress_zstd function handling of compression errors.
    """
    # Test case 12: Handling of compression errors
    with pytest.raises(ValueError):
        # Mock zstd.ZstdCompressor to raise an exception
        original_compressor = zstd.ZstdCompressor
        zstd.ZstdCompressor = lambda *args, **kwargs: (
            _ for _ in ()).throw(Exception("Mock error"))  # type: ignore
        try:
            compress_zstd(b"data")
        finally:
            zstd.ZstdCompressor = original_compressor
