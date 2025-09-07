"""
Unit tests for compare_file_hashes function.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from file_functions.file_hashing.compare_file_hashes import compare_file_hashes


def test_compare_file_hashes_case_1_identical_files() -> None:
    """
    Test case 1: Compare identical files returns True.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file1:
        file1.write("identical content")
        file1_path = file1.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file2:
        file2.write("identical content")
        file2_path = file2.name
    
    try:
        # Act
        result = compare_file_hashes(file1_path, file2_path)
        
        # Assert
        assert result is True
    finally:
        Path(file1_path).unlink()
        Path(file2_path).unlink()


def test_compare_file_hashes_case_2_different_files() -> None:
    """
    Test case 2: Compare different files returns False.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file1:
        file1.write("content one")
        file1_path = file1.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file2:
        file2.write("content two")
        file2_path = file2.name
    
    try:
        # Act
        result = compare_file_hashes(file1_path, file2_path)
        
        # Assert
        assert result is False
    finally:
        Path(file1_path).unlink()
        Path(file2_path).unlink()


def test_compare_file_hashes_case_3_sha256_algorithm() -> None:
    """
    Test case 3: Compare files using SHA256 algorithm.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file1:
        file1.write("test content")
        file1_path = file1.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file2:
        file2.write("test content")
        file2_path = file2.name
    
    try:
        # Act
        result = compare_file_hashes(file1_path, file2_path, hash_algorithm="sha256")
        
        # Assert
        assert result is True
    finally:
        Path(file1_path).unlink()
        Path(file2_path).unlink()


def test_compare_file_hashes_case_4_sha1_algorithm() -> None:
    """
    Test case 4: Compare files using SHA1 algorithm.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file1:
        file1.write("test content")
        file1_path = file1.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file2:
        file2.write("test content")
        file2_path = file2.name
    
    try:
        # Act
        result = compare_file_hashes(file1_path, file2_path, hash_algorithm="sha1")
        
        # Assert
        assert result is True
    finally:
        Path(file1_path).unlink()
        Path(file2_path).unlink()


def test_compare_file_hashes_case_5_custom_chunk_size() -> None:
    """
    Test case 5: Compare files with custom chunk size.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file1:
        file1.write("test content")
        file1_path = file1.name
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file2:
        file2.write("test content")
        file2_path = file2.name
    
    try:
        # Act
        result = compare_file_hashes(file1_path, file2_path, chunk_size=4)
        
        # Assert
        assert result is True
    finally:
        Path(file1_path).unlink()
        Path(file2_path).unlink()


def test_compare_file_hashes_case_6_path_objects() -> None:
    """
    Test case 6: Function works with Path object inputs.
    """
    # Arrange
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file1:
        file1.write("test content")
        file1_path = Path(file1.name)
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file2:
        file2.write("test content")
        file2_path = Path(file2.name)
    
    try:
        # Act
        result = compare_file_hashes(file1_path, file2_path)
        
        # Assert
        assert result is True
    finally:
        file1_path.unlink()
        file2_path.unlink()


def test_compare_file_hashes_case_7_invalid_algorithm_error() -> None:
    """
    Test case 7: ValueError for invalid hash algorithm.
    """
    # Arrange
    with tempfile.NamedTemporaryFile() as file1, tempfile.NamedTemporaryFile() as file2:
        # Act & Assert
        with pytest.raises(ValueError, match="hash_algorithm must be one of"):
            compare_file_hashes(file1.name, file2.name, hash_algorithm="invalid")


def test_compare_file_hashes_case_8_invalid_type_errors() -> None:
    """
    Test case 8: TypeError for invalid parameter types.
    """
    # Test invalid file1_path type
    with pytest.raises(TypeError, match="file1_path must be a string or Path"):
        compare_file_hashes(123, "/tmp/file2.txt")
    
    # Test invalid file2_path type
    with pytest.raises(TypeError, match="file2_path must be a string or Path"):
        compare_file_hashes("/tmp/file1.txt", 123)
    
    # Test invalid hash_algorithm type
    with pytest.raises(TypeError, match="hash_algorithm must be a string"):
        compare_file_hashes("/tmp/file1.txt", "/tmp/file2.txt", hash_algorithm=123)
    
    # Test invalid chunk_size type
    with pytest.raises(TypeError, match="chunk_size must be an integer"):
        compare_file_hashes("/tmp/file1.txt", "/tmp/file2.txt", chunk_size="not_int")


def test_compare_file_hashes_case_9_invalid_chunk_size_error() -> None:
    """
    Test case 9: ValueError for invalid chunk size.
    """
    # Arrange
    with tempfile.NamedTemporaryFile() as file1, tempfile.NamedTemporaryFile() as file2:
        # Act & Assert
        with pytest.raises(ValueError, match="chunk_size must be positive"):
            compare_file_hashes(file1.name, file2.name, chunk_size=0)


def test_compare_file_hashes_case_10_file_not_found_propagation() -> None:
    """
    Test case 10: Proper error propagation when files don't exist.
    """
    # Arrange
    non_existent_file1 = "/path/that/does/not/exist1.txt"
    non_existent_file2 = "/path/that/does/not/exist2.txt"
    
    # Act & Assert
    with pytest.raises(ValueError, match="File does not exist"):
        compare_file_hashes(non_existent_file1, non_existent_file2)
