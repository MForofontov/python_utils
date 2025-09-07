"""
Unit tests for copy_file function.
"""

import pytest
from pathlib import Path
from file_functions.file_operations.copy_file import copy_file


def test_copy_file_case_1_basic_copy() -> None:
    """
    Test case 1: Basic file copy operation.
    """
    # Arrange
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        source_file = os.path.join(tmp_dir, "source.txt")
        dest_file = os.path.join(tmp_dir, "destination.txt")
        content = "Hello, World!"
        
        with open(source_file, 'w') as f:
            f.write(content)
        
        # Act
        copy_file(source_file, dest_file)
        
        # Assert
        assert os.path.exists(dest_file)
        with open(dest_file, 'r') as f:
            assert f.read() == content


def test_copy_file_case_2_overwrite_existing() -> None:
    """
    Test case 2: Copy file should overwrite existing destination.
    """
    # Arrange
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        source_file = os.path.join(tmp_dir, "source.txt")
        dest_file = os.path.join(tmp_dir, "destination.txt")
        
        # Create source with new content
        new_content = "New content"
        with open(source_file, 'w') as f:
            f.write(new_content)
        
        # Create destination with old content
        old_content = "Old content"
        with open(dest_file, 'w') as f:
            f.write(old_content)
        
        # Act
        copy_file(source_file, dest_file)
        
        # Assert
        with open(dest_file, 'r') as f:
            assert f.read() == new_content


def test_copy_file_case_3_type_validation() -> None:
    """
    Test case 3: Type validation for parameters.
    """
    # Test invalid source_file type
    with pytest.raises(TypeError, match="source_file must be a string"):
        copy_file(123, "dest.txt")
    
    # Test invalid dest_file type
    with pytest.raises(TypeError, match="dest_file must be a string"):
        copy_file("source.txt", 123)


def test_copy_file_case_4_value_validation() -> None:
    """
    Test case 4: Value validation for parameters.
    """
    # Test empty source_file
    with pytest.raises(ValueError, match="source_file cannot be empty"):
        copy_file("", "dest.txt")
    
    # Test empty dest_file
    with pytest.raises(ValueError, match="dest_file cannot be empty"):
        copy_file("source.txt", "")


def test_copy_file_case_5_source_not_found() -> None:
    """
    Test case 5: Non-existent source file should raise FileNotFoundError.
    """
    # Act & Assert
    with pytest.raises(FileNotFoundError, match="Source file does not exist"):
        copy_file("non_existent_file.txt", "dest.txt")


def test_copy_file_case_6_binary_file() -> None:
    """
    Test case 6: Copy binary file correctly.
    """
    # Arrange
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        source_file = os.path.join(tmp_dir, "source.bin")
        dest_file = os.path.join(tmp_dir, "destination.bin")
        
        # Create binary content
        binary_content = b'\x00\x01\x02\x03\xFF\xFE\xFD'
        with open(source_file, 'wb') as f:
            f.write(binary_content)
        
        # Act
        copy_file(source_file, dest_file)
        
        # Assert
        assert os.path.exists(dest_file)
        with open(dest_file, 'rb') as f:
            assert f.read() == binary_content


def test_copy_file_case_7_large_file() -> None:
    """
    Test case 7: Copy large file efficiently.
    """
    # Arrange
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        source_file = os.path.join(tmp_dir, "large_source.txt")
        dest_file = os.path.join(tmp_dir, "large_destination.txt")
        
        # Create large content (1MB)
        large_content = "A" * (1024 * 1024)
        with open(source_file, 'w') as f:
            f.write(large_content)
        
        # Act
        copy_file(source_file, dest_file)
        
        # Assert
        assert os.path.exists(dest_file)
        assert os.path.getsize(dest_file) == os.path.getsize(source_file)


def test_copy_file_case_8_preserve_timestamps() -> None:
    """
    Test case 8: Verify file is copied correctly (basic timestamp check).
    """
    # Arrange
    import tempfile
    import os
    import time
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        source_file = os.path.join(tmp_dir, "source.txt")
        dest_file = os.path.join(tmp_dir, "destination.txt")
        
        content = "Timestamp test"
        with open(source_file, 'w') as f:
            f.write(content)
        
        # Wait a moment to ensure different timestamps
        time.sleep(0.1)
        
        # Act
        copy_file(source_file, dest_file)
        
        # Assert
        assert os.path.exists(dest_file)
        with open(dest_file, 'r') as f:
            assert f.read() == content


def test_copy_file_case_9_unicode_filename() -> None:
    """
    Test case 9: Handle Unicode characters in file names.
    """
    # Arrange
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        source_file = os.path.join(tmp_dir, "源文件.txt")
        dest_file = os.path.join(tmp_dir, "目標文件.txt")
        content = "Unicode filename test"
        
        with open(source_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Act
        copy_file(source_file, dest_file)
        
        # Assert
        assert os.path.exists(dest_file)
        with open(dest_file, 'r', encoding='utf-8') as f:
            assert f.read() == content


def test_copy_file_case_10_same_source_and_dest() -> None:
    """
    Test case 10: Copying to same file should raise ValueError.
    """
    # Arrange
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        same_file = os.path.join(tmp_dir, "same.txt")
        with open(same_file, 'w') as f:
            f.write("test")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Source and destination cannot be the same file"):
            copy_file(same_file, same_file)
