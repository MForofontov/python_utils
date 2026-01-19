import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.file_functions]
from file_functions import find_files_by_extension


def test_find_files_by_extension_normal_operation() -> None:
    """
    Test case 1: Normal operation with Python files.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        (Path(temp_dir) / "script.py").touch()
        (Path(temp_dir) / "module.py").touch()
        (Path(temp_dir) / "readme.txt").touch()
        (Path(temp_dir) / "subdir").mkdir()
        (Path(temp_dir) / "subdir" / "utils.py").touch()

        # Act
        result = find_files_by_extension(temp_dir, ".py")

        # Assert
        assert len(result) == 3
        py_files = [Path(f).name for f in result]
        assert "script.py" in py_files
        assert "module.py" in py_files
        assert "utils.py" in py_files


def test_find_files_by_extension_extension_without_dot() -> None:
    """
    Test case 2: Extension specified without leading dot.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        (Path(temp_dir) / "file.txt").touch()
        (Path(temp_dir) / "file.py").touch()

        # Act
        result = find_files_by_extension(temp_dir, "txt")

        # Assert
        assert len(result) == 1
        assert Path(result[0]).name == "file.txt"


def test_find_files_by_extension_case_sensitive() -> None:
    """
    Test case 3: Case sensitive search.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        (Path(temp_dir) / "file1.TXT").touch()
        (Path(temp_dir) / "file2.txt").touch()

        # Act - case sensitive
        result_sensitive = find_files_by_extension(
            temp_dir, ".txt", case_sensitive=True
        )
        # Act - case insensitive
        result_insensitive = find_files_by_extension(
            temp_dir, ".txt", case_sensitive=False
        )

        # Assert
        # Only file2.txt should match in case-sensitive mode
        assert len(result_sensitive) == 1
        assert Path(result_sensitive[0]).name == "file2.txt"
        # Both should match in case-insensitive mode
        found_names = {Path(f).name for f in result_insensitive}
        assert found_names == {"file1.TXT", "file2.txt"}


def test_find_files_by_extension_empty_directory() -> None:
    """
    Test case 4: Empty directory returns empty list.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act
        result = find_files_by_extension(temp_dir, ".py")

        # Assert
        assert result == []


def test_find_files_by_extension_path_object_input() -> None:
    """
    Test case 5: Function works with Path object input.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        (temp_path / "test.py").touch()

        # Act
        result = find_files_by_extension(temp_path, ".py")

        # Assert
        assert len(result) == 1
        assert Path(result[0]).name == "test.py"


def test_find_files_by_extension_invalid_directory_error() -> None:
    """
    Test case 6: ValueError for non-existent directory.
    """
    # Arrange
    non_existent_dir = "/path/that/does/not/exist"

    # Act & Assert
    with pytest.raises(ValueError, match="Directory does not exist"):
        find_files_by_extension(non_existent_dir, ".py")


def test_find_files_by_extension_invalid_type_errors() -> None:
    """
    Test case 7: TypeError for invalid parameter types.
    """
    # Test invalid directory type
    with pytest.raises(TypeError, match="directory must be a string or Path"):
        find_files_by_extension(123, ".py")

    # Test invalid extension type
    with pytest.raises(TypeError, match="extension must be a string"):
        find_files_by_extension("/tmp", 123)

    # Test invalid case_sensitive type
    with pytest.raises(TypeError, match="case_sensitive must be a boolean"):
        find_files_by_extension("/tmp", ".py", "not_bool")


def test_find_files_by_extension_empty_extension_error() -> None:
    """
    Test case 8: ValueError for empty extension.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act & Assert
        with pytest.raises(ValueError, match="Extension cannot be empty"):
            find_files_by_extension(temp_dir, "")


def test_find_files_by_extension_file_path_not_directory_error() -> None:
    """
    Test case 9: ValueError when path points to a file, not directory.
    """
    # Arrange
    with tempfile.NamedTemporaryFile() as temp_file:
        # Act & Assert
        with pytest.raises(ValueError, match="Path is not a directory"):
            find_files_by_extension(temp_file.name, ".py")


def test_find_files_by_extension_os_error_handling() -> None:
    """
    Test case 10: OSError handling during directory walk.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        with patch("os.walk", side_effect=OSError("Permission denied")):
            # Act & Assert
            with pytest.raises(OSError, match="Error accessing directory"):
                find_files_by_extension(temp_dir, ".py")
