import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from file_functions import get_temp_dir_info


def test_get_temp_dir_info_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation returns valid info dictionary.
    """
    with tempfile.TemporaryDirectory() as controlled_temp:
        with patch("tempfile.gettempdir", return_value=controlled_temp):
            info = get_temp_dir_info()

            # Assert
            assert isinstance(info, dict)
            assert "path" in info
            assert "exists" in info
            assert "writable" in info
            assert "total_files" in info
            assert "total_size_bytes" in info
            assert "available_space_bytes" in info

            # Check types
            assert isinstance(info["path"], str)
            assert isinstance(info["exists"], bool)
            assert isinstance(info["writable"], bool)
            assert isinstance(info["total_files"], int)
            assert isinstance(info["total_size_bytes"], int)
            assert isinstance(info["available_space_bytes"], int)


def test_get_temp_dir_info_case_2_temp_directory_exists() -> None:
    """
    Test case 2: System temp directory should exist and be writable.
    """
    with tempfile.TemporaryDirectory() as controlled_temp:
        with patch("tempfile.gettempdir", return_value=controlled_temp):
            info = get_temp_dir_info()

            # Assert
            assert info["exists"] is True
            assert info["writable"] is True
            assert info["total_files"] >= 0
            assert info["total_size_bytes"] >= 0


def test_get_temp_dir_info_case_3_path_matches_system_temp() -> None:
    """
    Test case 3: Path should match system temp directory.
    """
    with tempfile.TemporaryDirectory() as controlled_temp:
        with patch("tempfile.gettempdir", return_value=controlled_temp):
            info = get_temp_dir_info()
            expected_path = controlled_temp

            # Assert
            assert info["path"] == expected_path


def test_get_temp_dir_info_case_4_file_counting() -> None:
    """
    Test case 4: File counting with known files in temp directory.
    """
    # Arrange - Create a controlled temp directory
    with tempfile.TemporaryDirectory() as controlled_temp:
        # Create some test files
        test_files = []
        for i in range(3):
            test_file = Path(controlled_temp) / f"test{i}.txt"
            test_file.write_text(f"content {i}")
            test_files.append(test_file)

        # Mock tempfile.gettempdir to return our controlled directory
        with patch("tempfile.gettempdir", return_value=controlled_temp):
            # Act
            info = get_temp_dir_info()

            # Assert
            assert info["total_files"] == 3
            assert info["total_size_bytes"] > 0


def test_get_temp_dir_info_case_5_nested_files() -> None:
    """
    Test case 5: Counting includes files in subdirectories.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as controlled_temp:
        # Create nested structure
        subdir = Path(controlled_temp) / "subdir"
        subdir.mkdir()

        # Create files at different levels
        (Path(controlled_temp) / "root.txt").write_text("root content")
        (subdir / "nested.txt").write_text("nested content")

        with patch("tempfile.gettempdir", return_value=controlled_temp):
            # Act
            info = get_temp_dir_info()

            # Assert
            assert info["total_files"] == 2


def test_get_temp_dir_info_case_6_empty_directory() -> None:
    """
    Test case 6: Empty temp directory returns zero counts.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as empty_temp:
        with patch("tempfile.gettempdir", return_value=empty_temp):
            # Act
            info = get_temp_dir_info()

            # Assert
            assert info["total_files"] == 0
            assert info["total_size_bytes"] == 0


def test_get_temp_dir_info_case_7_non_existent_directory() -> None:
    """
    Test case 7: Non-existent temp directory handling.
    """
    # Arrange
    non_existent_dir = "/path/that/absolutely/does/not/exist"

    with patch("tempfile.gettempdir", return_value=non_existent_dir):
        # Act
        info = get_temp_dir_info()

        # Assert
        assert info["exists"] is False
        assert info["writable"] is False
        assert info["total_files"] == 0
        assert info["total_size_bytes"] == 0


def test_get_temp_dir_info_case_8_file_access_error_handling() -> None:
    """
    Test case 8: Graceful handling of file access errors.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as controlled_temp:
        # Create a test file
        test_file = Path(controlled_temp) / "test.txt"
        test_file.write_text("test content")

        # Mock stat to raise OSError for some files, and accept *args, **kwargs
        original_stat = Path.stat

        def mock_stat(self, *args, **kwargs):
            if self.name == "test.txt":
                raise OSError("Permission denied")
            return original_stat(self, *args, **kwargs)

        with patch("tempfile.gettempdir", return_value=controlled_temp):
            with patch.object(Path, "stat", mock_stat):
                # Act & Assert
                with pytest.raises(OSError, match="Error accessing temporary directory: Permission denied"):
                    get_temp_dir_info()


def test_get_temp_dir_info_case_9_statvfs_not_available() -> None:
    """
    Test case 9: Handle systems where statvfs is not available.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as controlled_temp:
        with patch("os.statvfs", side_effect=AttributeError("statvfs not available")):
            with patch("tempfile.gettempdir", return_value=controlled_temp):
                # Act
                info = get_temp_dir_info()

                # Assert
                assert info["available_space_bytes"] == 0


def test_get_temp_dir_info_case_10_directory_access_error() -> None:
    """
    Test case 10: OSError handling during directory access.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as controlled_temp:
        # Mock rglob to raise OSError
        with patch("tempfile.gettempdir", return_value=controlled_temp):
                def mock_stat(self, *args, **kwargs):
                    # Act & Assert
                    with pytest.raises(
                        OSError, match="Error accessing temporary directory"
                    ):
                        get_temp_dir_info()
