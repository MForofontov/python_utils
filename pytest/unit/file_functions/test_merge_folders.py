import shutil
from pathlib import Path

import pytest

from file_functions.merge_folders import merge_folders


def test_merge_folders_combines_structure(tmp_path: Path) -> None:
    """Merging two folders should combine their contents."""
    # Test case 1: Merge distinct contents
    folder1: Path = tmp_path / "folder1"
    folder2: Path = tmp_path / "folder2"
    output: Path = tmp_path / "merged"
    folder1.mkdir()
    folder2.mkdir()
    (folder1 / "file1.txt").write_text("a")
    (folder2 / "file2.txt").write_text("b")
    merge_folders(str(folder1), str(folder2), str(output))
    assert (output / "file1.txt").read_text() == "a", "File from folder1 should exist"
    assert (output / "file2.txt").read_text() == "b", "File from folder2 should exist"


def test_merge_folders_conflicting_filenames(tmp_path: Path) -> None:
    """Conflicting filenames should produce files with a _copy suffix."""
    # Test case 2: Handle conflicting filenames
    folder1: Path = tmp_path / "folder1"
    folder2: Path = tmp_path / "folder2"
    output: Path = tmp_path / "merged"
    folder1.mkdir()
    folder2.mkdir()
    (folder1 / "same.txt").write_text("one")
    (folder2 / "same.txt").write_text("two")
    merge_folders(str(folder1), str(folder2), str(output))
    assert (output / "same.txt").read_text() == "one", "Original file should be copied"
    assert (
        (output / "same_copy.txt").read_text() == "two"
    ), "Conflicting file should be renamed with _copy"


def test_merge_folders_nested_directories(tmp_path: Path) -> None:
    """Nested directory structures should be preserved in the merge."""
    # Test case 3: Preserve nested directories
    folder1: Path = tmp_path / "folder1"
    folder2: Path = tmp_path / "folder2"
    output: Path = tmp_path / "merged"
    (folder1 / "sub1").mkdir(parents=True)
    (folder2 / "sub2").mkdir(parents=True)
    (folder1 / "sub1" / "a.txt").write_text("a")
    (folder2 / "sub2" / "b.txt").write_text("b")
    merge_folders(str(folder1), str(folder2), str(output))
    assert (
        (output / "sub1" / "a.txt").read_text() == "a"
    ), "File in nested sub1 should be copied"
    assert (
        (output / "sub2" / "b.txt").read_text() == "b"
    ), "File in nested sub2 should be copied"


def test_merge_folders_missing_input_folder(tmp_path: Path) -> None:
    """Missing input folders should raise FileNotFoundError."""
    # Test case 4: Missing input folder
    folder1: Path = tmp_path / "folder1"
    missing_folder: Path = tmp_path / "missing"
    output: Path = tmp_path / "merged"
    folder1.mkdir()
    (folder1 / "file1.txt").write_text("a")
    with pytest.raises(FileNotFoundError):
        merge_folders(str(folder1), str(missing_folder), str(output))


def test_merge_folders_read_only_output_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A read-only output directory should raise PermissionError."""
    # Test case 5: Read-only output directory
    folder1: Path = tmp_path / "folder1"
    folder2: Path = tmp_path / "folder2"
    output: Path = tmp_path / "merged"
    folder1.mkdir()
    folder2.mkdir()
    output.mkdir()
    (folder1 / "file1.txt").write_text("a")
    (folder2 / "file2.txt").write_text("b")

    def mock_copy2(src: str, dst: str, follow_symlinks: bool = True) -> None:
        raise PermissionError("Read-only directory")

    monkeypatch.setattr(shutil, "copy2", mock_copy2)
    with pytest.raises(PermissionError):
        merge_folders(str(folder1), str(folder2), str(output))
