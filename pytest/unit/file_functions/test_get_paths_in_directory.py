import os
from pathlib import Path

import pytest

from file_functions.get_paths_in_directory import get_paths_in_directory


def test_get_paths_in_directory_files_only(tmp_path: Path) -> None:
    """
    Test retrieving only files from a directory containing files and folders.
    """
    # Test case 1: Directory with files and folders
    (tmp_path / "file1.txt").write_text("a")
    (tmp_path / "file2.log").write_text("b")
    (tmp_path / "folder").mkdir()
    expected_paths: list[str] = [
        os.path.join(tmp_path, "file1.txt"),
        os.path.join(tmp_path, "file2.log"),
    ]
    returned_paths: list[str] = get_paths_in_directory(str(tmp_path), "files")
    assert sorted(returned_paths) == sorted(
        expected_paths), "Should return only file paths"


def test_get_paths_in_directory_directories_only(tmp_path: Path) -> None:
    """
    Test retrieving only directories from a directory containing files and folders.
    """
    # Test case 2: Directory with files and folders
    (tmp_path / "file.txt").write_text("a")
    folder_path: Path = tmp_path / "folder"
    folder_path.mkdir()
    returned_paths: list[str] = get_paths_in_directory(
        str(tmp_path), "directories")
    expected_paths: list[str] = [os.path.join(tmp_path, "folder")]
    assert returned_paths == expected_paths, "Should return only directory paths"


def test_get_paths_in_directory_all_items(tmp_path: Path) -> None:
    """
    Test retrieving all items (files and directories) from a directory.
    """
    # Test case 3: Directory with mixed content
    (tmp_path / "file.txt").write_text("a")
    (tmp_path / "folder").mkdir()
    expected_paths: list[str] = [
        os.path.join(tmp_path, "file.txt"),
        os.path.join(tmp_path, "folder"),
    ]
    returned_paths: list[str] = get_paths_in_directory(str(tmp_path), "all")
    assert sorted(returned_paths) == sorted(
        expected_paths), "Should return files and directories"


def test_get_paths_in_directory_empty_directory(tmp_path: Path) -> None:
    """
    Test retrieving paths from an empty directory.
    """
    # Test case 4: Empty directory
    returned_paths: list[str] = get_paths_in_directory(str(tmp_path), "files")
    assert returned_paths == [], "Empty directory should return empty list"


def test_get_paths_in_directory_hidden_files(tmp_path: Path) -> None:
    """
    Test that hidden files are included when retrieving files.
    """
    # Test case 5: Directory with a hidden file
    hidden_file: Path = tmp_path / ".hidden"
    hidden_file.write_text("secret")
    expected_paths: list[str] = [os.path.join(tmp_path, ".hidden")]
    returned_paths: list[str] = get_paths_in_directory(str(tmp_path), "files")
    assert returned_paths == expected_paths, "Should include hidden files"


def test_get_paths_in_directory_relative_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    Test using a relative path to the directory.
    """
    # Test case 6: Relative directory path
    subdir: Path = tmp_path / "sub"
    subdir.mkdir()
    (subdir / "file.txt").write_text("a")
    monkeypatch.chdir(tmp_path)
    returned_paths: list[str] = get_paths_in_directory("sub", "files")
    expected_paths: list[str] = [os.path.join("sub", "file.txt")]
    assert returned_paths == expected_paths, "Should work with relative paths"


def test_get_paths_in_directory_trailing_slash(tmp_path: Path) -> None:
    """
    Test directory path with a trailing slash.
    """
    # Test case 7: Path with trailing slash
    (tmp_path / "file.txt").write_text("a")
    path_with_slash: str = os.path.join(str(tmp_path), "")
    returned_paths: list[str] = get_paths_in_directory(
        path_with_slash, "files")
    expected_paths: list[str] = [os.path.join(tmp_path, "file.txt")]
    assert returned_paths == expected_paths, "Should handle paths with trailing slash"


def test_get_paths_in_directory_non_recursive(tmp_path: Path) -> None:
    """
    Test that the function does not search recursively in subdirectories.
    """
    # Test case 8: Nested directory structure
    (tmp_path / "top.txt").write_text("a")
    nested_dir: Path = tmp_path / "nested"
    nested_dir.mkdir()
    (nested_dir / "inner.txt").write_text("b")
    returned_paths: list[str] = get_paths_in_directory(str(tmp_path), "files")
    expected_paths: list[str] = [os.path.join(tmp_path, "top.txt")]
    assert returned_paths == expected_paths, "Should not include files from nested directories"


def test_get_paths_in_directory_invalid_type(tmp_path: Path) -> None:
    """
    Test that providing an invalid type raises a ValueError.
    """
    # Test case 9: Invalid type argument
    with pytest.raises(ValueError):
        get_paths_in_directory(str(tmp_path), "invalid")


def test_get_paths_in_directory_nonexistent_directory(tmp_path: Path) -> None:
    """
    Test that providing a non-existent directory raises an error.
    """
    # Test case 10: Non-existent directory
    missing_dir: str = os.path.join(str(tmp_path), "missing")
    with pytest.raises(FileNotFoundError):
        get_paths_in_directory(missing_dir, "files")
