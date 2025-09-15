from pathlib import Path

import pytest

from file_functions import copy_file
from file_functions import copy_folder


def test_copy_file_preserves_contents(tmp_path: Path) -> None:
    """
    Test case 1: Copying a file should keep the original contents.
    """
    source: Path = tmp_path / "source.txt"
    destination: Path = tmp_path / "destination.txt"
    content: str = "sample text"
    source.write_text(content)
    copy_file(str(source), str(destination))
    assert (
        destination.read_text() == content
    ), "Destination should contain the same text as source"


def test_copy_file_overwrite_destination(tmp_path: Path) -> None:
    """
    Test case 2: Existing destination file should be overwritten.
    """
    source: Path = tmp_path / "source.txt"
    destination: Path = tmp_path / "destination.txt"
    source.write_text("new data")
    destination.write_text("old data")
    copy_file(str(source), str(destination))
    assert (
        destination.read_text() == "new data"
    ), "Destination should be overwritten with source content"


def test_copy_folder_replica_structure(tmp_path: Path) -> None:
    """
    Test case 3: Copying a folder should replicate nested files and folders.
    """
    src_folder: Path = tmp_path / "src"
    src_folder.mkdir()
    (src_folder / "file1.txt").write_text("a")
    nested: Path = src_folder / "nested"
    nested.mkdir()
    (nested / "file2.txt").write_text("b")
    dest_folder: Path = tmp_path / "dest"
    copy_folder(str(src_folder), str(dest_folder))
    assert (
        dest_folder / "file1.txt"
    ).read_text() == "a", "Top level file should be copied"
    assert (
        dest_folder / "nested" / "file2.txt"
    ).read_text() == "b", "Nested file should be copied"


def test_copy_folder_overwrite_file(tmp_path: Path) -> None:
    """
    Test case 4: Existing files in destination should be overwritten by source.
    """
    src_folder: Path = tmp_path / "src"
    src_folder.mkdir()
    (src_folder / "file.txt").write_text("new")
    dest_folder: Path = tmp_path / "dest"
    dest_folder.mkdir()
    (dest_folder / "file.txt").write_text("old")
    copy_folder(str(src_folder), str(dest_folder))
    assert (
        dest_folder / "file.txt"
    ).read_text() == "new", "Destination file should be overwritten with source content"


def test_copy_file_missing_source(tmp_path: Path) -> None:
    """
    Test case 5: Missing source file should raise FileNotFoundError.
    """
    missing_source: Path = tmp_path / "missing.txt"
    destination: Path = tmp_path / "destination.txt"
    with pytest.raises(FileNotFoundError):
        copy_file(str(missing_source), str(destination))


def test_copy_folder_missing_source(tmp_path: Path) -> None:
    """
    Test case 6: Missing source folder should raise FileNotFoundError.
    """
    missing_folder: Path = tmp_path / "missing"
    destination: Path = tmp_path / "destination"
    with pytest.raises(FileNotFoundError):
        copy_folder(str(missing_folder), str(destination))
