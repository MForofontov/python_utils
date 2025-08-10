import os
import pwd
from pathlib import Path

import pytest

from file_functions.create_directory import create_directory


def test_create_new_directory(tmp_path: Path) -> None:
    """Creating a new directory should return True and create the directory."""
    # Test case 1: Create new directory
    new_dir: Path = tmp_path / "new"
    result: bool = create_directory(str(new_dir))
    assert result is True, "Should return True for new directory"
    assert new_dir.exists(), "Directory should exist after creation"


def test_existing_directory(tmp_path: Path) -> None:
    """Calling on an existing directory should return False."""
    # Test case 2: Directory already exists
    existing_dir: Path = tmp_path / "existing"
    create_directory(str(existing_dir))
    result: bool = create_directory(str(existing_dir))
    assert result is False, "Should return False if directory already exists"


def test_path_is_existing_file(tmp_path: Path) -> None:
    """Calling on a path that points to a file should return False and keep the file."""
    # Test case 3: Path points to existing file
    file_path: Path = tmp_path / "target"
    file_path.write_text("data")
    result: bool = create_directory(str(file_path))
    assert result is False, "Should return False if path already exists as a file"
    assert file_path.exists(), "Existing file should remain after call"


def test_nested_path_creation(tmp_path: Path) -> None:
    """Creating nested directories should succeed."""
    # Test case 4: Create nested directory path
    nested_dir: Path = tmp_path / "level1" / "level2" / "level3"
    result: bool = create_directory(str(nested_dir))
    assert result is True, "Should return True when creating nested path"
    assert nested_dir.exists(), "Nested directory should exist after creation"


def test_permission_error_read_only_parent(tmp_path: Path) -> None:
    """Attempting to create a directory in a read-only parent should raise PermissionError."""
    # Test case 5: Read-only parent directory
    parent_dir: Path = tmp_path / "parent"
    parent_dir.mkdir()
    parent_dir.chmod(0o555)
    child_dir: Path = parent_dir / "child"

    uid = pwd.getpwnam("nobody").pw_uid
    gid = pwd.getpwnam("nobody").pw_gid
    original_uid = os.geteuid()
    original_gid = os.getegid()
    try:
        os.setegid(gid)
        os.seteuid(uid)
        with pytest.raises(PermissionError):
            create_directory(str(child_dir))
    finally:
        os.seteuid(original_uid)
        os.setegid(original_gid)
        parent_dir.chmod(0o755)
