import tempfile

import pytest
from linux_functions.get_disk_usage import get_disk_usage


def test_get_disk_usage_valid_path() -> None:
    """
    Test case 1: Test get_disk_usage function with valid path returns correct disk information.
    """
    disk_info: dict[str, int | float] = get_disk_usage("/")

    # Check return type
    assert isinstance(disk_info, dict)

    # Check required keys
    required_keys: list[str] = ["total", "used", "free", "percent_used"]
    for key in required_keys:
        assert key in disk_info

    # Check values are reasonable
    assert disk_info["total"] > 0
    assert disk_info["used"] >= 0
    assert disk_info["free"] >= 0
    assert 0 <= disk_info["percent_used"] <= 100

    # Check relationships
    assert disk_info["used"] <= disk_info["total"]
    assert disk_info["free"] <= disk_info["total"]


def test_get_disk_usage_with_temp_dir() -> None:
    """
    Test case 2: Test get_disk_usage function with temporary directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        disk_info: dict[str, int | float] = get_disk_usage(temp_dir)
        assert isinstance(disk_info, dict)
        assert disk_info["total"] > 0


def test_get_disk_usage_invalid_path() -> None:
    """
    Test case 3: Test get_disk_usage function with invalid path raises FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError):
        get_disk_usage("/nonexistent/path")


def test_get_disk_usage_invalid_type() -> None:
    """
    Test case 4: Test get_disk_usage function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError):
        get_disk_usage(123)

    with pytest.raises(TypeError):
        get_disk_usage(None)
