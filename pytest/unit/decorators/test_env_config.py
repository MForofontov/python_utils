import logging

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.decorators]
from decorators.env_config import env_config

# Configure test_logger
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
test_logger.addHandler(handler)


# Example function to be decorated
@env_config("TEST_VAR", logger=test_logger)
def sample_function(test_var: str) -> str:
    return f"Value: {test_var}"


@env_config("TEST_VAR", var_type=int, logger=test_logger)
def sample_function_int(test_var: int) -> str:
    return f"Value: {test_var}"


@env_config("TEST_VAR", required=False, logger=test_logger)
def sample_function_optional(test_var: str | None) -> str:
    return f"Value: {test_var}"


@env_config(
    "TEST_VAR", var_type=int, custom_message="Custom error message", logger=test_logger
)
def sample_function_custom_message(test_var: int) -> str:
    return f"Value: {test_var}"


def test_env_config_basic(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test case 1: Basic functionality of env_config
    """
    monkeypatch.setenv("TEST_VAR", "test_value")
    result = sample_function()
    assert result == "Value: test_value"


def test_env_config_int(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test case 2: Environment variable with int type
    """
    monkeypatch.setenv("TEST_VAR", "123")
    result = sample_function_int()
    assert result == "Value: 123"


def test_env_config_optional(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test case 3: Optional environment variable
    """
    monkeypatch.delenv("TEST_VAR", raising=False)
    result = sample_function_optional()
    assert result == "Value: None"


def test_env_config_custom_message(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test case 4: Custom error message for invalid environment variable type
    """
    monkeypatch.setenv("TEST_VAR", "invalid_int")
    with pytest.raises(TypeError, match="Custom error message"):
        sample_function_custom_message()


def test_env_config_missing_required(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test case 5: Missing required environment variable
    """
    monkeypatch.delenv("TEST_VAR", raising=False)
    with pytest.raises(
        TypeError, match="Environment variable 'TEST_VAR' is required but not set."
    ):
        sample_function()


def test_env_config_invalid_type(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test case 6: Invalid environment variable type
    """
    monkeypatch.setenv("TEST_VAR", "invalid_int")
    with pytest.raises(
        TypeError, match="Environment variable 'TEST_VAR' must be of type int."
    ):
        sample_function_int()


def test_env_config_invalid_logger() -> None:
    """
    Test case 7: Invalid logger type
    """
    with pytest.raises(
        TypeError, match="logger must be an instance of logging.Logger or None"
    ):

        @env_config("TEST_VAR", logger="invalid_logger")
        def sample_function_invalid_logger(test_var: str) -> str:
            return f"Value: {test_var}"


def test_env_config_invalid_var_name() -> None:
    """
    Test case 8: Invalid var_name type
    """
    with pytest.raises(TypeError, match="var_name must be a non-empty string"):

        @env_config(123, logger=test_logger)
        def sample_function_invalid_var_name(test_var: str) -> str:
            return f"Value: {test_var}"


def test_env_config_invalid_required() -> None:
    """
    Test case 9: Invalid required type
    """
    with pytest.raises(TypeError, match="required must be a boolean"):

        @env_config("TEST_VAR", required="yes", logger=test_logger)
        def sample_function_invalid_required(test_var: str) -> str:
            return f"Value: {test_var}"


def test_env_config_invalid_var_type() -> None:
    """
    Test case 10: Invalid var_type type
    """
    with pytest.raises(TypeError, match="var_type must be a type"):

        @env_config("TEST_VAR", var_type="int", logger=test_logger)
        def sample_function_invalid_var_type(test_var: str) -> str:
            return f"Value: {test_var}"


def test_env_config_invalid_custom_message() -> None:
    """
    Test case 11: Invalid custom_message type
    """
    with pytest.raises(TypeError, match="custom_message must be a string or None"):

        @env_config("TEST_VAR", custom_message=123, logger=test_logger)
        def sample_function_invalid_custom_message(test_var: str) -> str:
            return f"Value: {test_var}"
