import os
from pathlib import Path

import pytest

from file_functions import cleanup


def test_cleanup_exclude_relative_and_absolute(tmp_path: Path) -> None:
    """
    Test case 1: Relative and absolute paths in exclude preserve items.
    """
    keep_file: Path = tmp_path / "keep_file.txt"
    keep_file.write_text("keep")

    keep_dir: Path = tmp_path / "keep_dir"
    keep_dir.mkdir()
    (keep_dir / "inner.txt").write_text("data")

    remove_file: Path = tmp_path / "remove_file.txt"
    remove_file.write_text("remove")

    remove_dir: Path = tmp_path / "remove_dir"
    remove_dir.mkdir()
    (remove_dir / "inner.txt").write_text("remove")

    cleanup(str(tmp_path), ["keep_file.txt", str(keep_dir)])

    assert keep_file.exists(), "Excluded file should remain"
    assert keep_dir.exists(), "Excluded directory should remain"
    assert not remove_file.exists(), "Non-excluded file should be removed"
    assert not remove_dir.exists(), "Non-excluded directory should be removed"


def test_cleanup_removes_non_excluded_items(tmp_path: Path) -> None:
    """
    Test case 2: Non-excluded files, directories, and symlinks are removed.
    """
    file_path: Path = tmp_path / "file.txt"
    file_path.write_text("data")

    dir_path: Path = tmp_path / "dir"
    dir_path.mkdir()
    (dir_path / "inner.txt").write_text("data")

    symlink_path: Path = tmp_path / "link"
    os.symlink(file_path, symlink_path)

    cleanup(str(tmp_path), ["keep.txt"])

    assert not file_path.exists(), "Non-excluded file should be removed"
    assert not dir_path.exists(), "Non-excluded directory should be removed"
    assert not symlink_path.exists(), "Non-excluded symlink should be removed"


def test_cleanup_empty_exclude_wipes_directory(tmp_path: Path) -> None:
    """
    Test case 3: Empty exclude list removes all content.
    """
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b").mkdir()

    cleanup(str(tmp_path), [])

    assert os.listdir(tmp_path) == [], "Directory should be empty after cleanup"


def test_cleanup_nonexistent_directory(tmp_path: Path) -> None:
    """
    Test case 4: Raise FileNotFoundError when directory does not exist.
    """
    missing: Path = tmp_path / "missing"
    with pytest.raises(FileNotFoundError):
        cleanup(str(missing), [])
