import bz2

import pytest
from compression_functions.binary_compression.decompress_bz2 import decompress_bz2


def test_decompress_bz2_basic() -> None:
    """
    Test case 1: Test the decompress_bz2 function with basic input.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_bz2_empty() -> None:
    """
    Test case 2: Test the decompress_bz2 function with empty byte string.
    """
    data: bytes = b""
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_bz2_large_data() -> None:
    """
    Test case 3: Test the decompress_bz2 function with large data.
    """
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_bz2_special_characters() -> None:
    """
    Test case 4: Test the decompress_bz2 function with special characters.
    """
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_bz2_binary_data() -> None:
    """
    Test case 5: Test the decompress_bz2 function with binary data.
    """
    data: bytes = bytes(range(256))
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_bz2_small_data() -> None:
    """
    Test case 6: Test the decompress_bz2 function with very small data.
    """
    data: bytes = b"a"
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_bz2_unicode_data() -> None:
    """
    Test case 7: Test the decompress_bz2 function with Unicode data.
    """
    data: bytes = "你好，世界".encode()
    compressed_data: bytes = bz2.compress(data)
    decompressed_data: bytes = decompress_bz2(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_bz2_invalid_type() -> None:
    """
    Test case 8: Test the decompress_bz2 function with invalid data type.
    """
    with pytest.raises(TypeError):
        decompress_bz2("not bytes")  # type: ignore


def test_decompress_bz2_decompression_error() -> None:
    """
    Test case 9: Test the decompress_bz2 function handling of decompression errors.
    """
    with pytest.raises(ValueError):
        # Provide invalid compressed data
        invalid_compressed_data: bytes = b"invalid compressed data"
        decompress_bz2(invalid_compressed_data)
