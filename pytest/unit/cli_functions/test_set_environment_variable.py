import os

import pytest

try:
    import psutil
    from pyutils_collection.cli_functions.set_environment_variable import set_environment_variable
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None  # type: ignore
    set_environment_variable = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.cli_functions,
    pytest.mark.skipif(not PSUTIL_AVAILABLE, reason="psutil not installed"),
]


def test_set_environment_variable_simple_set() -> None:
    """
    Test case 1: Set environment variable successfully.
    """
    set_environment_variable("MY_VAR", "my_value")
    try:
        assert os.environ.get("MY_VAR") == "my_value"
    finally:
        if "MY_VAR" in os.environ:
            del os.environ["MY_VAR"]


def test_set_environment_variable_overwrite_existing() -> None:
    """
    Test case 2: Overwrite existing environment variable.
    """
    os.environ["MY_VAR"] = "old_value"
    set_environment_variable("MY_VAR", "new_value")
    try:
        assert os.environ.get("MY_VAR") == "new_value"
    finally:
        if "MY_VAR" in os.environ:
            del os.environ["MY_VAR"]


def test_set_environment_variable_empty_value() -> None:
    """
    Test case 3: Set environment variable to empty string.
    """
    set_environment_variable("MY_VAR", "")
    try:
        assert os.environ.get("MY_VAR") == ""
    finally:
        if "MY_VAR" in os.environ:
            del os.environ["MY_VAR"]


def test_set_environment_variable_invalid_var_name_type() -> None:
    """
    Test case 4: Invalid var_name type raises TypeError.
    """
    with pytest.raises(TypeError, match="var_name must be a string"):
        set_environment_variable(123, "value")

    with pytest.raises(TypeError):
        set_environment_variable(None, "value")


def test_set_environment_variable_invalid_value_type() -> None:
    """
    Test case 5: Invalid value type raises TypeError.
    """
    with pytest.raises(TypeError, match="value must be a string"):
        set_environment_variable("MY_VAR", 123)

    with pytest.raises(TypeError):
        set_environment_variable("MY_VAR", None)


def test_set_environment_variable_empty_var_name_error() -> None:
    """
    Test case 6: Empty var_name raises ValueError.
    """
    with pytest.raises(ValueError, match="var_name cannot be empty"):
        set_environment_variable("", "value")
