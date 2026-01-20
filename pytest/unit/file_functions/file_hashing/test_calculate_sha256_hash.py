import hashlib
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.file_functions]
from pyutils_collection.file_functions import calculate_sha256_hash


def test_calculate_sha256_hash_normal_operation() -> None:
    """
    Test case 1: Normal operation with known content.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write("hello world")
        temp_file_path = temp_file.name

    try:
        # Act
        result = calculate_sha256_hash(temp_file_path)

        # Assert - Known SHA256 hash of "hello world"
        expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
        assert result == expected
    finally:
        Path(temp_file_path).unlink()


def test_calculate_sha256_hash_empty_file() -> None:
    """
    Test case 2: SHA256 hash of empty file.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file_path = temp_file.name

    try:
        # Act
        result = calculate_sha256_hash(temp_file_path)

        # Assert - Known SHA256 hash of empty string
        expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert result == expected
    finally:
        Path(temp_file_path).unlink()


def test_calculate_sha256_hash_custom_chunk_size() -> None:
    """
    Test case 3: Function works with custom chunk size.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write("test content")
        temp_file_path = temp_file.name

    try:
        # Act
        result = calculate_sha256_hash(temp_file_path, chunk_size=4)

        # Assert - Should produce same hash regardless of chunk size
        expected = hashlib.sha256(b"test content").hexdigest()
        assert result == expected
    finally:
        Path(temp_file_path).unlink()


def test_calculate_sha256_hash_large_file() -> None:
    """
    Test case 4: Handle large file efficiently.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        large_content = "a" * 10000  # 10KB file
        temp_file.write(large_content)
        temp_file_path = temp_file.name

    try:
        # Act
        result = calculate_sha256_hash(temp_file_path, chunk_size=1024)

        # Assert
        expected = hashlib.sha256(large_content.encode()).hexdigest()
        assert result == expected
    finally:
        Path(temp_file_path).unlink()


def test_calculate_sha256_hash_path_object_input() -> None:
    """
    Test case 5: Function works with Path object input.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write("test")
        temp_file_path = Path(temp_file.name)

    try:
        # Act
        result = calculate_sha256_hash(temp_file_path)

        # Assert
        expected = hashlib.sha256(b"test").hexdigest()
        assert result == expected
    finally:
        temp_file_path.unlink()


def test_calculate_sha256_hash_non_existent_file_error() -> None:
    """
    Test case 6: ValueError for non-existent file.
    """
    # Arrange
    non_existent_file = "/path/that/does/not/exist.txt"

    # Act & Assert
    with pytest.raises(ValueError, match="File does not exist"):
        calculate_sha256_hash(non_existent_file)


def test_calculate_sha256_hash_invalid_type_errors() -> None:
    """
    Test case 7: TypeError for invalid parameter types.
    """
    # Test invalid file_path type
    with pytest.raises(TypeError, match="file_path must be a string or Path"):
        calculate_sha256_hash(123)

    # Test invalid chunk_size type
    with pytest.raises(TypeError, match="chunk_size must be an integer"):
        calculate_sha256_hash("/tmp/file.txt", chunk_size="not_int")


def test_calculate_sha256_hash_directory_path_error() -> None:
    """
    Test case 8: ValueError when path points to directory.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act & Assert
        with pytest.raises(ValueError, match="Path is not a file"):
            calculate_sha256_hash(temp_dir)


def test_calculate_sha256_hash_invalid_chunk_size_error() -> None:
    """
    Test case 9: ValueError for invalid chunk size.
    """
    # Arrange
    with tempfile.NamedTemporaryFile() as temp_file:
        # Act & Assert
        with pytest.raises(ValueError, match="chunk_size must be positive"):
            calculate_sha256_hash(temp_file.name, chunk_size=0)

        with pytest.raises(ValueError, match="chunk_size must be positive"):
            calculate_sha256_hash(temp_file.name, chunk_size=-1)


def test_calculate_sha256_hash_file_read_error() -> None:
    """
    Test case 10: OSError handling during file reading.
    """
    # Arrange
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(b"test")
        temp_file.flush()

        # Mock open to raise OSError
        with patch("builtins.open", side_effect=OSError("Permission denied")):
            # Act & Assert
            with pytest.raises(OSError, match="Error reading file"):
                calculate_sha256_hash(temp_file.name)
