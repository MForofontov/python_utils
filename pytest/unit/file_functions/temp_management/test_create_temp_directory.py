import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.file_functions]
from file_functions import create_temp_directory


def test_create_temp_directory_normal_operation() -> None:
    """
    Test case 1: Normal operation with default parameters.
    """
    # Act
    with create_temp_directory() as temp_dir:
        # Assert
        assert isinstance(temp_dir, str)
        assert Path(temp_dir).exists()
        assert Path(temp_dir).is_dir()

        # Create file in directory
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("test content")
        assert test_file.exists()

    # Assert directory is deleted after context
    assert not Path(temp_dir).exists()


def test_create_temp_directory_custom_suffix() -> None:
    """
    Test case 2: Create temp directory with custom suffix.
    """
    # Act
    with create_temp_directory(suffix="_test") as temp_dir:
        # Assert
        dir_name = Path(temp_dir).name
        assert dir_name.endswith("_test")
        assert Path(temp_dir).exists()


def test_create_temp_directory_custom_prefix() -> None:
    """
    Test case 3: Create temp directory with custom prefix.
    """
    # Act
    with create_temp_directory(prefix="mytest_") as temp_dir:
        # Assert
        dir_name = Path(temp_dir).name
        assert dir_name.startswith("mytest_")
        assert Path(temp_dir).exists()


def test_create_temp_directory_custom_parent_directory() -> None:
    """
    Test case 4: Create temp directory in custom parent directory.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as parent_dir:
        # Act
        with create_temp_directory(dir=parent_dir) as temp_dir:
            # Assert
            assert Path(temp_dir).parent == Path(parent_dir)
            assert Path(temp_dir).exists()


def test_create_temp_directory_no_delete() -> None:
    """
    Test case 5: Create persistent temp directory (delete=False).
    """
    # Act
    with create_temp_directory(delete=False) as temp_dir:
        temp_dir_path = Path(temp_dir)
        assert temp_dir_path.exists()

        # Create file in directory
        test_file = temp_dir_path / "persistent.txt"
        test_file.write_text("persistent content")

    # Assert directory still exists after context
    assert temp_dir_path.exists()
    assert (temp_dir_path / "persistent.txt").exists()

    # Cleanup
    try:
        shutil.rmtree(temp_dir_path)
    except OSError:
        pass


def test_create_temp_directory_nested_structure() -> None:
    """
    Test case 6: Create nested structure in temp directory.
    """
    # Act
    with create_temp_directory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create nested structure
        subdir = temp_path / "subdir"
        subdir.mkdir()
        (subdir / "file.txt").write_text("nested content")

        # Assert
        assert subdir.exists()
        assert (subdir / "file.txt").exists()
        assert (subdir / "file.txt").read_text() == "nested content"

    # Assert all is cleaned up
    assert not temp_path.exists()


def test_create_temp_directory_path_object_directory() -> None:
    """
    Test case 7: Function works with Path object for parent directory.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as parent_dir:
        parent_path = Path(parent_dir)

        # Act
        with create_temp_directory(dir=parent_path) as temp_dir:
            # Assert
            assert Path(temp_dir).parent == parent_path
            assert Path(temp_dir).exists()


def test_create_temp_directory_cleanup_error_handling() -> None:
    """
    Test case 8: Graceful handling of cleanup errors.
    """
    temp_dir_holder = []

    # Act
    with create_temp_directory() as temp_dir:
        temp_dir_holder.append(temp_dir)
        assert Path(temp_dir).exists()

        # Manually delete the directory to simulate cleanup error
        shutil.rmtree(temp_dir)

    # Assert - should not raise error even if directory was already deleted
    assert not Path(temp_dir_holder[0]).exists()


def test_create_temp_directory_invalid_type_errors() -> None:
    """
    Test case 9: TypeError for invalid parameter types.
    """
    # Test invalid suffix type
    with pytest.raises(TypeError, match="suffix must be a string"):
        with create_temp_directory(suffix=123):
            pass

    # Test invalid prefix type
    with pytest.raises(TypeError, match="prefix must be a string"):
        with create_temp_directory(prefix=123):
            pass

    # Test invalid dir type
    with pytest.raises(TypeError, match="dir must be a string, Path, or None"):
        with create_temp_directory(dir=123):
            pass

    # Test invalid delete type
    with pytest.raises(TypeError, match="delete must be a boolean"):
        with create_temp_directory(delete="not_bool"):
            pass


def test_create_temp_directory_directory_creation_error() -> None:
    """
    Test case 10: OSError handling during directory creation.
    """
    # Mock mkdtemp to raise OSError
    with patch("tempfile.mkdtemp", side_effect=OSError("Permission denied")):
        # Act & Assert
        with pytest.raises(OSError, match="Error creating temporary directory"):
            with create_temp_directory():
                pass
