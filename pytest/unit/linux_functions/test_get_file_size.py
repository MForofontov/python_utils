import pytest
import tempfile
import os
from linux_functions.get_file_size import get_file_size


def test_get_file_size_valid_file() -> None:
    """
    Test case 1: Test get_file_size function with a valid file returns correct size.
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Write some content to the file
        content: bytes = b"Hello, World!"
        temp_file.write(content)
        temp_file.flush()
        
        try:
            size: int = get_file_size(temp_file.name)
            assert size == len(content)
            assert isinstance(size, int)
        finally:
            os.unlink(temp_file.name)


def test_get_file_size_empty_file() -> None:
    """
    Test case 2: Test get_file_size function with an empty file returns zero.
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        try:
            size: int = get_file_size(temp_file.name)
            assert size == 0
        finally:
            os.unlink(temp_file.name)


def test_get_file_size_nonexistent_file() -> None:
    """
    Test case 3: Test get_file_size function with a nonexistent file raises FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError):
        get_file_size('/nonexistent/file.txt')


def test_get_file_size_directory() -> None:
    """
    Test case 4: Test get_file_size function with a directory raises IsADirectoryError.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(IsADirectoryError):
            get_file_size(temp_dir)


def test_get_file_size_invalid_type() -> None:
    """
    Test case 5: Test get_file_size function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        get_file_size(123)
    
    with pytest.raises(TypeError):
        get_file_size(None)
