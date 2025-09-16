"""
Unit tests for find_files_by_pattern function.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from file_functions import find_files_by_pattern


def test_find_files_by_pattern_case_1_wildcard_pattern() -> None:
    """
    Test case 1: Normal operation with wildcard pattern.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        (Path(temp_dir) / "test_file.py").touch()
        (Path(temp_dir) / "test_module.py").touch()
        (Path(temp_dir) / "readme.txt").touch()
        (Path(temp_dir) / "subdir").mkdir()
        (Path(temp_dir) / "subdir" / "test_utils.py").touch()

        # Act
        result = find_files_by_pattern(temp_dir, "test_*")

        # Assert
        assert len(result) == 3
        file_names = [Path(f).name for f in result]
        assert "test_file.py" in file_names
        assert "test_module.py" in file_names
        assert "test_utils.py" in file_names


def test_find_files_by_pattern_case_2_question_mark_pattern() -> None:
    """
    Test case 2: Pattern with question mark wildcard.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        (Path(temp_dir) / "file1.txt").touch()
        (Path(temp_dir) / "file2.txt").touch()
        (Path(temp_dir) / "file10.txt").touch()

        # Act
        result = find_files_by_pattern(temp_dir, "file?.txt")

        # Assert
        assert len(result) == 2
        file_names = [Path(f).name for f in result]
        assert "file1.txt" in file_names
        assert "file2.txt" in file_names
        assert "file10.txt" not in file_names


def test_find_files_by_pattern_case_3_case_sensitive() -> None:
    """
    Test case 3: Case sensitive pattern matching.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        (Path(temp_dir) / "Test.txt").touch()
        (Path(temp_dir) / "test.txt").touch()

        # Act - case sensitive
        result_sensitive = find_files_by_pattern(temp_dir, "Test*", case_sensitive=True)
        # Act - case insensitive
        result_insensitive = find_files_by_pattern(
            temp_dir, "Test*", case_sensitive=False
        )

        # Assert
        assert len(result_sensitive) == 1
        assert len(result_insensitive) == 2


def test_find_files_by_pattern_case_4_bracket_pattern() -> None:
    """
    Test case 4: Pattern with character class brackets.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        (Path(temp_dir) / "file1.txt").touch()
        (Path(temp_dir) / "file2.txt").touch()
        (Path(temp_dir) / "file5.txt").touch()
        (Path(temp_dir) / "file9.txt").touch()

        # Act
        result = find_files_by_pattern(temp_dir, "file[1-5].txt")

        # Assert
        assert len(result) == 3
        file_names = [Path(f).name for f in result]
        assert "file1.txt" in file_names
        assert "file2.txt" in file_names
        assert "file5.txt" in file_names
        assert "file9.txt" not in file_names


def test_find_files_by_pattern_case_5_empty_directory() -> None:
    """
    Test case 5: Empty directory returns empty list.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act
        result = find_files_by_pattern(temp_dir, "*")

        # Assert
        assert result == []


def test_find_files_by_pattern_case_6_invalid_directory_error() -> None:
    """
    Test case 6: ValueError for non-existent directory.
    """
    # Arrange
    non_existent_dir = "/path/that/does/not/exist"

    # Act & Assert
    with pytest.raises(ValueError, match="Directory does not exist"):
        find_files_by_pattern(non_existent_dir, "*")


def test_find_files_by_pattern_case_7_invalid_type_errors() -> None:
    """
    Test case 7: TypeError for invalid parameter types.
    """
    # Test invalid directory type
    with pytest.raises(TypeError, match="directory must be a string or Path"):
        find_files_by_pattern(123, "*")

    # Test invalid pattern type
    with pytest.raises(TypeError, match="pattern must be a string"):
        find_files_by_pattern("/tmp", 123)

    # Test invalid case_sensitive type
    with pytest.raises(TypeError, match="case_sensitive must be a boolean"):
        find_files_by_pattern("/tmp", "*", "not_bool")


def test_find_files_by_pattern_case_8_empty_pattern_error() -> None:
    """
    Test case 8: ValueError for empty pattern.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act & Assert
        with pytest.raises(ValueError, match="Pattern cannot be empty"):
            find_files_by_pattern(temp_dir, "")


def test_find_files_by_pattern_case_9_path_object_input() -> None:
    """
    Test case 9: Function works with Path object input.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        (temp_path / "test.py").touch()

        # Act
        result = find_files_by_pattern(temp_path, "*.py")

        # Assert
        assert len(result) == 1
        assert Path(result[0]).name == "test.py"


def test_find_files_by_pattern_case_10_os_error_handling() -> None:
    """
    Test case 10: OSError handling during directory walk.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch("os.walk", side_effect=OSError("Permission denied")):
            # Act & Assert
            with pytest.raises(OSError, match="Error accessing directory"):
                find_files_by_pattern(temp_dir, "*")
