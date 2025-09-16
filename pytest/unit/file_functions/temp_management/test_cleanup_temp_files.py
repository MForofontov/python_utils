"""
Unit tests for cleanup_temp_files function.
"""

import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest
from file_functions import cleanup_temp_files


def test_cleanup_temp_files_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation cleaning old files.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create old file
        old_file = Path(temp_dir) / "old_file.txt"
        old_file.write_text("old content")

        # Set file to be older than 1 hour
        old_time = time.time() - (2 * 3600)  # 2 hours ago
        os.utime(old_file, (old_time, old_time))

        # Create new file
        new_file = Path(temp_dir) / "new_file.txt"
        new_file.write_text("new content")

        # Act
        deleted_files = cleanup_temp_files(temp_dir, max_age_hours=1.0)

        # Assert
        assert len(deleted_files) == 1
        assert str(old_file) in deleted_files
        assert not old_file.exists()
        assert new_file.exists()


def test_cleanup_temp_files_case_2_pattern_filtering() -> None:
    """
    Test case 2: Clean files matching specific pattern.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create files with different extensions
        log_file = Path(temp_dir) / "app.log"
        txt_file = Path(temp_dir) / "document.txt"

        log_file.write_text("log content")
        txt_file.write_text("text content")

        # Set both files to be old
        old_time = time.time() - (2 * 3600)  # 2 hours ago
        os.utime(log_file, (old_time, old_time))
        os.utime(txt_file, (old_time, old_time))

        # Act - clean only .log files
        deleted_files = cleanup_temp_files(temp_dir, max_age_hours=1.0, pattern="*.log")

        # Assert
        assert len(deleted_files) == 1
        assert str(log_file) in deleted_files
        assert not log_file.exists()
        assert txt_file.exists()


def test_cleanup_temp_files_case_3_dry_run() -> None:
    """
    Test case 3: Dry run mode lists files without deleting.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        old_file = Path(temp_dir) / "old_file.txt"
        old_file.write_text("content")

        # Set file to be old
        old_time = time.time() - (2 * 3600)  # 2 hours ago
        os.utime(old_file, (old_time, old_time))

        # Act
        would_delete = cleanup_temp_files(temp_dir, max_age_hours=1.0, dry_run=True)

        # Assert
        assert len(would_delete) == 1
        assert str(old_file) in would_delete
        assert old_file.exists()  # File should still exist


def test_cleanup_temp_files_case_4_default_temp_directory() -> None:
    """
    Test case 4: Use system temp directory when none specified.
    """
    # Act
    deleted_files = cleanup_temp_files(
        max_age_hours=24.0, pattern="non_existent_pattern_xyz", dry_run=True
    )

    # Assert - should not error and return empty list
    assert isinstance(deleted_files, list)


def test_cleanup_temp_files_case_5_empty_directory() -> None:
    """
    Test case 5: Empty directory returns empty list.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act
        deleted_files = cleanup_temp_files(temp_dir, max_age_hours=1.0)

        # Assert
        assert deleted_files == []


def test_cleanup_temp_files_case_6_no_old_files() -> None:
    """
    Test case 6: No files older than threshold.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        new_file = Path(temp_dir) / "new_file.txt"
        new_file.write_text("new content")

        # Act
        deleted_files = cleanup_temp_files(temp_dir, max_age_hours=1.0)

        # Assert
        assert deleted_files == []
        assert new_file.exists()


def test_cleanup_temp_files_case_7_invalid_directory_error() -> None:
    """
    Test case 7: ValueError for non-existent directory.
    """
    # Arrange
    non_existent_dir = "/path/that/does/not/exist"

    # Act & Assert
    with pytest.raises(ValueError, match="Directory does not exist"):
        cleanup_temp_files(non_existent_dir, max_age_hours=1.0)


def test_cleanup_temp_files_case_8_invalid_type_errors() -> None:
    """
    Test case 8: TypeError for invalid parameter types.
    """
    # Test invalid temp_dir type
    with pytest.raises(TypeError, match="temp_dir must be a string, Path, or None"):
        cleanup_temp_files(123, max_age_hours=1.0)

    # Test invalid max_age_hours type
    with pytest.raises(TypeError, match="max_age_hours must be a number"):
        cleanup_temp_files("/tmp", max_age_hours="not_number")

    # Test invalid pattern type
    with pytest.raises(TypeError, match="pattern must be a string"):
        cleanup_temp_files("/tmp", pattern=123)

    # Test invalid dry_run type
    with pytest.raises(TypeError, match="dry_run must be a boolean"):
        cleanup_temp_files("/tmp", dry_run="not_bool")


def test_cleanup_temp_files_case_9_invalid_max_age_hours() -> None:
    """
    Test case 9: ValueError for invalid max_age_hours value.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        # Act & Assert
        with pytest.raises(ValueError, match="max_age_hours must be positive"):
            cleanup_temp_files(temp_dir, max_age_hours=0)

        with pytest.raises(ValueError, match="max_age_hours must be positive"):
            cleanup_temp_files(temp_dir, max_age_hours=-1)


def test_cleanup_temp_files_case_10_file_access_error_handling() -> None:
    """
    Test case 10: Graceful handling of file access errors.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("content")

        # Set file to be old
        old_time = time.time() - (2 * 3600)
        os.utime(test_file, (old_time, old_time))

        # Mock stat to raise OSError for some files
        original_stat = Path.stat

        def mock_stat(self):
            if self.name == "test.txt":
                raise OSError("Permission denied")
            return original_stat(self)

        with patch.object(Path, "stat", mock_stat):
            # Act
            deleted_files = cleanup_temp_files(temp_dir, max_age_hours=1.0)

            # Assert - should skip the problematic file
            assert deleted_files == []
            assert test_file.exists()  # File should still exist
