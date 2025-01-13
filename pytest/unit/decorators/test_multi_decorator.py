import pytest
from typing import Any, Callable
from decorators.multi_decorator import multi_decorator

# Example decorators
def uppercase_decorator(func: Callable[..., str]) -> Callable[..., str]:
    def wrapper(*args: Any, **kwargs: Any) -> str:
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

def exclamation_decorator(func: Callable[..., str]) -> Callable[..., str]:
    def wrapper(*args: Any, **kwargs: Any) -> str:
        result = func(*args, **kwargs)
        return f"{result}!"
    return wrapper

# Example function to be decorated
@multi_decorator(uppercase_decorator, exclamation_decorator)
def sample_function(a: str, b: str) -> str:
    return f"{a} - {b}"

def test_multi_decorator_basic() -> None:
    """
    Test case 1: Basic functionality of multi_decorator
    """
    result = sample_function("hello", "world")
    assert result == "HELLO - WORLD!"

def test_multi_decorator_with_kwargs() -> None:
    """
    Test case 2: Multi-decorator with kwargs
    """
    @multi_decorator(uppercase_decorator, exclamation_decorator)
    def sample_function_kwargs(a: str, b: str) -> str:
        return f"{a} - {b}"
    
    result = sample_function_kwargs(a="hello", b="world")
    assert result == "HELLO - WORLD!"

def test_multi_decorator_with_mixed_args() -> None:
    """
    Test case 3: Multi-decorator with mixed args and kwargs
    """
    @multi_decorator(uppercase_decorator, exclamation_decorator)
    def sample_function_mixed(a: str, b: str, c: str) -> str:
        return f"{a} - {b} - {c}"
    
    result = sample_function_mixed("hello", b="world", c="python")
    assert result == "HELLO - WORLD - PYTHON!"

def test_multi_decorator_with_non_string() -> None:
    """
    Test case 4: Multi-decorator with non-string arguments
    """
    @multi_decorator(uppercase_decorator, exclamation_decorator)
    def sample_function_non_string(a: str, b: int) -> str:
        return f"{a} - {b}"
    
    result = sample_function_non_string("hello", 123)
    assert result == "HELLO - 123!"

def test_multi_decorator_with_variable_length_arguments() -> None:
    """
    Test case 5: Multi-decorator with variable length arguments (*args and **kwargs)
    """
    @multi_decorator(uppercase_decorator, exclamation_decorator)
    def sample_function_var_args(a: str, *args: str, **kwargs: str) -> str:
        return f"{a} - {args} - {kwargs}"
    
    result = sample_function_var_args("hello", "world", kwarg1="python", kwarg2="test")
    assert result == "HELLO - ('world',) - {'kwarg1': 'python', 'kwarg2': 'test'}!"

# Error tests

def test_multi_decorator_non_callable() -> None:
    """
    Test case 6: Non-callable decorator
    """
    with pytest.raises(TypeError, match="Decorator 123 is not callable"):
        @multi_decorator(123)
        def sample_function_invalid(a: str, b: str) -> str:
            return f"{a} - {b}"
