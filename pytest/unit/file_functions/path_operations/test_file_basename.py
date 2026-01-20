import pytest

pytestmark = [pytest.mark.unit, pytest.mark.file_functions]
from pyutils_collection.file_functions import file_basename


def test_file_basename_default_mode() -> None:
    """
    Test case 1: Test that the default mode returns the filename with extension.
    """
    path: str = "/path/to/example.txt"
    assert file_basename(path) == "example.txt", "Should return filename with extension"


def test_file_basename_strip_extension() -> None:
    """
    Test case 2: Test that setting ``file_extension`` to ``False`` strips the extension.
    """
    path: str = "/path/to/example.txt"
    assert file_basename(path, file_extension=False) == "example", (
        "Should remove the extension"
    )


def test_file_basename_multiple_dots() -> None:
    """
    Test case 3: Test handling filenames that contain multiple dots.
    """
    path: str = "/path/to/archive.tar.gz"
    assert file_basename(path) == "archive.tar.gz", "Should retain full filename"
    assert file_basename(path, file_extension=False) == "archive.tar", (
        "Should remove only the last extension"
    )


def test_file_basename_trailing_slash() -> None:
    """
    Test case 4: Test handling paths that include a trailing slash.
    """
    path: str = "/path/to/file.txt/"
    assert file_basename(path) == "file.txt", "Should handle trailing slash correctly"
    assert file_basename(path, file_extension=False) == "file", (
        "Should handle trailing slash and remove extension"
    )


def test_file_basename_empty_path_raises_value_error() -> None:
    """
    Test case 5: Test that providing an empty path raises a ``ValueError``.
    """
    with pytest.raises(ValueError):
        file_basename("")
