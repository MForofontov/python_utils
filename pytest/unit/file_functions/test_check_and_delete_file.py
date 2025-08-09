import os
import pytest
from file_functions.check_and_delete_file import check_and_delete_file


def test_check_and_delete_file_existing_file(tmp_path) -> None:
    """
    Test that deleting an existing file removes it from the filesystem.
    """
    file_path = tmp_path / "temp.txt"
    file_path.write_text("data")
    check_and_delete_file(str(file_path))
    assert not file_path.exists(), "Existing file should be removed"


def test_check_and_delete_file_nonexistent_file(tmp_path) -> None:
    """
    Test that calling the function with a missing file changes nothing.
    """
    sentinel = tmp_path / "sentinel.txt"
    sentinel.write_text("a")
    before = set(os.listdir(tmp_path))
    check_and_delete_file(str(tmp_path / "missing.txt"))
    after = set(os.listdir(tmp_path))
    assert before == after, "Filesystem should remain unchanged"


def test_check_and_delete_file_directory_path(tmp_path) -> None:
    """
    Test that supplying a directory path does not delete the directory.
    """
    dir_path = tmp_path / "folder"
    dir_path.mkdir()
    check_and_delete_file(str(dir_path))
    assert dir_path.exists(), "Directory should not be removed"


def test_check_and_delete_file_permission_error(tmp_path, monkeypatch) -> None:
    """
    Test that attempting to delete a read-only file raises PermissionError.
    """
    file_path = tmp_path / "readonly.txt"
    file_path.write_text("data")
    file_path.chmod(0o400)

    def mock_remove(path):
        raise PermissionError

    monkeypatch.setattr(os, "remove", mock_remove)
    with pytest.raises(PermissionError):
        check_and_delete_file(str(file_path))
    assert file_path.exists(), "File should remain when deletion is not permitted"
