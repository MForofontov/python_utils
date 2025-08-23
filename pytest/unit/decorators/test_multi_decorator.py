import pytest
import logging
from typing import Any
from collections.abc import Callable
from decorators.multi_decorator import multi_decorator

# Configure test_logger
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
test_logger.addHandler(handler)


# Example decorators
def decorator1(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return f"decorator1({func(*args, **kwargs)})"

    return wrapper


def decorator2(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return f"decorator2({func(*args, **kwargs)})"

    return wrapper


# Example function to be decorated
@multi_decorator([decorator1, decorator2], logger=test_logger)
def sample_function(a: int, b: int) -> int:
    return a + b


@multi_decorator([decorator1, decorator2], logger=test_logger)
def sample_function_args_kwargs(*args: Any, **kwargs: Any) -> str:
    return f"args: {args}, kwargs: {kwargs}"


@multi_decorator([decorator1, decorator2], logger=test_logger)
def sample_function_raises_error(a: int, b: int) -> int:
    raise ValueError("An error occurred")


def test_multi_decorator_basic(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 1: Basic functionality of multi_decorator
    """
    with caplog.at_level(logging.ERROR):
        result = sample_function(1, 2)
    assert result == "decorator1(decorator2(3))"


def test_multi_decorator_with_kwargs(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 2: Multi decorator with kwargs
    """

    @multi_decorator([decorator1, decorator2], logger=test_logger)
    def sample_function_kwargs(a: int, b: int) -> int:
        return a + b

    with caplog.at_level(logging.ERROR):
        result = sample_function_kwargs(a=1, b=2)
    assert result == "decorator1(decorator2(3))"


def test_multi_decorator_with_mixed_args(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 3: Multi decorator with mixed args and kwargs
    """

    @multi_decorator([decorator1, decorator2], logger=test_logger)
    def sample_function_mixed(a: int, b: int, c: int) -> int:
        return a + b + c

    with caplog.at_level(logging.ERROR):
        result = sample_function_mixed(1, b=2, c=3)
    assert result == "decorator1(decorator2(6))"


def test_multi_decorator_with_variable_length_arguments(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test case 4: Multi decorator with variable length arguments (*args and **kwargs)
    """
    with caplog.at_level(logging.ERROR):
        result = sample_function_args_kwargs(
            1, 2, 3, kwarg1="test", kwarg2="example")
    assert (
        result
        == "decorator1(decorator2(args: (1, 2, 3), kwargs: {'kwarg1': 'test', 'kwarg2': 'example'}))"
    )


def test_multi_decorator_function_raises_error(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test case 5: Multi decorator when the wrapped function raises an error
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="An error occurred"):
            sample_function_raises_error(1, 2)


def test_multi_decorator_invalid_decorator(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 6: Invalid decorator type
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(TypeError, match="Decorator 123 is not callable"):

            @multi_decorator([123], logger=test_logger)
            def sample_function_invalid_decorator(a: int, b: int) -> int:
                return a + b


def test_multi_decorator_invalid_logger() -> None:
    """
    Test case 7: Invalid logger type
    """
    with pytest.raises(
        TypeError, match="logger must be an instance of logging.Logger or None"
    ):

        @multi_decorator([decorator1, decorator2], logger="invalid_logger")
        def sample_function_invalid_logger(a: int, b: int) -> int:
            return a + b


def test_multi_decorator_no_logger() -> None:
    """
    Test case 8: Multi decorator without logger
    """

    @multi_decorator([decorator1, decorator2])
    def sample_function_no_logger(a: int, b: int) -> int:
        return a + b

    result = sample_function_no_logger(1, 2)
    assert result == "decorator1(decorator2(3))"


def test_multi_decorator_invalid_decorator_no_logger() -> None:
    """
    Test case 9: Invalid decorator type without logger
    """
    with pytest.raises(TypeError, match="Decorator 123 is not callable"):

        @multi_decorator([123])
        def sample_function_invalid_decorator(a: int, b: int) -> int:
            return a + b
