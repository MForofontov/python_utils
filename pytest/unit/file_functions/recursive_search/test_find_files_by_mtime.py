import os
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.file_functions]
from file_functions import find_files_by_mtime


def test_find_files_by_mtime_newer_than_filter() -> None:
    """
    Test case 1: Filter files newer than specified datetime.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        old_file = Path(temp_dir) / "old.txt"
        new_file = Path(temp_dir) / "new.txt"

        # Create files and set modification times
        old_file.touch()
        new_file.touch()

        # Set old file to 2 days ago
        old_time = time.time() - (2 * 24 * 3600)  # 2 days ago
        os.utime(old_file, (old_time, old_time))

        # Filter criterion
        cutoff = datetime.now() - timedelta(days=1)

        # Act
        result = find_files_by_mtime(temp_dir, newer_than=cutoff)

        # Assert
        assert len(result) == 1
        file_path, _ = result[0]
        assert Path(file_path).name == "new.txt"


def test_find_files_by_mtime_older_than_filter() -> None:
    """
    Test case 2: Filter files older than specified datetime.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        old_file = Path(temp_dir) / "old.txt"
        new_file = Path(temp_dir) / "new.txt"

        # Create files
        old_file.touch()
        new_file.touch()

        # Set old file to 2 days ago
        old_time = time.time() - (2 * 24 * 3600)
        os.utime(old_file, (old_time, old_time))

        # Filter criterion
        cutoff = datetime.now() - timedelta(days=1)

        # Act
        result = find_files_by_mtime(temp_dir, older_than=cutoff)

        # Assert
        assert len(result) == 1
        file_path, _ = result[0]
        assert Path(file_path).name == "old.txt"


def test_find_files_by_mtime_days_old_filter() -> None:
    """
    Test case 3: Filter files modified exactly N days ago.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        target_file = Path(temp_dir) / "target.txt"
        other_file = Path(temp_dir) / "other.txt"

        # Create files
        target_file.touch()
        other_file.touch()

        # Set target file to exactly 1 day ago
        target_time = time.time() - (1 * 24 * 3600)  # 1 day ago
        os.utime(target_file, (target_time, target_time))

        # Act
        result = find_files_by_mtime(temp_dir, days_old=1)

        # Assert
        assert len(result) == 1
        file_path, _ = result[0]
        assert Path(file_path).name == "target.txt"


def test_find_files_by_mtime_combined_filters() -> None:
    """
    Test case 4: Combined newer_than and older_than filters.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        very_old = Path(temp_dir) / "very_old.txt"
        middle = Path(temp_dir) / "middle.txt"
        very_new = Path(temp_dir) / "very_new.txt"

        # Create files with different times
        very_old.touch()
        middle.touch()
        very_new.touch()

        # Set modification times
        very_old_time = time.time() - (5 * 24 * 3600)  # 5 days ago
        middle_time = time.time() - (2 * 24 * 3600)  # 2 days ago

        os.utime(very_old, (very_old_time, very_old_time))
        os.utime(middle, (middle_time, middle_time))

        # Filter criteria
        newer_than = datetime.now() - timedelta(days=3)
        older_than = datetime.now() - timedelta(days=1)

        # Act
        result = find_files_by_mtime(
            temp_dir, newer_than=newer_than, older_than=older_than
        )

        # Assert
        assert len(result) == 1
        file_path, _ = result[0]
        assert Path(file_path).name == "middle.txt"


def test_find_files_by_mtime_file_access_error_handling() -> None:
    """
    Test case 5: Graceful handling of file access errors.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.txt"
        test_file.touch()

        # Mock stat to raise OSError
        original_stat = Path.stat

        def mock_stat(self, *args, **kwargs) -> os.stat_result:
            if self.name == "test.txt":
                raise OSError("Permission denied")
            return original_stat(self, *args, **kwargs)

        with patch.object(Path, "stat", mock_stat):
            # Act
            result = find_files_by_mtime(
                temp_dir, newer_than=datetime.now() - timedelta(days=1)
            )

            # Assert - should skip the problematic file
            assert result == []


def test_find_files_by_mtime_no_criteria_error() -> None:
    """
    Test case 6: ValueError when no time criteria specified.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act & Assert
        with pytest.raises(
            ValueError, match="At least one time criterion must be specified"
        ):
            find_files_by_mtime(temp_dir)


def test_find_files_by_mtime_path_is_file_not_directory() -> None:
    """
    Test case 7: ValueError when path is a file, not a directory.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "test_file.txt"
        file_path.write_text("test")
        cutoff = datetime.now()

        # Act & Assert
        with pytest.raises(ValueError, match="Path is not a directory"):
            find_files_by_mtime(str(file_path), newer_than=cutoff)


def test_find_files_by_mtime_invalid_directory_error() -> None:
    """
    Test case 8: ValueError for non-existent directory.
    """
    # Arrange
    non_existent_dir = "/path/that/does/not/exist"
    cutoff = datetime.now()

    # Act & Assert
    with pytest.raises(ValueError, match="Directory does not exist"):
        find_files_by_mtime(non_existent_dir, newer_than=cutoff)


def test_find_files_by_mtime_invalid_type_errors() -> None:
    """
    Test case 9: TypeError for invalid parameter types.
    """
    cutoff = datetime.now()

    # Test invalid directory type
    with pytest.raises(TypeError, match="directory must be a string or Path"):
        find_files_by_mtime(123, newer_than=cutoff)

    # Test invalid days_old type
    with pytest.raises(TypeError, match="days_old must be an integer or None"):
        find_files_by_mtime("/tmp", days_old="not_int")

    # Test invalid newer_than type
    with pytest.raises(TypeError, match="newer_than must be a datetime or None"):
        find_files_by_mtime("/tmp", newer_than="not_datetime")

    # Test invalid older_than type
    with pytest.raises(TypeError, match="older_than must be a datetime or None"):
        find_files_by_mtime("/tmp", older_than="not_datetime")


def test_find_files_by_mtime_invalid_time_range() -> None:
    """
    Test case 10: ValueError for invalid time range.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        newer_than = datetime.now() - timedelta(days=1)
        older_than = datetime.now() - timedelta(days=2)  # older than newer_than

        # Act & Assert
        with pytest.raises(ValueError, match="newer_than must be before older_than"):
            find_files_by_mtime(temp_dir, newer_than=newer_than, older_than=older_than)


def test_find_files_by_mtime_negative_days_old_error() -> None:
    """
    Test case 11: ValueError for negative days_old.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act & Assert
        with pytest.raises(ValueError, match="days_old must be non-negative"):
            find_files_by_mtime(temp_dir, days_old=-1)
