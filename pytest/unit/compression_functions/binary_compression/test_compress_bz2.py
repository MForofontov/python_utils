import bz2

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.compression]
from compression_functions.binary_compression.compress_bz2 import compress_bz2


def test_compress_bz2_basic() -> None:
    """
    Test case 1: Test the compress_bz2 function with basic input.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_bz2(data)
    expected_compressed_data: bytes = bz2.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected bz2 compression"
    )


def test_compress_bz2_empty() -> None:
    """
    Test case 2: Test the compress_bz2 function with empty byte string.
    """
    data: bytes = b""
    compressed_data: bytes = compress_bz2(data)
    expected_compressed_data: bytes = bz2.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected bz2 compression"
    )


def test_compress_bz2_large_data() -> None:
    """
    Test case 3: Test the compress_bz2 function with large data.
    """
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressed_data: bytes = compress_bz2(data)
    expected_compressed_data: bytes = bz2.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected bz2 compression"
    )


def test_compress_bz2_special_characters() -> None:
    """
    Test case 4: Test the compress_bz2 function with special characters.
    """
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressed_data: bytes = compress_bz2(data)
    expected_compressed_data: bytes = bz2.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected bz2 compression"
    )


def test_compress_bz2_binary_data() -> None:
    """
    Test case 5: Test the compress_bz2 function with binary data.
    """
    data: bytes = bytes(range(256))
    compressed_data: bytes = compress_bz2(data)
    expected_compressed_data: bytes = bz2.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected bz2 compression"
    )


def test_compress_bz2_small_data() -> None:
    """
    Test case 6: Test the compress_bz2 function with very small data.
    """
    data: bytes = b"a"
    compressed_data: bytes = compress_bz2(data)
    expected_compressed_data: bytes = bz2.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected bz2 compression"
    )


def test_compress_bz2_already_compressed_data() -> None:
    """
    Test case 7: Test the compress_bz2 function with already compressed data.
    """
    data: bytes = bz2.compress(b"hello world")
    compressed_data: bytes = compress_bz2(data)
    expected_compressed_data: bytes = bz2.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected bz2 compression"
    )


def test_compress_bz2_unicode_data() -> None:
    """
    Test case 8: Test the compress_bz2 function with Unicode data.
    """
    data: bytes = "你好，世界".encode()
    compressed_data: bytes = compress_bz2(data)
    expected_compressed_data: bytes = bz2.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected bz2 compression"
    )


def test_compress_bz2_invalid_type() -> None:
    """
    Test case 9: Test the compress_bz2 function with invalid data type.
    """
    with pytest.raises(TypeError):
        compress_bz2("not bytes")  # type: ignore


def test_compress_bz2_compression_error() -> None:
    """
    Test case 10: Test the compress_bz2 function handling of compression errors.
    """
    with pytest.raises(ValueError):
        # Mock bz2.compress to raise an exception
        original_compress = bz2.compress
        bz2.compress = lambda x: (_ for _ in ()).throw(Exception("Mock error"))  # type: ignore
        try:
            compress_bz2(b"data")
        finally:
            bz2.compress = original_compress
