import os
import pytest
from file_functions.cleanup import cleanup


def test_cleanup_exclude_relative_and_absolute(tmp_path) -> None:
    """Relative and absolute paths in exclude preserve items."""
    keep_file = tmp_path / "keep_file.txt"
    keep_file.write_text("keep")

    keep_dir = tmp_path / "keep_dir"
    keep_dir.mkdir()
    (keep_dir / "inner.txt").write_text("data")

    remove_file = tmp_path / "remove_file.txt"
    remove_file.write_text("remove")

    remove_dir = tmp_path / "remove_dir"
    remove_dir.mkdir()
    (remove_dir / "inner.txt").write_text("remove")

    cleanup(str(tmp_path), ["keep_file.txt", str(keep_dir)])

    assert keep_file.exists()
    assert keep_dir.exists()
    assert not remove_file.exists()
    assert not remove_dir.exists()


def test_cleanup_removes_non_excluded_items(tmp_path) -> None:
    """Non-excluded files, directories, and symlinks are removed."""
    file_path = tmp_path / "file.txt"
    file_path.write_text("data")

    dir_path = tmp_path / "dir"
    dir_path.mkdir()
    (dir_path / "inner.txt").write_text("data")

    symlink_path = tmp_path / "link"
    os.symlink(file_path, symlink_path)

    cleanup(str(tmp_path), ["keep.txt"])

    assert not file_path.exists()
    assert not dir_path.exists()
    assert not symlink_path.exists()


def test_cleanup_empty_exclude_wipes_directory(tmp_path) -> None:
    """Empty exclude list removes all content."""
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b").mkdir()

    cleanup(str(tmp_path), [])

    assert os.listdir(tmp_path) == []


def test_cleanup_nonexistent_directory(tmp_path) -> None:
    """Raise FileNotFoundError when directory does not exist."""
    missing = tmp_path / "missing"
    with pytest.raises(FileNotFoundError):
        cleanup(str(missing), [])
