import pytest
from testing_functions.mock_helpers.mock_file_system import mock_file_system


def test_mock_file_system_case_1_single_file() -> None:
    """
    Test case 1: Create mock filesystem with single file.
    """
    # Arrange
    files = {"/test.txt": "content"}
    
    # Act
    fs = mock_file_system(files)
    
    # Assert
    assert fs.read("/test.txt") == "content"
    assert fs.exists("/test.txt") is True


def test_mock_file_system_case_2_multiple_files() -> None:
    """
    Test case 2: Create mock filesystem with multiple files.
    """
    # Arrange
    files = {
        "/file1.txt": "content1",
        "/file2.txt": "content2",
        "/dir/file3.txt": "content3"
    }
    
    # Act
    fs = mock_file_system(files)
    
    # Assert
    assert fs.read("/file1.txt") == "content1"
    assert fs.read("/file2.txt") == "content2"
    assert fs.read("/dir/file3.txt") == "content3"


def test_mock_file_system_case_3_file_exists() -> None:
    """
    Test case 3: Test exists method.
    """
    # Arrange
    files = {"/existing.txt": "data"}
    
    # Act
    fs = mock_file_system(files)
    
    # Assert
    assert fs.exists("/existing.txt") is True
    assert fs.exists("/nonexisting.txt") is False


def test_mock_file_system_case_4_listdir() -> None:
    """
    Test case 4: Test listdir method.
    """
    # Arrange
    files = {
        "/dir/file1.txt": "content1",
        "/dir/file2.txt": "content2",
        "/other/file3.txt": "content3"
    }
    
    # Act
    fs = mock_file_system(files)
    result = fs.listdir("/dir")
    
    # Assert
    assert len(result) == 2
    assert "/dir/file1.txt" in result
    assert "/dir/file2.txt" in result


def test_mock_file_system_case_5_empty_filesystem() -> None:
    """
    Test case 5: Create empty mock filesystem.
    """
    # Arrange
    files = {}
    
    # Act
    fs = mock_file_system(files)
    
    # Assert
    assert fs.exists("/any.txt") is False


def test_mock_file_system_case_6_files_attribute() -> None:
    """
    Test case 6: Access files attribute.
    """
    # Arrange
    files = {"/test.txt": "content"}
    
    # Act
    fs = mock_file_system(files)
    
    # Assert
    assert fs.files == files


def test_mock_file_system_case_7_read_nonexistent_file() -> None:
    """
    Test case 7: FileNotFoundError when reading nonexistent file.
    """
    # Arrange
    files = {"/existing.txt": "content"}
    
    # Act
    fs = mock_file_system(files)
    
    # Assert
    with pytest.raises(FileNotFoundError, match="File not found"):
        fs.read("/nonexistent.txt")


def test_mock_file_system_case_8_type_error_files() -> None:
    """
    Test case 8: TypeError for invalid files type.
    """
    # Act & Assert
    with pytest.raises(TypeError, match="files must be a dict"):
        mock_file_system("not a dict")
