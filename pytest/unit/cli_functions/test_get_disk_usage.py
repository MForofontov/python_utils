import tempfile

import pytest
from cli_functions.get_disk_usage import get_disk_usage


def test_get_disk_usage_valid_path() -> None:
    """
    Test case 1: Test get_disk_usage function with valid path returns correct disk information.
    """
    disk_info = get_disk_usage("/")

    # Check return type
    assert isinstance(disk_info, dict)

    # Check required keys
    required_keys = ["total", "used", "free", "percent_used"]
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


def test_get_disk_usage_temp_directory() -> None:
    """
    Test case 2: Test get_disk_usage function with temporary directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        disk_info = get_disk_usage(temp_dir)
        assert isinstance(disk_info, dict)
        assert disk_info["total"] > 0


def test_get_disk_usage_invalid_path_error() -> None:
    """
    Test case 3: Test get_disk_usage function with invalid path raises FileNotFoundError.
    """
    with pytest.raises(FileNotFoundError, match="Path does not exist"):
        get_disk_usage("/nonexistent/path")


def test_get_disk_usage_invalid_type_error() -> None:
    """
    Test case 4: Test get_disk_usage function with invalid input type raises TypeError.
    """
    with pytest.raises(TypeError, match="path must be a string"):
        get_disk_usage(123)

    with pytest.raises(TypeError):
        get_disk_usage(None)


def test_get_disk_usage_percent_calculation() -> None:
    """
    Test case 5: Verify percent_used calculation is accurate.
    """
    disk_info = get_disk_usage("/")

    expected_percent = (
        (disk_info["used"] / disk_info["total"]) * 100 if disk_info["total"] > 0 else 0
    )
    assert abs(disk_info["percent_used"] - expected_percent) < 0.01


def test_get_disk_usage_multiple_paths() -> None:
    """
    Test case 6: Test disk usage for multiple valid paths.
    """
    with tempfile.TemporaryDirectory() as temp_dir1:
        with tempfile.TemporaryDirectory() as temp_dir2:
            disk_info1 = get_disk_usage(temp_dir1)
            disk_info2 = get_disk_usage(temp_dir2)

            # Both should return valid data
            assert disk_info1["total"] > 0
            assert disk_info2["total"] > 0
