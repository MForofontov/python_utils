"""
Unit tests for find_files_by_size function.
"""

import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from file_functions import find_files_by_size


def test_find_files_by_size_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation with size filtering.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create files with different sizes
        small_file = Path(temp_dir) / "small.txt"
        medium_file = Path(temp_dir) / "medium.txt"
        large_file = Path(temp_dir) / "large.txt"
        
        small_file.write_text("a")  # 1 byte
        medium_file.write_text("a" * 100)  # 100 bytes
        large_file.write_text("a" * 1000)  # 1000 bytes
        
        # Act
        result = find_files_by_size(temp_dir, min_size=50, max_size=500)
        
        # Assert
        assert len(result) == 1
        file_path, file_size = result[0]
        assert Path(file_path).name == "medium.txt"
        assert file_size == 100


def test_find_files_by_size_case_2_min_size_only() -> None:
    """
    Test case 2: Filter with minimum size only.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        small_file = Path(temp_dir) / "small.txt"
        large_file = Path(temp_dir) / "large.txt"
        
        small_file.write_text("a")  # 1 byte
        large_file.write_text("a" * 1000)  # 1000 bytes
        
        # Act
        result = find_files_by_size(temp_dir, min_size=500)
        
        # Assert
        assert len(result) == 1
        file_path, file_size = result[0]
        assert Path(file_path).name == "large.txt"
        assert file_size == 1000


def test_find_files_by_size_case_3_max_size_only() -> None:
    """
    Test case 3: Filter with maximum size only.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        small_file = Path(temp_dir) / "small.txt"
        large_file = Path(temp_dir) / "large.txt"
        
        small_file.write_text("a")  # 1 byte
        large_file.write_text("a" * 1000)  # 1000 bytes
        
        # Act
        result = find_files_by_size(temp_dir, max_size=500)
        
        # Assert
        assert len(result) == 1
        file_path, file_size = result[0]
        assert Path(file_path).name == "small.txt"
        assert file_size == 1


def test_find_files_by_size_case_4_empty_directory() -> None:
    """
    Test case 4: Empty directory returns empty list.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act
        result = find_files_by_size(temp_dir)
        
        # Assert
        assert result == []


def test_find_files_by_size_case_5_recursive_search() -> None:
    """
    Test case 5: Recursive search in subdirectories.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create nested structure
        subdir = Path(temp_dir) / "subdir"
        subdir.mkdir()
        
        file1 = Path(temp_dir) / "file1.txt"
        file2 = subdir / "file2.txt"
        
        file1.write_text("a" * 100)  # 100 bytes
        file2.write_text("a" * 200)  # 200 bytes
        
        # Act
        result = find_files_by_size(temp_dir, min_size=50)
        
        # Assert
        assert len(result) == 2
        file_names = [Path(f[0]).name for f in result]
        assert "file1.txt" in file_names
        assert "file2.txt" in file_names


def test_find_files_by_size_case_6_invalid_directory_error() -> None:
    """
    Test case 6: ValueError for non-existent directory.
    """
    # Arrange
    non_existent_dir = "/path/that/does/not/exist"
    
    # Act & Assert
    with pytest.raises(ValueError, match="Directory does not exist"):
        find_files_by_size(non_existent_dir)


def test_find_files_by_size_case_7_invalid_type_errors() -> None:
    """
    Test case 7: TypeError for invalid parameter types.
    """
    # Test invalid directory type
    with pytest.raises(TypeError, match="directory must be a string or Path"):
        find_files_by_size(123)
    
    # Test invalid min_size type
    with pytest.raises(TypeError, match="min_size must be an integer"):
        find_files_by_size("/tmp", min_size="not_int")
    
    # Test invalid max_size type
    with pytest.raises(TypeError, match="max_size must be an integer or None"):
        find_files_by_size("/tmp", max_size="not_int")


def test_find_files_by_size_case_8_invalid_size_values() -> None:
    """
    Test case 8: ValueError for invalid size values.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        
        # Test negative min_size
        with pytest.raises(ValueError, match="min_size must be non-negative"):
            find_files_by_size(temp_dir, min_size=-1)
        
        # Test negative max_size
        with pytest.raises(ValueError, match="max_size must be non-negative"):
            find_files_by_size(temp_dir, max_size=-1)
        
        # Test max_size < min_size
        with pytest.raises(ValueError, match="max_size .* must be >= min_size"):
            find_files_by_size(temp_dir, min_size=100, max_size=50)


def test_find_files_by_size_case_9_path_object_input() -> None:
    """
    Test case 9: Function works with Path object input.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_file = temp_path / "test.txt"
        test_file.write_text("test content")
        
        # Act
        result = find_files_by_size(temp_path)
        
        # Assert
        assert len(result) == 1
        file_path, file_size = result[0]
        assert Path(file_path).name == "test.txt"


def test_find_files_by_size_case_10_file_access_error_handling() -> None:
    """
    Test case 10: Graceful handling of file access errors.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a file
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("test")
        
        # Mock stat to raise OSError for some files
        original_stat = Path.stat
        def mock_stat(self):
            if self.name == "test.txt":
                raise OSError("Permission denied")
            return original_stat(self)
        
        with patch.object(Path, 'stat', mock_stat):
            # Act
            result = find_files_by_size(temp_dir)
            
            # Assert - should skip the problematic file
            assert result == []
