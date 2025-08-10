import os
import os
from pathlib import Path

import pytest

from file_functions.join_paths import join_paths


def test_join_paths_multiple_relative_segments(tmp_path: Path) -> None:
    """
    Test joining multiple relative child segments.
    """
    # Test case 1: Join relative segments
    parent_path: str = str(tmp_path)
    child_segments: list[str] = ["folder", "sub", "file.txt"]
    expected_path: str = os.path.join(parent_path, "folder", "sub", "file.txt")
    joined: str = join_paths(parent_path, child_segments)
    assert joined == expected_path, "Should join all relative child segments"


def test_join_paths_empty_child_list_returns_parent(tmp_path: Path) -> None:
    """
    Test that empty child list returns the parent path unchanged.
    """
    # Test case 2: Empty child segments
    parent_path: str = str(tmp_path)
    returned_path: str = join_paths(parent_path, [])
    assert returned_path == parent_path, "Empty child list should return parent path"


def test_join_paths_absolute_child_supersedes_parent(tmp_path: Path) -> None:
    """
    Test that an absolute child path supersedes the parent path.
    """
    # Test case 3: Absolute child path
    parent_path: str = "/does/not/matter"
    absolute_child: str = os.path.join(str(tmp_path), "abs")
    child_segments: list[str] = [absolute_child, "nested.txt"]
    expected_path: str = os.path.join(absolute_child, "nested.txt")
    joined: str = join_paths(parent_path, child_segments)
    assert joined == expected_path, "Absolute child path should ignore parent path"


def test_join_paths_non_string_child_raises_type_error(tmp_path: Path) -> None:
    """
    Test that providing non-string child paths raises a TypeError.
    """
    # Test case 4: Non-string child path
    parent_path: str = str(tmp_path)
    child_segments: list[object] = ["valid", 123]
    with pytest.raises(TypeError):
        join_paths(parent_path, child_segments)  # type: ignore[arg-type]
