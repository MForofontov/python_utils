import tempfile
from pathlib import Path

from file_functions.directory_operations.copy_folder import copy_folder


def test_copy_folder_basic_copy() -> None:
    """
    Test case 1: Copy folder with files successfully.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        src = Path(temp_dir) / "source"
        dest = Path(temp_dir) / "destination"

        src.mkdir()
        (src / "file1.txt").write_text("content1")
        (src / "file2.txt").write_text("content2")

        # Act
        copy_folder(str(src), str(dest))

        # Assert
        assert dest.exists()
        assert (dest / "file1.txt").exists()
        assert (dest / "file2.txt").exists()
        assert (dest / "file1.txt").read_text() == "content1"
        assert (dest / "file2.txt").read_text() == "content2"


def test_copy_folder_with_subdirectories() -> None:
    """
    Test case 2: Copy folder with subdirectories.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        src = Path(temp_dir) / "source"
        dest = Path(temp_dir) / "destination"

        src.mkdir()
        subdir = src / "subdir"
        subdir.mkdir()
        (subdir / "nested_file.txt").write_text("nested content")

        # Act
        copy_folder(str(src), str(dest))

        # Assert
        assert (dest / "subdir").exists()
        assert (dest / "subdir" / "nested_file.txt").exists()
        assert (dest / "subdir" / "nested_file.txt").read_text() == "nested content"


def test_copy_folder_creates_destination() -> None:
    """
    Test case 3: Destination folder is created if it doesn't exist.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        src = Path(temp_dir) / "source"
        dest = Path(temp_dir) / "new" / "destination"

        src.mkdir()
        (src / "file.txt").write_text("content")

        # Act
        copy_folder(str(src), str(dest))

        # Assert
        assert dest.exists()
        assert (dest / "file.txt").exists()


def test_copy_folder_empty_folder() -> None:
    """
    Test case 4: Copy empty folder.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        src = Path(temp_dir) / "source"
        dest = Path(temp_dir) / "destination"

        src.mkdir()

        # Act
        copy_folder(str(src), str(dest))

        # Assert
        assert dest.exists()
        assert list(dest.iterdir()) == []


def test_copy_folder_overwrites_existing() -> None:
    """
    Test case 5: Existing files in destination are overwritten.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        src = Path(temp_dir) / "source"
        dest = Path(temp_dir) / "destination"

        src.mkdir()
        dest.mkdir()
        (src / "file.txt").write_text("new content")
        (dest / "file.txt").write_text("old content")

        # Act
        copy_folder(str(src), str(dest))

        # Assert
        assert (dest / "file.txt").read_text() == "new content"


def test_copy_folder_multiple_files() -> None:
    """
    Test case 6: Copy folder with multiple files.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        src = Path(temp_dir) / "source"
        dest = Path(temp_dir) / "destination"

        src.mkdir()
        for i in range(5):
            (src / f"file{i}.txt").write_text(f"content{i}")

        # Act
        copy_folder(str(src), str(dest))

        # Assert
        for i in range(5):
            assert (dest / f"file{i}.txt").exists()
            assert (dest / f"file{i}.txt").read_text() == f"content{i}"


def test_copy_folder_deep_hierarchy() -> None:
    """
    Test case 7: Copy folder with deep directory hierarchy.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        src = Path(temp_dir) / "source"
        dest = Path(temp_dir) / "destination"

        src.mkdir()
        deep_path = src / "a" / "b" / "c"
        deep_path.mkdir(parents=True)
        (deep_path / "deep_file.txt").write_text("deep content")

        # Act
        copy_folder(str(src), str(dest))

        # Assert
        assert (dest / "a" / "b" / "c" / "deep_file.txt").exists()
        assert (dest / "a" / "b" / "c" / "deep_file.txt").read_text() == "deep content"


def test_copy_folder_preserves_structure() -> None:
    """
    Test case 8: Verify folder structure is preserved.
    """
    # Arrange
    with tempfile.TemporaryDirectory() as temp_dir:
        src = Path(temp_dir) / "source"
        dest = Path(temp_dir) / "destination"

        src.mkdir()
        (src / "dir1").mkdir()
        (src / "dir2").mkdir()
        (src / "dir1" / "file1.txt").write_text("content1")
        (src / "dir2" / "file2.txt").write_text("content2")

        # Act
        copy_folder(str(src), str(dest))

        # Assert
        assert (dest / "dir1").is_dir()
        assert (dest / "dir2").is_dir()
        assert (dest / "dir1" / "file1.txt").is_file()
        assert (dest / "dir2" / "file2.txt").is_file()
