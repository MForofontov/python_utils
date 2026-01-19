import logging
from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.decorators]
from python_utils.decorators.log_function_calls import log_function_calls

# Configure test_logger
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
test_logger.addHandler(handler)


# Example function to be decorated
@log_function_calls(logger=test_logger)
def sample_function(a: int, b: str) -> str:
    return f"{a} - {b}"


@log_function_calls(logger=test_logger)
def sample_function_args_kwargs(*args: Any, **kwargs: Any) -> str:
    return f"args: {args}, kwargs: {kwargs}"


@log_function_calls(logger=test_logger)
def sample_function_raises_error(a: int, b: str) -> str:
    raise ValueError("An error occurred")


def test_log_function_calls_basic(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 1: Basic functionality of log_function_calls
    """
    with caplog.at_level(logging.INFO):
        result = sample_function(1, "test")
    assert result == "1 - test"
    assert (
        "Calling sample_function with args: (1, 'test') and kwargs: {}" in caplog.text
    )
    assert "sample_function returned: 1 - test" in caplog.text


def test_log_function_calls_with_kwargs(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 2: Log function calls with kwargs
    """

    @log_function_calls(logger=test_logger)
    def sample_function_kwargs(a: int, b: str) -> str:
        return f"{a} - {b}"

    with caplog.at_level(logging.INFO):
        result = sample_function_kwargs(a=1, b="test")
    assert result == "1 - test"
    assert (
        "Calling sample_function_kwargs with args: () and kwargs: {'a': 1, 'b': 'test'}"
        in caplog.text
    )
    assert "sample_function_kwargs returned: 1 - test" in caplog.text


def test_log_function_calls_with_mixed_args(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 3: Log function calls with mixed args and kwargs
    """

    @log_function_calls(logger=test_logger)
    def sample_function_mixed(a: int, b: str, c: float) -> str:
        return f"{a} - {b} - {c}"

    with caplog.at_level(logging.INFO):
        result = sample_function_mixed(1, b="test", c=2.0)
    assert result == "1 - test - 2.0"
    assert (
        "Calling sample_function_mixed with args: (1,) and kwargs: {'b': 'test', 'c': 2.0}"
        in caplog.text
    )
    assert "sample_function_mixed returned: 1 - test - 2.0" in caplog.text


def test_log_function_calls_with_variable_length_arguments(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test case 4: Log function calls with variable length arguments (*args and **kwargs)
    """

    @log_function_calls(logger=test_logger)
    def sample_function_var_args(a: int, *args: str, **kwargs: float) -> str:
        return f"{a} - {args} - {kwargs}"

    with caplog.at_level(logging.INFO):
        result = sample_function_var_args(1, "arg1", "arg2", kwarg1=1.0, kwarg2=2.0)
    assert result == "1 - ('arg1', 'arg2') - {'kwarg1': 1.0, 'kwarg2': 2.0}"
    assert (
        "Calling sample_function_var_args with args: (1, 'arg1', 'arg2') and kwargs: {'kwarg1': 1.0, 'kwarg2': 2.0}"
        in caplog.text
    )
    assert (
        "sample_function_var_args returned: 1 - ('arg1', 'arg2') - {'kwarg1': 1.0, 'kwarg2': 2.0}"
        in caplog.text
    )


def test_log_function_calls_mixed_type_arguments(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test case 5: Log function calls with mixed type arguments
    """

    @log_function_calls(logger=test_logger)
    def sample_function_mixed_types(a: int, b: str, c: float) -> str:
        return f"{a} - {b} - {c}"

    with caplog.at_level(logging.INFO):
        result = sample_function_mixed_types(1, "test", 2.0)
    assert result == "1 - test - 2.0"
    assert (
        "Calling sample_function_mixed_types with args: (1, 'test', 2.0) and kwargs: {}"
        in caplog.text
    )
    assert "sample_function_mixed_types returned: 1 - test - 2.0" in caplog.text


def test_log_function_calls_function_raises_error(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test case 6: Log function calls when the wrapped function raises an error
    """
    with caplog.at_level(logging.INFO):
        with pytest.raises(ValueError, match="An error occurred"):
            sample_function_raises_error(1, "test")
    assert (
        "Calling sample_function_raises_error with args: (1, 'test') and kwargs: {}"
        in caplog.text
    )
    assert "Exception in sample_function_raises_error:" in caplog.text


def test_log_function_calls_invalid_logger() -> None:
    """
    Test case 7: Invalid logger type
    """
    with pytest.raises(
        TypeError, match="logger must be an instance of logging.Logger."
    ):

        @log_function_calls(logger="invalid_logger")
        def sample_function_invalid_logger(a: int, b: str) -> str:
            return f"{a} - {b}"


if __name__ == "__main__":
    pytest.main()
