import pytest
from typing import Any
from decorators.format_output import format_output

# Example function to be decorated
@format_output("Result: {}")
def sample_function(a: int, b: int) -> int:
    return a + b

@format_output("Result: {}")
def sample_function_args_kwargs(*args: Any, **kwargs: Any) -> str:
    return f"args: {args}, kwargs: {kwargs}"

@format_output("Result: {}")
def sample_function_raises_error(a: int, b: int) -> int:
    raise ValueError("An error occurred")

def test_format_output_basic() -> None:
    """
    Test case 1: Basic functionality of format_output
    """
    result = sample_function(1, 2)
    assert result == "Result: 3"

def test_format_output_with_kwargs() -> None:
    """
    Test case 2: Format output with kwargs
    """
    @format_output("Result: {}")
    def sample_function_kwargs(a: int, b: int) -> int:
        return a + b
    
    result = sample_function_kwargs(a=1, b=2)
    assert result == "Result: 3"

def test_format_output_with_mixed_args() -> None:
    """
    Test case 3: Format output with mixed args and kwargs
    """
    @format_output("Result: {}")
    def sample_function_mixed(a: int, b: int, c: int) -> int:
        return a + b + c
    
    result = sample_function_mixed(1, b=2, c=3)
    assert result == "Result: 6"

def test_format_output_with_non_string() -> None:
    """
    Test case 4: Format output with non-string return value
    """
    @format_output("Result: {}")
    def sample_function_non_string(a: int, b: int) -> int:
        return a + b
    
    result = sample_function_non_string(1, 2)
    assert result == "Result: 3"

def test_format_output_with_variable_length_arguments() -> None:
    """
    Test case 5: Format output with variable length arguments (*args and **kwargs)
    """
    result = sample_function_args_kwargs(1, 2, 3, kwarg1="test", kwarg2="example")
    assert result == "Result: args: (1, 2, 3), kwargs: {'kwarg1': 'test', 'kwarg2': 'example'}"

def test_format_output_mixed_type_arguments() -> None:
    """
    Test case 6: Format output with mixed type arguments
    """
    @format_output("Result: {}")
    def sample_function_mixed_types(a: int, b: str, c: float) -> str:
        return f"{a} - {b} - {c}"
    
    result = sample_function_mixed_types(1, "test", 2.0)
    assert result == "Result: 1 - test - 2.0"

def test_format_output_function_raises_error() -> None:
    """
    Test case 7: Format output when the wrapped function raises an error
    """
    with pytest.raises(ValueError, match="An error occurred"):
        sample_function_raises_error(1, 2)

def test_format_output_invalid_format_string() -> None:
    """
    Test case 8: Invalid format string type
    """
    with pytest.raises(TypeError, match="format_string must be a string"):
        @format_output(123)
        def sample_function_invalid_format_string(a: int, b: int) -> int:
            return a + b
