import pytest

from file_functions.file_basename import file_basename


def test_file_basename_default_mode() -> None:
    """Test that the default mode returns the filename with extension."""
    # Test case 1: Default behavior includes extension
    path: str = "/path/to/example.txt"
    assert (
        file_basename(path) == "example.txt"
    ), "Should return filename with extension"


def test_file_basename_strip_extension() -> None:
    """Test that setting ``file_extension`` to ``False`` strips the extension."""
    # Test case 2: Strip extension when flag is False
    path: str = "/path/to/example.txt"
    assert (
        file_basename(path, file_extension=False) == "example"
    ), "Should remove the extension"


def test_file_basename_multiple_dots() -> None:
    """Test handling filenames that contain multiple dots."""
    # Test case 3: Filename with multiple dots
    path: str = "/path/to/archive.tar.gz"
    assert file_basename(
        path) == "archive.tar.gz", "Should retain full filename"
    assert (
        file_basename(path, file_extension=False) == "archive.tar"
    ), "Should remove only the last extension"


def test_file_basename_trailing_slash() -> None:
    """Test handling paths that include a trailing slash."""
    # Test case 4: Path with trailing slash
    path: str = "/path/to/file.txt/"
    assert (
        file_basename(path) == "file.txt"
    ), "Should handle trailing slash correctly"
    assert (
        file_basename(path, file_extension=False) == "file"
    ), "Should handle trailing slash and remove extension"


def test_file_basename_empty_path_raises_value_error() -> None:
    """Test that providing an empty path raises a ``ValueError``."""
    # Test case 5: Empty path raises error
    with pytest.raises(ValueError):
        file_basename("")
