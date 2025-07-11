import pytest
import bz2
from compression_functions.binary_compression.decompress_bz2 import decompress_bz2

def test_decompress_bz2_basic() -> None:
    """
    Test the decompress_bz2 function with basic input.
    """
    # Test case 1: Basic decompression
    data: bytes = b"hello world"
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_bz2_empty() -> None:
    """
    Test the decompress_bz2 function with empty byte string.
    """
    # Test case 2: Empty byte string
    data: bytes = b""
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_bz2_large_data() -> None:
    """
    Test the decompress_bz2 function with large data.
    """
    # Test case 3: Large data decompression
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_bz2_special_characters() -> None:
    """
    Test the decompress_bz2 function with special characters.
    """
    # Test case 4: Special characters
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_bz2_binary_data() -> None:
    """
    Test the decompress_bz2 function with binary data.
    """
    # Test case 5: Binary data
    data: bytes = bytes(range(256))
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_bz2_small_data() -> None:
    """
    Test the decompress_bz2 function with very small data.
    """
    # Test case 6: Very small data
    data: bytes = b"a"
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_bz2_unicode_data() -> None:
    """
    Test the decompress_bz2 function with Unicode data.
    """
    # Test case 7: Unicode data
    data: bytes = "你好，世界".encode()
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_bz2_invalid_type() -> None:
    """
    Test the decompress_bz2 function with invalid data type.
    """
    # Test case 8: Invalid data type (non-bytes)
    with pytest.raises(TypeError):
        decompress_bz2("not bytes")  # type: ignore

def test_decompress_bz2_decompression_error() -> None:
    """
    Test the decompress_bz2 function handling of decompression errors.
    """
    # Test case 9: Handling of decompression errors
    with pytest.raises(ValueError):
        # Provide invalid compressed data
        invalid_compressed_data: bytes = b"invalid compressed data"
        decompress_bz2(invalid_compressed_data)
