import shutil
import pytest
from file_functions.merge_folders import merge_folders


def test_merge_folders_combines_structure(tmp_path) -> None:
    """Merging two folders should combine their contents."""
    folder1 = tmp_path / "folder1"
    folder2 = tmp_path / "folder2"
    output = tmp_path / "merged"
    folder1.mkdir()
    folder2.mkdir()
    (folder1 / "file1.txt").write_text("a")
    (folder2 / "file2.txt").write_text("b")
    merge_folders(str(folder1), str(folder2), str(output))
    assert (output / "file1.txt").read_text() == "a"
    assert (output / "file2.txt").read_text() == "b"


def test_merge_folders_conflicting_filenames(tmp_path) -> None:
    """Conflicting filenames should produce files with a _copy suffix."""
    folder1 = tmp_path / "folder1"
    folder2 = tmp_path / "folder2"
    output = tmp_path / "merged"
    folder1.mkdir()
    folder2.mkdir()
    (folder1 / "same.txt").write_text("one")
    (folder2 / "same.txt").write_text("two")
    merge_folders(str(folder1), str(folder2), str(output))
    assert (output / "same.txt").read_text() == "one"
    assert (output / "same_copy.txt").read_text() == "two"


def test_merge_folders_nested_directories(tmp_path) -> None:
    """Nested directory structures should be preserved in the merge."""
    folder1 = tmp_path / "folder1"
    folder2 = tmp_path / "folder2"
    output = tmp_path / "merged"
    (folder1 / "sub1").mkdir(parents=True)
    (folder2 / "sub2").mkdir(parents=True)
    (folder1 / "sub1" / "a.txt").write_text("a")
    (folder2 / "sub2" / "b.txt").write_text("b")
    merge_folders(str(folder1), str(folder2), str(output))
    assert (output / "sub1" / "a.txt").read_text() == "a"
    assert (output / "sub2" / "b.txt").read_text() == "b"


def test_merge_folders_missing_input_folder(tmp_path) -> None:
    """Missing input folders should raise FileNotFoundError."""
    folder1 = tmp_path / "folder1"
    missing_folder = tmp_path / "missing"
    output = tmp_path / "merged"
    folder1.mkdir()
    (folder1 / "file1.txt").write_text("a")
    with pytest.raises(FileNotFoundError):
        merge_folders(str(folder1), str(missing_folder), str(output))


def test_merge_folders_read_only_output_dir(tmp_path, monkeypatch) -> None:
    """A read-only output directory should raise PermissionError."""
    folder1 = tmp_path / "folder1"
    folder2 = tmp_path / "folder2"
    output = tmp_path / "merged"
    folder1.mkdir()
    folder2.mkdir()
    output.mkdir()
    (folder1 / "file1.txt").write_text("a")
    (folder2 / "file2.txt").write_text("b")

    def mock_copy2(src, dst, follow_symlinks=True):
        raise PermissionError("Read-only directory")

    monkeypatch.setattr(shutil, "copy2", mock_copy2)
    with pytest.raises(PermissionError):
        merge_folders(str(folder1), str(folder2), str(output))
