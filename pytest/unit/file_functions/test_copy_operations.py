import pytest
from file_functions.copy_file import copy_file
from file_functions.copy_folder import copy_folder


def test_copy_file_preserves_contents(tmp_path) -> None:
    """Copying a file should keep the original contents."""
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"
    content = "sample text"
    source.write_text(content)
    copy_file(str(source), str(destination))
    assert destination.read_text() == content, "Destination should contain the same text as source"


def test_copy_file_overwrite_destination(tmp_path) -> None:
    """Existing destination file should be overwritten."""
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"
    source.write_text("new data")
    destination.write_text("old data")
    copy_file(str(source), str(destination))
    assert destination.read_text() == "new data", "Destination should be overwritten with source content"


def test_copy_folder_replica_structure(tmp_path) -> None:
    """Copying a folder should replicate nested files and folders."""
    src_folder = tmp_path / "src"
    src_folder.mkdir()
    (src_folder / "file1.txt").write_text("a")
    nested = src_folder / "nested"
    nested.mkdir()
    (nested / "file2.txt").write_text("b")
    dest_folder = tmp_path / "dest"
    copy_folder(str(src_folder), str(dest_folder))
    assert (dest_folder / "file1.txt").read_text() == "a", "Top level file should be copied"
    assert (dest_folder / "nested" / "file2.txt").read_text() == "b", "Nested file should be copied"


def test_copy_folder_overwrite_file(tmp_path) -> None:
    """Existing files in destination should be overwritten by source."""
    src_folder = tmp_path / "src"
    src_folder.mkdir()
    (src_folder / "file.txt").write_text("new")
    dest_folder = tmp_path / "dest"
    dest_folder.mkdir()
    (dest_folder / "file.txt").write_text("old")
    copy_folder(str(src_folder), str(dest_folder))
    assert (
        dest_folder / "file.txt"
    ).read_text() == "new", "Destination file should be overwritten with source content"


def test_copy_file_missing_source(tmp_path) -> None:
    """Missing source file should raise FileNotFoundError."""
    missing_source = tmp_path / "missing.txt"
    destination = tmp_path / "destination.txt"
    with pytest.raises(FileNotFoundError):
        copy_file(str(missing_source), str(destination))


def test_copy_folder_missing_source(tmp_path) -> None:
    """Missing source folder should raise FileNotFoundError."""
    missing_folder = tmp_path / "missing"
    destination = tmp_path / "destination"
    with pytest.raises(FileNotFoundError):
        copy_folder(str(missing_folder), str(destination))
