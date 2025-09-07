"""
Unit tests for calculate_sha1_hash function.
"""

import hashlib
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from file_functions.file_hashing.calculate_sha1_hash import calculate_sha1_hash


def test_calculate_sha1_hash_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation with known content.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write("hello world")
        temp_file_path = temp_file.name
    
    try:
        # Act
        result = calculate_sha1_hash(temp_file_path)
        
        # Assert - Known SHA1 hash of "hello world"
        expected = "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"
        assert result == expected
    finally:
        Path(temp_file_path).unlink()


def test_calculate_sha1_hash_case_2_empty_file() -> None:
    """
    Test case 2: SHA1 hash of empty file.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file_path = temp_file.name
    
    try:
        # Act
        result = calculate_sha1_hash(temp_file_path)
        
        # Assert - Known SHA1 hash of empty string
        expected = "da39a3ee5e6b4b0d3255bfef95601890afd80709"
        assert result == expected
    finally:
        Path(temp_file_path).unlink()


def test_calculate_sha1_hash_case_3_custom_chunk_size() -> None:
    """
    Test case 3: Function works with custom chunk size.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write("test content")
        temp_file_path = temp_file.name
    
    try:
        # Act
        result = calculate_sha1_hash(temp_file_path, chunk_size=4)
        
        # Assert - Should produce same hash regardless of chunk size
        expected = hashlib.sha1("test content".encode()).hexdigest()
        assert result == expected
    finally:
        Path(temp_file_path).unlink()


def test_calculate_sha1_hash_case_4_large_file() -> None:
    """
    Test case 4: Handle large file efficiently.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        large_content = "a" * 10000  # 10KB file
        temp_file.write(large_content)
        temp_file_path = temp_file.name
    
    try:
        # Act
        result = calculate_sha1_hash(temp_file_path, chunk_size=1024)
        
        # Assert
        expected = hashlib.sha1(large_content.encode()).hexdigest()
        assert result == expected
    finally:
        Path(temp_file_path).unlink()


def test_calculate_sha1_hash_case_5_path_object_input() -> None:
    """
    Test case 5: Function works with Path object input.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write("test")
        temp_file_path = Path(temp_file.name)
    
    try:
        # Act
        result = calculate_sha1_hash(temp_file_path)
        
        # Assert
        expected = hashlib.sha1("test".encode()).hexdigest()
        assert result == expected
    finally:
        temp_file_path.unlink()


def test_calculate_sha1_hash_case_6_non_existent_file_error() -> None:
    """
    Test case 6: ValueError for non-existent file.
    """
    # Arrange
    non_existent_file = "/path/that/does/not/exist.txt"
    
    # Act & Assert
    with pytest.raises(ValueError, match="File does not exist"):
        calculate_sha1_hash(non_existent_file)


def test_calculate_sha1_hash_case_7_invalid_type_errors() -> None:
    """
    Test case 7: TypeError for invalid parameter types.
    """
    # Test invalid file_path type
    with pytest.raises(TypeError, match="file_path must be a string or Path"):
        calculate_sha1_hash(123)
    
    # Test invalid chunk_size type
    with pytest.raises(TypeError, match="chunk_size must be an integer"):
        calculate_sha1_hash("/tmp/file.txt", chunk_size="not_int")


def test_calculate_sha1_hash_case_8_directory_path_error() -> None:
    """
    Test case 8: ValueError when path points to directory.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act & Assert
        with pytest.raises(ValueError, match="Path is not a file"):
            calculate_sha1_hash(temp_dir)


def test_calculate_sha1_hash_case_9_invalid_chunk_size_error() -> None:
    """
    Test case 9: ValueError for invalid chunk size.
    """
    # Arrange
    with tempfile.NamedTemporaryFile() as temp_file:
        # Act & Assert
        with pytest.raises(ValueError, match="chunk_size must be positive"):
            calculate_sha1_hash(temp_file.name, chunk_size=0)
        
        with pytest.raises(ValueError, match="chunk_size must be positive"):
            calculate_sha1_hash(temp_file.name, chunk_size=-1)


def test_calculate_sha1_hash_case_10_file_read_error() -> None:
    """
    Test case 10: OSError handling during file reading.
    """
    # Arrange
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(b"test")
        temp_file.flush()
        
        # Mock open to raise OSError
        with patch('builtins.open', side_effect=OSError("Permission denied")):
            # Act & Assert
            with pytest.raises(OSError, match="Error reading file"):
                calculate_sha1_hash(temp_file.name)
