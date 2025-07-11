import pytest
import gzip
from compression_functions.binary_compression.compress_gzip import compress_gzip

def test_compress_gzip_basic() -> None:
    """
    Test the compress_gzip function with basic input.
    """
    # Test case 1: Basic compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_gzip(data)
    expected_compressed_data: bytes = gzip.compress(data)
    assert compressed_data == expected_compressed_data, "Compressed data should match expected gzip compression"

def test_compress_gzip_empty() -> None:
    """
    Test the compress_gzip function with empty byte string.
    """
    # Test case 2: Empty byte string
    data: bytes = b""
    compressed_data: bytes = compress_gzip(data)
    expected_compressed_data: bytes = gzip.compress(data)
    assert compressed_data == expected_compressed_data, "Compressed data should match expected gzip compression"

def test_compress_gzip_large_data() -> None:
    """
    Test the compress_gzip function with large data.
    """
    # Test case 3: Large data compression
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressed_data: bytes = compress_gzip(data)
    expected_compressed_data: bytes = gzip.compress(data)
    assert compressed_data == expected_compressed_data, "Compressed data should match expected gzip compression"

def test_compress_gzip_special_characters() -> None:
    """
    Test the compress_gzip function with special characters.
    """
    # Test case 4: Special characters
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressed_data: bytes = compress_gzip(data)
    expected_compressed_data: bytes = gzip.compress(data)
    assert compressed_data == expected_compressed_data, "Compressed data should match expected gzip compression"

def test_compress_gzip_binary_data() -> None:
    """
    Test the compress_gzip function with binary data.
    """
    # Test case 5: Binary data
    data: bytes = bytes(range(256))
    compressed_data: bytes = compress_gzip(data)
    expected_compressed_data: bytes = gzip.compress(data)
    assert compressed_data == expected_compressed_data, "Compressed data should match expected gzip compression"

def test_compress_gzip_small_data() -> None:
    """
    Test the compress_gzip function with very small data.
    """
    # Test case 6: Very small data
    data: bytes = b"a"
    compressed_data: bytes = compress_gzip(data)
    expected_compressed_data: bytes = gzip.compress(data)
    assert compressed_data == expected_compressed_data, "Compressed data should match expected gzip compression"

def test_compress_gzip_already_compressed_data() -> None:
    """
    Test the compress_gzip function with already compressed data.
    """
    # Test case 7: Already compressed data
    data: bytes = gzip.compress(b"hello world")
    compressed_data: bytes = compress_gzip(data)
    expected_compressed_data: bytes = gzip.compress(data)
    assert compressed_data == expected_compressed_data, "Compressed data should match expected gzip compression"

def test_compress_gzip_unicode_data() -> None:
    """
    Test the compress_gzip function with Unicode data.
    """
    # Test case 8: Unicode data
    data: bytes = "你好，世界".encode()
    compressed_data: bytes = compress_gzip(data)
    expected_compressed_data: bytes = gzip.compress(data)
    assert compressed_data == expected_compressed_data, "Compressed data should match expected gzip compression"

def test_compress_gzip_invalid_type() -> None:
    """
    Test the compress_gzip function with invalid data type.
    """
    # Test case 9: Invalid data type (non-bytes)
    with pytest.raises(TypeError):
        compress_gzip("not bytes")  # type: ignore

def test_compress_gzip_compression_error() -> None:
    """
    Test the compress_gzip function handling of compression errors.
    """
    # Test case 10: Handling of compression errors
    with pytest.raises(ValueError):
        # Mock gzip.GzipFile to raise an exception
        original_gzipfile = gzip.GzipFile
        gzip.GzipFile = lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Mock error"))  # type: ignore
        try:
            compress_gzip(b"data")
        finally:
            gzip.GzipFile = original_gzipfile
