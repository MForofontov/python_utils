import pytest
import zlib
import base64
from compression_functions.binary_compression.compress_zlib import compress_zlib

def test_compress_zlib_basic() -> None:
    """
    Test the compress_zlib function with basic input.
    """
    # Test case 1: Basic compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_zlib(data)
    expected_compressed_data: bytes = base64.b64encode(zlib.compress(data))
    assert compressed_data == expected_compressed_data, "Compressed data should match expected zlib compression and base64 encoding"

def test_compress_zlib_empty() -> None:
    """
    Test the compress_zlib function with empty byte string.
    """
    # Test case 2: Empty byte string
    data: bytes = b""
    compressed_data: bytes = compress_zlib(data)
    expected_compressed_data: bytes = base64.b64encode(zlib.compress(data))
    assert compressed_data == expected_compressed_data, "Compressed data should match expected zlib compression and base64 encoding"

def test_compress_zlib_large_data() -> None:
    """
    Test the compress_zlib function with large data.
    """
    # Test case 3: Large data compression
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressed_data: bytes = compress_zlib(data)
    expected_compressed_data: bytes = base64.b64encode(zlib.compress(data))
    assert compressed_data == expected_compressed_data, "Compressed data should match expected zlib compression and base64 encoding"

def test_compress_zlib_special_characters() -> None:
    """
    Test the compress_zlib function with special characters.
    """
    # Test case 4: Special characters
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressed_data: bytes = compress_zlib(data)
    expected_compressed_data: bytes = base64.b64encode(zlib.compress(data))
    assert compressed_data == expected_compressed_data, "Compressed data should match expected zlib compression and base64 encoding"

def test_compress_zlib_binary_data() -> None:
    """
    Test the compress_zlib function with binary data.
    """
    # Test case 5: Binary data
    data: bytes = bytes(range(256))
    compressed_data: bytes = compress_zlib(data)
    expected_compressed_data: bytes = base64.b64encode(zlib.compress(data))
    assert compressed_data == expected_compressed_data, "Compressed data should match expected zlib compression and base64 encoding"

def test_compress_zlib_small_data() -> None:
    """
    Test the compress_zlib function with very small data.
    """
    # Test case 6: Very small data
    data: bytes = b"a"
    compressed_data: bytes = compress_zlib(data)
    expected_compressed_data: bytes = base64.b64encode(zlib.compress(data))
    assert compressed_data == expected_compressed_data, "Compressed data should match expected zlib compression and base64 encoding"

def test_compress_zlib_already_compressed_data() -> None:
    """
    Test the compress_zlib function with already compressed data.
    """
    # Test case 7: Already compressed data
    data: bytes = zlib.compress(b"hello world")
    compressed_data: bytes = compress_zlib(data)
    expected_compressed_data: bytes = base64.b64encode(zlib.compress(data))
    assert compressed_data == expected_compressed_data, "Compressed data should match expected zlib compression and base64 encoding"

def test_compress_zlib_unicode_data() -> None:
    """
    Test the compress_zlib function with Unicode data.
    """
    # Test case 8: Unicode data
    data: bytes = "你好，世界".encode()
    compressed_data: bytes = compress_zlib(data)
    expected_compressed_data: bytes = base64.b64encode(zlib.compress(data))
    assert compressed_data == expected_compressed_data, "Compressed data should match expected zlib compression and base64 encoding"

def test_compress_zlib_invalid_type() -> None:
    """
    Test the compress_zlib function with invalid data type.
    """
    # Test case 9: Invalid data type (non-bytes)
    with pytest.raises(TypeError):
        compress_zlib("not bytes")  # type: ignore

def test_compress_zlib_compression_error() -> None:
    """
    Test the compress_zlib function handling of compression errors.
    """
    # Test case 10: Handling of compression errors
    with pytest.raises(ValueError):
        # Mock zlib.compress to raise an exception
        original_compress = zlib.compress
        zlib.compress = lambda x: (_ for _ in ()).throw(Exception("Mock error"))  # type: ignore
        try:
            compress_zlib(b"data")
        finally:
            zlib.compress = original_compress

