import snappy

import pytest
from compression_functions.binary_compression.decompress_snappy import decompress_snappy


def test_decompress_snappy_basic() -> None:
    """
    Test case 1: Test the decompress_snappy function with basic input.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = snappy.compress(data)
    decompressed_data: bytes = decompress_snappy(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_snappy_empty() -> None:
    """
    Test case 2: Test the decompress_snappy function with empty byte string.
    """
    data: bytes = b""
    compressed_data: bytes = snappy.compress(data)
    decompressed_data: bytes = decompress_snappy(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_snappy_large_data() -> None:
    """
    Test case 3: Test the decompress_snappy function with large data.
    """
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressed_data: bytes = snappy.compress(data)
    decompressed_data: bytes = decompress_snappy(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_snappy_special_characters() -> None:
    """
    Test case 4: Test the decompress_snappy function with special characters.
    """
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressed_data: bytes = snappy.compress(data)
    decompressed_data: bytes = decompress_snappy(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_snappy_binary_data() -> None:
    """
    Test case 5: Test the decompress_snappy function with binary data.
    """
    data: bytes = bytes(range(256))
    compressed_data: bytes = snappy.compress(data)
    decompressed_data: bytes = decompress_snappy(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_snappy_small_data() -> None:
    """
    Test case 6: Test the decompress_snappy function with very small data.
    """
    data: bytes = b"a"
    compressed_data: bytes = snappy.compress(data)
    decompressed_data: bytes = decompress_snappy(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_snappy_unicode_data() -> None:
    """
    Test case 7: Test the decompress_snappy function with Unicode data.
    """
    data: bytes = "你好，世界".encode()
    compressed_data: bytes = snappy.compress(data)
    decompressed_data: bytes = decompress_snappy(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_snappy_invalid_type() -> None:
    """
    Test case 8: Test the decompress_snappy function with invalid data type.
    """
    with pytest.raises(TypeError):
        decompress_snappy("not bytes")  # type: ignore


def test_decompress_snappy_decompression_error() -> None:
    """
    Test case 9: Test the decompress_snappy function handling of decompression errors.
    """
    with pytest.raises(ValueError):
        # Provide invalid compressed data
        invalid_compressed_data: bytes = b"invalid compressed data"
        decompress_snappy(invalid_compressed_data)
