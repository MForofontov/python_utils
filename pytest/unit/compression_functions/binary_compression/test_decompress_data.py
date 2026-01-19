import pytest

pytestmark = [pytest.mark.unit, pytest.mark.compression]
from python_utils.compression_functions.binary_compression.compress_bz2 import compress_bz2
from python_utils.compression_functions.binary_compression.compress_gzip import compress_gzip
from python_utils.compression_functions.binary_compression.compress_lzma import compress_lzma
from python_utils.compression_functions.binary_compression.compress_snappy import compress_snappy
from python_utils.compression_functions.binary_compression.compress_zstd import compress_zstd
from python_utils.compression_functions.binary_compression.decompress_data import decompress_data


def test_decompress_data_gzip() -> None:
    """
    Test case 1: Test the decompress_data function with gzip compression.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_gzip(data)
    decompressed_data: bytes = decompress_data(compressed_data, algorithm="gzip")
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_data_bz2() -> None:
    """
    Test case 2: Test the decompress_data function with bz2 compression.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_bz2(data)
    decompressed_data: bytes = decompress_data(compressed_data, algorithm="bz2")
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_data_lzma() -> None:
    """
    Test case 3: Test the decompress_data function with lzma compression.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_lzma(data)
    decompressed_data: bytes = decompress_data(compressed_data, algorithm="lzma")
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_data_snappy() -> None:
    """
    Test case 4: Test the decompress_data function with snappy compression.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_snappy(data)
    decompressed_data: bytes = decompress_data(compressed_data, algorithm="snappy")
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_data_zstd() -> None:
    """
    Test case 5: Test the decompress_data function with zstd compression.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_zstd(data)
    decompressed_data: bytes = decompress_data(compressed_data, algorithm="zstd")
    assert decompressed_data == data, "Decompressed data should match the original data"


def test_decompress_data_invalid_algorithm() -> None:
    """
    Test case 6: Test the decompress_data function with an unsupported algorithm.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_gzip(data)
    with pytest.raises(ValueError):
        decompress_data(compressed_data, algorithm="unsupported")


def test_decompress_data_invalid_type() -> None:
    """
    Test case 7: Test the decompress_data function with invalid data type.
    """
    with pytest.raises(TypeError):
        decompress_data("not bytes", algorithm="gzip")  # type: ignore


def test_decompress_data_decompression_error() -> None:
    """
    Test case 8: Test the decompress_data function handling of decompression errors.
    """
    with pytest.raises(ValueError):
        # Provide invalid compressed data
        invalid_compressed_data: bytes = b"invalid compressed data"
        decompress_data(invalid_compressed_data, algorithm="gzip")
