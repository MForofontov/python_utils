"""
Unit tests for create_temp_file function.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from file_functions import create_temp_file


def test_create_temp_file_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation with default parameters.
    """
    # Act
    with create_temp_file() as temp_path:
        # Assert
        assert isinstance(temp_path, str)
        assert Path(temp_path).exists()
        assert Path(temp_path).is_file()

        # Write and read content
        with open(temp_path, "w") as f:
            f.write("test content")

        with open(temp_path) as f:
            content = f.read()

        assert content == "test content"

    # Assert file is deleted after context
    assert not Path(temp_path).exists()


def test_create_temp_file_case_2_custom_suffix() -> None:
    """
    Test case 2: Create temp file with custom suffix.
    """
    # Act
    with create_temp_file(suffix=".txt") as temp_path:
        # Assert
        assert temp_path.endswith(".txt")
        assert Path(temp_path).exists()


def test_create_temp_file_case_3_custom_prefix() -> None:
    """
    Test case 3: Create temp file with custom prefix.
    """
    # Act
    with create_temp_file(prefix="test_") as temp_path:
        # Assert
        filename = Path(temp_path).name
        assert filename.startswith("test_")
        assert Path(temp_path).exists()


def test_create_temp_file_case_4_custom_directory() -> None:
    """
    Test case 4: Create temp file in custom directory.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as custom_dir:
        # Act
        with create_temp_file(dir=custom_dir) as temp_path:
            # Assert
            assert Path(temp_path).parent == Path(custom_dir)
            assert Path(temp_path).exists()


def test_create_temp_file_case_5_no_delete() -> None:
    """
    Test case 5: Create persistent temp file (delete=False).
    """
    # Act
    with create_temp_file(delete=False) as temp_path:
        temp_file_path = Path(temp_path)
        assert temp_file_path.exists()

        # Write some content
        with open(temp_path, "w") as f:
            f.write("persistent content")

    # Assert file still exists after context
    assert temp_file_path.exists()

    # Cleanup
    try:
        temp_file_path.unlink()
    except OSError:
        pass


def test_create_temp_file_case_6_binary_mode() -> None:
    """
    Test case 6: Create temp file in binary mode.
    """
    # Act
    with create_temp_file(text=False) as temp_path:
        # Assert
        assert Path(temp_path).exists()

        # Write binary content
        with open(temp_path, "wb") as f:
            f.write(b"binary content")

        with open(temp_path, "rb") as f:
            content = f.read()

        assert content == b"binary content"


def test_create_temp_file_case_7_path_object_directory() -> None:
    """
    Test case 7: Function works with Path object for directory.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as custom_dir:
        custom_path = Path(custom_dir)

        # Act
        with create_temp_file(dir=custom_path) as temp_path:
            # Assert
            assert Path(temp_path).parent == custom_path
            assert Path(temp_path).exists()


def test_create_temp_file_case_8_invalid_type_errors() -> None:
    """
    Test case 8: TypeError for invalid parameter types.
    """
    # Test invalid suffix type
    with pytest.raises(TypeError, match="suffix must be a string"):
        with create_temp_file(suffix=123):
            pass

    # Test invalid prefix type
    with pytest.raises(TypeError, match="prefix must be a string"):
        with create_temp_file(prefix=123):
            pass

    # Test invalid dir type
    with pytest.raises(TypeError, match="dir must be a string, Path, or None"):
        with create_temp_file(dir=123):
            pass

    # Test invalid text type
    with pytest.raises(TypeError, match="text must be a boolean"):
        with create_temp_file(text="not_bool"):
            pass

    # Test invalid delete type
    with pytest.raises(TypeError, match="delete must be a boolean"):
        with create_temp_file(delete="not_bool"):
            pass


def test_create_temp_file_case_9_file_creation_error() -> None:
    """
    Test case 9: OSError handling during file creation.
    """
    # Mock NamedTemporaryFile to raise OSError
    with patch("tempfile.NamedTemporaryFile", side_effect=OSError("Disk full")):
        # Act & Assert
        with pytest.raises(OSError, match="Error creating temporary file"):
            with create_temp_file():
                pass


def test_create_temp_file_case_10_cleanup_error_handling() -> None:
    """
    Test case 10: Graceful handling of cleanup errors.
    """
    temp_path_holder = []

    # Act
    with create_temp_file() as temp_path:
        temp_path_holder.append(temp_path)
        assert Path(temp_path).exists()

        # Manually delete the file to simulate cleanup error
        Path(temp_path).unlink()

    # Assert - should not raise error even if file was already deleted
    assert not Path(temp_path_holder[0]).exists()
