import os
from pathlib import Path

import pytest

from file_functions.get_paths_dict import get_paths_dict


def test_get_paths_dict_files_only(tmp_path: Path) -> None:
    """Test retrieving only files from a directory containing files and folders."""
    # Test case 1: Directory with files and folders
    (tmp_path / "file1.txt").write_text("a")
    (tmp_path / "file2.log").write_text("b")
    (tmp_path / "folder").mkdir()

    expected_paths: dict[str, str] = {
        "file1.txt": os.path.join(tmp_path, "file1.txt"),
        "file2.log": os.path.join(tmp_path, "file2.log"),
    }
    returned_paths: dict[str, str] = get_paths_dict(str(tmp_path), "files")
    assert returned_paths == expected_paths, "Should return only file paths"


def test_get_paths_dict_directories_only(tmp_path: Path) -> None:
    """Test retrieving only directories from a directory containing files and folders."""
    # Test case 2: Directory with files and folders
    (tmp_path / "file.txt").write_text("a")
    folder_path: Path = tmp_path / "folder"
    folder_path.mkdir()

    returned_paths: dict[str, str] = get_paths_dict(
        str(tmp_path), "directories")
    expected_paths: dict[str, str] = {
        "folder": os.path.join(tmp_path, "folder")}
    assert returned_paths == expected_paths, "Should return only directory paths"


def test_get_paths_dict_all_items(tmp_path: Path) -> None:
    """Test retrieving all items (files and directories) from a directory."""
    # Test case 3: Directory with mixed content
    (tmp_path / "file.txt").write_text("a")
    (tmp_path / "folder").mkdir()

    expected_paths: dict[str, str] = {
        "file.txt": os.path.join(tmp_path, "file.txt"),
        "folder": os.path.join(tmp_path, "folder"),
    }
    returned_paths: dict[str, str] = get_paths_dict(str(tmp_path), "all")
    assert returned_paths == expected_paths, "Should return files and directories"


def test_get_paths_dict_invalid_type(tmp_path: Path) -> None:
    """Test that an invalid type argument raises a ValueError."""
    # Test case 4: Invalid type argument
    with pytest.raises(ValueError):
        get_paths_dict(str(tmp_path), "invalid")


def test_get_paths_dict_nonexistent_directory(tmp_path: Path) -> None:
    """Test that a missing directory raises FileNotFoundError."""
    # Test case 5: Missing directory path
    missing_dir: str = os.path.join(str(tmp_path), "missing")
    with pytest.raises(FileNotFoundError):
        get_paths_dict(missing_dir, "files")
