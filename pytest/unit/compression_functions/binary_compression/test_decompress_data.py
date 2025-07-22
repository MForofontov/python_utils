import pytest
from compression_functions.binary_compression.decompress_data import decompress_data
from compression_functions.binary_compression.compress_gzip import compress_gzip
from compression_functions.binary_compression.compress_bz2 import compress_bz2
from compression_functions.binary_compression.compress_lzma import compress_lzma
from compression_functions.binary_compression.compress_snappy import compress_snappy
from compression_functions.binary_compression.compress_zstd import compress_zstd

def test_decompress_data_gzip() -> None:
    """
    Test the decompress_data function with gzip compression.
    """
    # Test case 1: Gzip compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_gzip(data)
    decompressed_data: bytes = decompress_data(compressed_data, algorithm='gzip')
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_data_bz2() -> None:
    """
    Test the decompress_data function with bz2 compression.
    """
    # Test case 2: Bz2 compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_bz2(data)
    decompressed_data: bytes = decompress_data(compressed_data, algorithm='bz2')
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_data_lzma() -> None:
    """
    Test the decompress_data function with lzma compression.
    """
    # Test case 3: Lzma compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_lzma(data)
    decompressed_data: bytes = decompress_data(compressed_data, algorithm='lzma')
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_data_snappy() -> None:
    """
    Test the decompress_data function with snappy compression.
    """
    # Test case 4: Snappy compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_snappy(data)
    decompressed_data: bytes = decompress_data(compressed_data, algorithm='snappy')
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_data_zstd() -> None:
    """
    Test the decompress_data function with zstd compression.
    """
    # Test case 5: Zstd compression
    data: bytes = b"hello world"
    compressed_data: bytes = compress_zstd(data)
    decompressed_data: bytes = decompress_data(compressed_data, algorithm='zstd')
    assert decompressed_data == data, "Decompressed data should match the original data"

def test_decompress_data_invalid_algorithm() -> None:
    """
    Test the decompress_data function with an unsupported algorithm.
    """
    # Test case 6: Unsupported algorithm
    data: bytes = b"hello world"
    compressed_data: bytes = compress_gzip(data)
    with pytest.raises(ValueError):
        decompress_data(compressed_data, algorithm='unsupported')

def test_decompress_data_invalid_type() -> None:
    """
    Test the decompress_data function with invalid data type.
    """
    # Test case 7: Invalid data type (non-bytes)
    with pytest.raises(TypeError):
        decompress_data("not bytes", algorithm='gzip')  # type: ignore

def test_decompress_data_decompression_error() -> None:
    """
    Test the decompress_data function handling of decompression errors.
    """
    # Test case 8: Handling of decompression errors
    with pytest.raises(ValueError):
        # Provide invalid compressed data
        invalid_compressed_data: bytes = b"invalid compressed data"
        decompress_data(invalid_compressed_data, algorithm='gzip')

