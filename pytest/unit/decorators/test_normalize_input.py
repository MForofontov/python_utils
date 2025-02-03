import pytest
import logging
from typing import Any
from decorators.normalize_input import normalize_input

# Configure test_logger
test_logger = logging.getLogger('test_logger')
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
test_logger.addHandler(handler)

# Example normalization function
def to_uppercase(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Value must be a string")
    return value.upper()

# Example function to be decorated
@normalize_input(to_uppercase, logger=test_logger)
def sample_function(a: str, b: str) -> str:
    return f"{a} - {b}"

@normalize_input(to_uppercase, logger=test_logger)
def sample_function_args_kwargs(*args: Any, **kwargs: Any) -> str:
    return f"args: {args}, kwargs: {kwargs}"

@normalize_input(to_uppercase, logger=test_logger)
def sample_function_raises_error(a: str, b: str) -> str:
    raise ValueError("An error occurred")

def test_normalize_input_basic() -> None:
    """
    Test case 1: Basic functionality of normalize_input
    """
    result = sample_function("hello", "world")
    assert result == "HELLO - WORLD"

def test_normalize_input_with_kwargs() -> None:
    """
    Test case 2: Normalize input with kwargs
    """
    @normalize_input(to_uppercase, logger=test_logger)
    def sample_function_kwargs(a: str, b: str) -> str:
        return f"{a} - {b}"
    
    result = sample_function_kwargs(a="hello", b="world")
    assert result == "HELLO - WORLD"

def test_normalize_input_with_mixed_args() -> None:
    """
    Test case 3: Normalize input with mixed args and kwargs
    """
    @normalize_input(to_uppercase, logger=test_logger)
    def sample_function_mixed(a: str, b: str, c: str) -> str:
        return f"{a} - {b} - {c}"
    
    result = sample_function_mixed("hello", b="world", c="test")
    assert result == "HELLO - WORLD - TEST"

def test_normalize_input_with_non_string() -> None:
    """
    Test case 4: Normalize input with non-string return value
    """
    @normalize_input(to_uppercase, logger=test_logger)
    def sample_function_non_string(a: str, b: str) -> str:
        return f"{a} - {b}"
    
    result = sample_function_non_string("hello", "world")
    assert result == "HELLO - WORLD"

def test_normalize_input_with_variable_length_arguments() -> None:
    """
    Test case 5: Normalize input with variable length arguments (*args and **kwargs)
    """
    result = sample_function_args_kwargs("hello", "world", "test", kwarg1="example", kwarg2="case")
    assert result == "args: ('HELLO', 'WORLD', 'TEST'), kwargs: {'kwarg1': 'EXAMPLE', 'kwarg2': 'CASE'}"

def test_normalize_input_mixed_type_arguments(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 6: Normalize input with mixed type arguments
    """
    @normalize_input(to_uppercase, logger=test_logger)
    def sample_function_mixed_types(a: str, b: str, c: str) -> str:
        return f"{a} - {b} - {c}"
    
    with caplog.at_level(logging.ERROR):
        result = sample_function_mixed_types("hello", "world", "test")
    assert result == "HELLO - WORLD - TEST"

def test_normalize_input_function_raises_error_with_logger(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 7: Normalize input when the wrapped function raises an error
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="Normalization failed:"):
            sample_function_raises_error("hello", "world")
        assert "An error occurred" in caplog.text

def test_normalize_input_function_raises_error_no_logger() -> None:
    """
    Test case 8: Normalize input when the wrapped function raises an error without logger
    """
    with pytest.raises(ValueError, match="An error occurred"):
        sample_function_raises_error("hello", "world")

def test_normalize_input_invalid_normalizer_with_logger(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 9: Invalid normalizer type with logger
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(TypeError, match="Normalizer 123 is not callable"):
            @normalize_input(123, logger=test_logger)
            def sample_function_invalid_normalizer(a: str, b: str) -> str:
                return f"{a} - {b}"
        assert "Normalizer 123 is not callable" in caplog.text

def test_normalize_input_invalid_normalizer_no_logger() -> None:
    """
    Test case 10: Invalid normalizer type without logger
    """
    with pytest.raises(TypeError, match="Normalizer 123 is not callable"):
        @normalize_input(123)
        def sample_function_invalid_normalizer(a: str, b: str) -> str:
            return f"{a} - {b}"


def test_normalize_input_invalid_logger() -> None:
    """
    Test case 11: Invalid logger type
    """
    with pytest.raises(TypeError, match="logger must be an instance of logging.Logger or None"):
        @normalize_input(to_uppercase, logger="invalid_logger")
        def sample_function_invalid_logger(a: str, b: str) -> str:
            return f"{a} - {b}"

def test_normalize_input_normalization_failure_with_logger(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 12: Normalization failure
    """
    def fail_normalizer(value: Any) -> str:
        raise ValueError("Normalization failed")

    @normalize_input(fail_normalizer, logger=test_logger)
    def sample_function_normalization_failure(a: str, b: str) -> str:
        return f"{a} - {b}"
    
    with caplog.at_level(logging.ERROR):
        with pytest.raises(TypeError, match="Normalization failed: Normalization failed"):
            sample_function_normalization_failure("hello", "world")
        assert "Normalization failed: Normalization failed" in caplog.text

def test_normalize_input_normalization_failure_no_logger() -> None:
    """
    Test case 13: Normalization failure without logger
    """
    def fail_normalizer(value: Any) -> str:
        raise ValueError("Normalization failed")

    @normalize_input(fail_normalizer)
    def sample_function_normalization_failure(a: str, b: str) -> str:
        return f"{a} - {b}"
    
    with pytest.raises(TypeError, match="Normalization failed: Normalization failed"):
        sample_function_normalization_failure("hello", "world")
