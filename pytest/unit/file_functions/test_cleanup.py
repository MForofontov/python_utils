import os
from file_functions.cleanup import cleanup


def test_cleanup_exclude_relative_names(tmp_path) -> None:
    """
    Ensure cleanup keeps items specified by relative names.
    """
    keep_file = tmp_path / "keep.txt"
    keep_file.write_text("data")
    remove_file = tmp_path / "remove.txt"
    remove_file.write_text("data")
    keep_dir = tmp_path / "keep_dir"
    keep_dir.mkdir()
    remove_dir = tmp_path / "remove_dir"
    remove_dir.mkdir()

    cleanup(str(tmp_path), ["keep.txt", "keep_dir"])

    assert keep_file.exists()
    assert keep_dir.exists()
    assert not remove_file.exists()
    assert not remove_dir.exists()


def test_cleanup_exclude_absolute_paths(tmp_path) -> None:
    """
    Ensure cleanup keeps items specified by absolute paths.
    """
    keep_file = tmp_path / "keep.txt"
    keep_file.write_text("data")
    remove_file = tmp_path / "remove.txt"
    remove_file.write_text("data")
    keep_dir = tmp_path / "keep_dir"
    keep_dir.mkdir()
    remove_dir = tmp_path / "remove_dir"
    remove_dir.mkdir()

    cleanup(str(tmp_path), [str(keep_file), str(keep_dir)])

    assert keep_file.exists()
    assert keep_dir.exists()
    assert not remove_file.exists()
    assert not remove_dir.exists()
