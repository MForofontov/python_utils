import pytest
from typing import Any
from decorators.normalize_input import normalize_input

# Example normalization function
def to_lowercase(value: Any) -> Any:
    if isinstance(value, str):
        return value.lower()
    return value

# Example function to be decorated
@normalize_input(to_lowercase)
def sample_function(a: str, b: str) -> str:
    return f"{a} - {b}"

@normalize_input(to_lowercase)
def sample_function_args_kwargs(*args: Any, **kwargs: Any) -> str:
    return f"args: {args}, kwargs: {kwargs}"

@normalize_input(to_lowercase)
def sample_function_raises_error(a: str, b: str) -> str:
    raise ValueError("An error occurred")

def test_normalize_input_basic() -> None:
    """
    Test case 1: Basic functionality of normalize_input
    """
    result = sample_function("HELLO", "WORLD")
    assert result == "hello - world"

def test_normalize_input_with_kwargs() -> None:
    """
    Test case 2: Normalize input with kwargs
    """
    @normalize_input(to_lowercase)
    def sample_function_kwargs(a: str, b: str) -> str:
        return f"{a} - {b}"
    
    result = sample_function_kwargs(a="HELLO", b="WORLD")
    assert result == "hello - world"

def test_normalize_input_with_mixed_args() -> None:
    """
    Test case 3: Normalize input with mixed args and kwargs
    """
    @normalize_input(to_lowercase)
    def sample_function_mixed(a: str, b: str, c: str) -> str:
        return f"{a} - {b} - {c}"
    
    result = sample_function_mixed("HELLO", b="WORLD", c="PYTHON")
    assert result == "hello - world - python"

def test_normalize_input_with_non_string() -> None:
    """
    Test case 4: Normalize input with non-string arguments
    """
    @normalize_input(to_lowercase)
    def sample_function_non_string(a: str, b: int) -> str:
        return f"{a} - {b}"
    
    result = sample_function_non_string("HELLO", 123)
    assert result == "hello - 123"

def test_normalize_input_with_variable_length_arguments() -> None:
    """
    Test case 5: Normalize input with variable length arguments (*args and **kwargs)
    """
    result = sample_function_args_kwargs("HELLO", "WORLD", kwarg1="PYTHON", kwarg2="TEST")
    assert result == "args: ('hello', 'world'), kwargs: {'kwarg1': 'python', 'kwarg2': 'test'}"

def test_normalize_input_mixed_type_arguments() -> None:
    """
    Test case 6: Normalize input with mixed type arguments
    """
    @normalize_input(to_lowercase)
    def sample_function_mixed_types(a: str, b: int, c: str) -> str:
        return f"{a} - {b} - {c}"
    
    result = sample_function_mixed_types("HELLO", 123, "WORLD")
    assert result == "hello - 123 - world"

def test_normalize_input_function_raises_error() -> None:
    """
    Test case 7: Normalize input when the wrapped function raises an error
    """
    with pytest.raises(ValueError, match="An error occurred"):
        sample_function_raises_error("HELLO", "WORLD")

def test_normalize_input_non_callable() -> None:
    """
    Test case 8: Non-callable normalization function
    """
    with pytest.raises(TypeError, match="Normalizer 123 is not callable"):
        @normalize_input(123)
        def sample_function_invalid(a: str, b: str) -> str:
            return f"{a} - {b}"
