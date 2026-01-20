import logging
from typing import Any

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.decorators]
from pyutils_collection.decorators.manipulate_output import manipulate_output

# Configure test_logger
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
test_logger.addHandler(handler)


# Example manipulation function
def add_exclamation(value: Any) -> Any:
    if isinstance(value, str):
        return f"{value}!"
    return value


# Example function to be decorated
@manipulate_output(add_exclamation, logger=test_logger)
def sample_function(a: str, b: str) -> str:
    return f"{a} - {b}"


@manipulate_output(add_exclamation, logger=test_logger)
def sample_function_args_kwargs(*args: Any, **kwargs: Any) -> str:
    return f"args: {args}, kwargs: {kwargs}"


@manipulate_output(add_exclamation, logger=test_logger)
def sample_function_raises_error(a: str, b: str) -> str:
    raise ValueError("An error occurred")


def test_manipulate_output_basic() -> None:
    """
    Test case 1: Basic functionality of manipulate_output
    """
    result = sample_function("hello", "world")
    assert result == "hello - world!"


def test_manipulate_output_with_kwargs() -> None:
    """
    Test case 2: Manipulate output with kwargs
    """

    @manipulate_output(add_exclamation)
    def sample_function_kwargs(a: str, b: str) -> str:
        return f"{a} - {b}"

    result = sample_function_kwargs(a="hello", b="world")
    assert result == "hello - world!"


def test_manipulate_output_with_mixed_args() -> None:
    """
    Test case 3: Manipulate output with mixed args and kwargs
    """

    @manipulate_output(add_exclamation)
    def sample_function_mixed(a: str, b: str, c: str) -> str:
        return f"{a} - {b} - {c}"

    result = sample_function_mixed("hello", b="world", c="python")
    assert result == "hello - world - python!"


def test_manipulate_output_with_non_string() -> None:
    """
    Test case 4: Manipulate output with non-string return value
    """

    @manipulate_output(add_exclamation)
    def sample_function_non_string(a: str, b: int) -> str:
        return f"{a} - {b}"

    result = sample_function_non_string("hello", 123)
    assert result == "hello - 123!"


def test_manipulate_output_with_variable_length_arguments() -> None:
    """
    Test case 5: Manipulate output with variable length arguments (*args and **kwargs)
    """
    result = sample_function_args_kwargs(
        "hello", "world", kwarg1="python", kwarg2="test"
    )
    assert (
        result
        == "args: ('hello', 'world'), kwargs: {'kwarg1': 'python', 'kwarg2': 'test'}!"
    )


def test_manipulate_output_mixed_type_arguments() -> None:
    """
    Test case 6: Manipulate output with mixed type arguments
    """

    @manipulate_output(add_exclamation)
    def sample_function_mixed_types(a: str, b: int, c: str) -> str:
        return f"{a} - {b} - {c}"

    result = sample_function_mixed_types("hello", 123, "world")
    assert result == "hello - 123 - world!"


def test_manipulate_output_function_raises_error() -> None:
    """
    Test case 7: Manipulate output when the wrapped function raises an error
    """
    with pytest.raises(ValueError, match="An error occurred"):
        sample_function_raises_error("hello", "world")


def test_manipulate_output_non_callable() -> None:
    """
    Test case 8: Non-callable manipulation function
    """
    with pytest.raises(
        TypeError, match="manipulation_func must be a callable function."
    ):

        @manipulate_output(123)
        def sample_function_invalid(a: str, b: str) -> str:
            return f"{a} - {b}"


def test_manipulate_output_invalid_logger() -> None:
    """
    Test case 9: Invalid logger type
    """
    with pytest.raises(
        TypeError, match="logger must be an instance of logging.Logger or None."
    ):

        @manipulate_output(add_exclamation, logger="invalid_logger")
        def sample_function_invalid_logger(a: str, b: str) -> str:
            return f"{a} - {b}"
