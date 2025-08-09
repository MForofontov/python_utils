import os
import pwd
import pytest
from file_functions.create_directory import create_directory


def test_create_new_directory(tmp_path) -> None:
    """Creating a new directory should return True and create the directory."""
    new_dir = tmp_path / "new"
    result: bool = create_directory(str(new_dir))
    assert result is True, "Should return True for new directory"
    assert new_dir.exists(), "Directory should exist after creation"


def test_existing_directory(tmp_path) -> None:
    """Calling on an existing directory should return False."""
    existing_dir = tmp_path / "existing"
    create_directory(str(existing_dir))
    result: bool = create_directory(str(existing_dir))
    assert result is False, "Should return False if directory already exists"


def test_nested_path_creation(tmp_path) -> None:
    """Creating nested directories should succeed."""
    nested_dir = tmp_path / "level1" / "level2" / "level3"
    result: bool = create_directory(str(nested_dir))
    assert result is True, "Should return True when creating nested path"
    assert nested_dir.exists(), "Nested directory should exist after creation"


def test_permission_error_read_only_parent(tmp_path) -> None:
    """Attempting to create a directory in a read-only parent should raise PermissionError."""
    parent_dir = tmp_path / "parent"
    parent_dir.mkdir()
    parent_dir.chmod(0o555)
    child_dir = parent_dir / "child"

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
