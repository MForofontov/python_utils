import os
from pathlib import Path

import pytest
from file_functions import (
    get_paths_in_directory_with_suffix,
)


def test_get_paths_in_directory_with_suffix_case_sensitive(tmp_path: Path) -> None:
    """
    Test case 1: Ensure only files with the exact suffix are returned and directories are ignored.
    """
    (tmp_path / "file1.txt").write_text("a")
    (tmp_path / "file2.txt").write_text("b")
    (tmp_path / "file3.log").write_text("c")
    (tmp_path / "file4.TXT").write_text("d")
    (tmp_path / "folder").mkdir()
    expected_paths: list[str] = [
        os.path.join(tmp_path, "file1.txt"),
        os.path.join(tmp_path, "file2.txt"),
    ]
    returned_paths: list[str] = get_paths_in_directory_with_suffix(
        str(tmp_path), ".txt"
    )
    assert sorted(returned_paths) == sorted(expected_paths), (
        "Should return only .txt files"
    )


def test_get_paths_in_directory_with_suffix_no_matching_files(tmp_path: Path) -> None:
    """
    Test case 2: Return an empty list when no files share the suffix.
    """
    (tmp_path / "file1.log").write_text("a")
    (tmp_path / "file2.data").write_text("b")
    (tmp_path / "folder").mkdir()
    returned_paths: list[str] = get_paths_in_directory_with_suffix(
        str(tmp_path), ".txt"
    )
    assert returned_paths == [], "Should return an empty list"


def test_get_paths_in_directory_with_suffix_case_insensitive(tmp_path: Path) -> None:
    """
    Test case 3: Verify files are matched when the suffix case matches the filename.
    """
    (tmp_path / "lower.txt").write_text("a")
    (tmp_path / "upper.TXT").write_text("b")
    expected_paths: list[str] = [os.path.join(tmp_path, "upper.TXT")]
    returned_paths: list[str] = get_paths_in_directory_with_suffix(
        str(tmp_path), ".TXT"
    )
    assert returned_paths == expected_paths, "Should match files with uppercase suffix"


def test_get_paths_in_directory_with_suffix_nonexistent_directory(
    tmp_path: Path,
) -> None:
    """
    Test case 4: Ensure providing a non-existent directory raises an error.
    """
    missing_dir: str = os.path.join(str(tmp_path), "missing")
    with pytest.raises(FileNotFoundError):
        get_paths_in_directory_with_suffix(missing_dir, ".txt")
