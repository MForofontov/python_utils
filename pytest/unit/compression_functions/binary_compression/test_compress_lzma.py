import pytest

try:
    import lzma
    from python_utils.compression_functions.binary_compression.compress_lzma import compress_lzma
    SNAPPY_AVAILABLE = True
except ImportError:
    SNAPPY_AVAILABLE = False
    lzma = None  # type: ignore
    compress_lzma = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.compression,
    pytest.mark.skipif(not SNAPPY_AVAILABLE, reason="snappy not installed"),
]


def test_compress_lzma_basic() -> None:
    """
    Test case 1: Test the compress_lzma function with basic input.
    """
    data: bytes = b"hello world"
    compressed_data: bytes = compress_lzma(data)
    expected_compressed_data: bytes = lzma.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected lzma compression"
    )


def test_compress_lzma_empty() -> None:
    """
    Test case 2: Test the compress_lzma function with empty byte string.
    """
    data: bytes = b""
    compressed_data: bytes = compress_lzma(data)
    expected_compressed_data: bytes = lzma.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected lzma compression"
    )


def test_compress_lzma_large_data() -> None:
    """
    Test case 3: Test the compress_lzma function with large data.
    """
    data: bytes = b"a" * 1000000  # 1 MB of data
    compressed_data: bytes = compress_lzma(data)
    expected_compressed_data: bytes = lzma.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected lzma compression"
    )


def test_compress_lzma_special_characters() -> None:
    """
    Test case 4: Test the compress_lzma function with special characters.
    """
    data: bytes = b"!@#$%^&*()_+-=[]{}|;':,.<>/?"
    compressed_data: bytes = compress_lzma(data)
    expected_compressed_data: bytes = lzma.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected lzma compression"
    )


def test_compress_lzma_binary_data() -> None:
    """
    Test case 5: Test the compress_lzma function with binary data.
    """
    data: bytes = bytes(range(256))
    compressed_data: bytes = compress_lzma(data)
    expected_compressed_data: bytes = lzma.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected lzma compression"
    )


def test_compress_lzma_small_data() -> None:
    """
    Test case 6: Test the compress_lzma function with very small data.
    """
    data: bytes = b"a"
    compressed_data: bytes = compress_lzma(data)
    expected_compressed_data: bytes = lzma.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected lzma compression"
    )


def test_compress_lzma_already_compressed_data() -> None:
    """
    Test case 7: Test the compress_lzma function with already compressed data.
    """
    data: bytes = lzma.compress(b"hello world")
    compressed_data: bytes = compress_lzma(data)
    expected_compressed_data: bytes = lzma.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected lzma compression"
    )


def test_compress_lzma_unicode_data() -> None:
    """
    Test case 8: Test the compress_lzma function with Unicode data.
    """
    data: bytes = "你好，世界".encode()
    compressed_data: bytes = compress_lzma(data)
    expected_compressed_data: bytes = lzma.compress(data)
    assert compressed_data == expected_compressed_data, (
        "Compressed data should match expected lzma compression"
    )


def test_compress_lzma_invalid_type() -> None:
    """
    Test case 9: Test the compress_lzma function with invalid data type.
    """
    with pytest.raises(TypeError):
        compress_lzma("not bytes")  # type: ignore


def test_compress_lzma_compression_error() -> None:
    """
    Test case 10: Test the compress_lzma function handling of compression errors.
    """
    with pytest.raises(ValueError):
        # Mock lzma.compress to raise an exception
        original_compress = lzma.compress
        lzma.compress = lambda x: (_ for _ in ()).throw(Exception("Mock error"))  # type: ignore
        try:
            compress_lzma(b"data")
        finally:
            lzma.compress = original_compress
