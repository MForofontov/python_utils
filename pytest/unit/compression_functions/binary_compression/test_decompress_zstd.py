import pytest
import zstandard as zstd
from compression_functions.binary_compression.decompress_zstd import decompress_zstd


def test_decompress_zstd_basic() -> None:
    """
    Test the decompress_zstd function with basic input.
    """
    # Test case 1: Basic decompression
    data: bytes = b"hello world"
    compressor = zstd.ZstdCompressor()
    compressed_data: bytes = compressor.compress(data)
    decompressed_data: bytes = decompress_zstd(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_zstd_empty() -> None:
    """
    Test the decompress_zstd function with empty byte string.
    """
    # Test case 2: Empty byte string
    data: bytes = b""
    compressor = zstd.ZstdCompressor()
    compressed_data: bytes = compressor.compress(data)
    decompressed_data: bytes = decompress_zstd(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_zstd_large_data() -> None:
    """
    Test the decompress_zstd function with large data.
    """
    # Test case 3: Large data decompression
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressor = zstd.ZstdCompressor()
    compressed_data: bytes = compressor.compress(data)
    decompressed_data: bytes = decompress_zstd(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_zstd_special_characters() -> None:
    """
    Test the decompress_zstd function with special characters.
    """
    # Test case 4: Special characters
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressor = zstd.ZstdCompressor()
    compressed_data: bytes = compressor.compress(data)
    decompressed_data: bytes = decompress_zstd(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_zstd_binary_data() -> None:
    """
    Test the decompress_zstd function with binary data.
    """
    # Test case 5: Binary data
    data: bytes = bytes(range(256))
    compressor = zstd.ZstdCompressor()
    compressed_data: bytes = compressor.compress(data)
    decompressed_data: bytes = decompress_zstd(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_zstd_small_data() -> None:
    """
    Test the decompress_zstd function with very small data.
    """
    # Test case 6: Very small data
    data: bytes = b"a"
    compressor = zstd.ZstdCompressor()
    compressed_data: bytes = compressor.compress(data)
    decompressed_data: bytes = decompress_zstd(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_zstd_unicode_data() -> None:
    """
    Test the decompress_zstd function with Unicode data.
    """
    # Test case 7: Unicode data
    data: bytes = "你好，世界".encode()
    compressor = zstd.ZstdCompressor()
    compressed_data: bytes = compressor.compress(data)
    decompressed_data: bytes = decompress_zstd(compressed_data)
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_zstd_invalid_type() -> None:
    """
    Test the decompress_zstd function with invalid data type.
    """
    # Test case 8: Invalid data type (non-bytes)
    with pytest.raises(TypeError):
        decompress_zstd("not bytes")  # type: ignore


def test_decompress_zstd_decompression_error() -> None:
    """
    Test the decompress_zstd function handling of decompression errors.
    """
    # Test case 9: Handling of decompression errors
    with pytest.raises(ValueError):
        # Provide invalid compressed data
        invalid_compressed_data: bytes = b"invalid compressed data"
        decompress_zstd(invalid_compressed_data)
