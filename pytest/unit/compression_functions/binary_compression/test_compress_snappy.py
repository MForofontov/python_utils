import pytest
import snappy
from compression_functions.binary_compression.compress_snappy import compress_snappy


def test_compress_snappy_basic() -> None:
    """
    Test case 1: Test the compress_snappy function with basic input.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_snappy(data)
    expected_compressed_data: bytes = snappy.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected snappy compression"


def test_compress_snappy_empty() -> None:
    """
    Test case 2: Test the compress_snappy function with empty byte string.
    """
    data: bytes = b""
    compressed_data: bytes = compress_snappy(data)
    expected_compressed_data: bytes = snappy.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected snappy compression"


def test_compress_snappy_large_data() -> None:
    """
    Test case 3: Test the compress_snappy function with large data.
    """
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressed_data: bytes = compress_snappy(data)
    expected_compressed_data: bytes = snappy.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected snappy compression"


def test_compress_snappy_special_characters() -> None:
    """
    Test case 4: Test the compress_snappy function with special characters.
    """
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressed_data: bytes = compress_snappy(data)
    expected_compressed_data: bytes = snappy.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected snappy compression"


def test_compress_snappy_binary_data() -> None:
    """
    Test case 5: Test the compress_snappy function with binary data.
    """
    data: bytes = bytes(range(256))
    compressed_data: bytes = compress_snappy(data)
    expected_compressed_data: bytes = snappy.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected snappy compression"


def test_compress_snappy_small_data() -> None:
    """
    Test case 6: Test the compress_snappy function with very small data.
    """
    data: bytes = b"a"
    compressed_data: bytes = compress_snappy(data)
    expected_compressed_data: bytes = snappy.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected snappy compression"


def test_compress_snappy_already_compressed_data() -> None:
    """
    Test case 7: Test the compress_snappy function with already compressed data.
    """
    data: bytes = snappy.compress(b"hello world")
    compressed_data: bytes = compress_snappy(data)
    expected_compressed_data: bytes = snappy.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected snappy compression"


def test_compress_snappy_unicode_data() -> None:
    """
    Test case 8: Test the compress_snappy function with Unicode data.
    """
    data: bytes = "你好，世界".encode()
    compressed_data: bytes = compress_snappy(data)
    expected_compressed_data: bytes = snappy.compress(data)
    assert (
        compressed_data == expected_compressed_data
    ), "Compressed data should match expected snappy compression"


def test_compress_snappy_invalid_type() -> None:
    """
    Test case 9: Test the compress_snappy function with invalid data type.
    """
    with pytest.raises(TypeError):
        compress_snappy("not bytes")  # type: ignore


def test_compress_snappy_compression_error() -> None:
    """
    Test case 10: Test the compress_snappy function handling of compression errors.
    """
    with pytest.raises(ValueError):
        # Mock snappy.compress to raise an exception
        original_compress = snappy.compress
        snappy.compress = lambda x: (_ for _ in ()).throw(Exception("Mock error"))  # type: ignore
        try:
            compress_snappy(b"data")
        finally:
            snappy.compress = original_compress
