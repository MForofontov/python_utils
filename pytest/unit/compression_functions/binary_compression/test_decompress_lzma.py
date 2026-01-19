import lzma

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.compression]
from compression_functions.binary_compression.decompress_lzma import decompress_lzma


def test_decompress_lzma_basic() -> None:
    """
    Test case 1: Test the decompress_lzma function with basic input.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = lzma.compress(data)
    decompressed_data: bytes = decompress_lzma(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_lzma_empty() -> None:
    """
    Test case 2: Test the decompress_lzma function with empty byte string.
    """
    data: bytes = b""
    compressed_data: bytes = lzma.compress(data)
    decompressed_data: bytes = decompress_lzma(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_lzma_large_data() -> None:
    """
    Test case 3: Test the decompress_lzma function with large data.
    """
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressed_data: bytes = lzma.compress(data)
    decompressed_data: bytes = decompress_lzma(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_lzma_special_characters() -> None:
    """
    Test case 4: Test the decompress_lzma function with special characters.
    """
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressed_data: bytes = lzma.compress(data)
    decompressed_data: bytes = decompress_lzma(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_lzma_binary_data() -> None:
    """
    Test case 5: Test the decompress_lzma function with binary data.
    """
    data: bytes = bytes(range(256))
    compressed_data: bytes = lzma.compress(data)
    decompressed_data: bytes = decompress_lzma(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_lzma_small_data() -> None:
    """
    Test case 6: Test the decompress_lzma function with very small data.
    """
    data: bytes = b"a"
    compressed_data: bytes = lzma.compress(data)
    decompressed_data: bytes = decompress_lzma(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_lzma_unicode_data() -> None:
    """
    Test case 7: Test the decompress_lzma function with Unicode data.
    """
    data: bytes = "你好，世界".encode()
    compressed_data: bytes = lzma.compress(data)
    decompressed_data: bytes = decompress_lzma(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_lzma_invalid_type() -> None:
    """
    Test case 8: Test the decompress_lzma function with invalid data type.
    """
    with pytest.raises(TypeError):
        decompress_lzma("not bytes")  # type: ignore


def test_decompress_lzma_decompression_error() -> None:
    """
    Test case 9: Test the decompress_lzma function handling of decompression errors.
    """
    with pytest.raises(ValueError):
        # Provide invalid compressed data
        invalid_compressed_data: bytes = b"invalid compressed data"
        decompress_lzma(invalid_compressed_data)
