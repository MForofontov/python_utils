from pathlib import Path

import pytest
from testing_functions.fixture_factories.create_temp_dir_fixture import (
    create_temp_dir_fixture,
)


def test_create_temp_dir_fixture_empty_directory() -> None:
    """
    Test case 1: Create empty temp directory.
    """
    # Act & Assert
    with create_temp_dir_fixture() as temp_dir:
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        assert list(temp_dir.iterdir()) == []
    
    # After context, directory should be deleted
    assert not temp_dir.exists()


def test_create_temp_dir_fixture_with_single_file() -> None:
    """
    Test case 2: Create temp directory with single file.
    """
    # Arrange
    files = {"test.txt": "content"}
    
    # Act & Assert
    with create_temp_dir_fixture(files) as temp_dir:
        file_path = temp_dir / "test.txt"
        assert file_path.exists()
        assert file_path.read_text() == "content"


def test_create_temp_dir_fixture_with_multiple_files() -> None:
    """
    Test case 3: Create temp directory with multiple files.
    """
    # Arrange
    files = {
        "file1.txt": "content1",
        "file2.txt": "content2",
        "file3.txt": "content3"
    }
    
    # Act & Assert
    with create_temp_dir_fixture(files) as temp_dir:
        assert (temp_dir / "file1.txt").read_text() == "content1"
        assert (temp_dir / "file2.txt").read_text() == "content2"
        assert (temp_dir / "file3.txt").read_text() == "content3"


def test_create_temp_dir_fixture_with_subdirectories() -> None:
    """
    Test case 4: Create temp directory with subdirectories.
    """
    # Arrange
    files = {
        "dir1/file1.txt": "content1",
        "dir2/file2.txt": "content2"
    }
    
    # Act & Assert
    with create_temp_dir_fixture(files) as temp_dir:
        assert (temp_dir / "dir1" / "file1.txt").exists()
        assert (temp_dir / "dir2" / "file2.txt").exists()


def test_create_temp_dir_fixture_directory_cleanup() -> None:
    """
    Test case 5: Verify directory is deleted after context.
    """
    # Arrange
    files = {"test.txt": "content"}
    dir_path = None
    
    # Act
    with create_temp_dir_fixture(files) as temp_dir:
        dir_path = temp_dir
        assert dir_path.exists()
    
    # Assert
    assert not dir_path.exists()


def test_create_temp_dir_fixture_nested_directories() -> None:
    """
    Test case 6: Create temp directory with nested structure.
    """
    # Arrange
    files = {
        "level1/level2/level3/file.txt": "deep content"
    }
    
    # Act & Assert
    with create_temp_dir_fixture(files) as temp_dir:
        file_path = temp_dir / "level1" / "level2" / "level3" / "file.txt"
        assert file_path.exists()
        assert file_path.read_text() == "deep content"


def test_create_temp_dir_fixture_type_error_files() -> None:
    """
    Test case 7: TypeError for invalid files type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="files must be a dict or None"):
        with create_temp_dir_fixture("not a dict"):
            pass
