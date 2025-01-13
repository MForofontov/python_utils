import pytest
from typing import Any
from decorators.normalize_input import normalize_input

def to_lowercase(value: Any) -> Any:
    """
    A normalization function that converts strings to lowercase.
    """
    if isinstance(value, str):
        return value.lower()
    return value

@normalize_input(to_lowercase)
def greet(name: str) -> str:
    """
    A function that returns a greeting message.
    """
    return f"Hello, {name}"

def test_normalize_input_basic():
    """
    Test case 1: Basic functionality of normalize_input
    """
    # Test case 1: Basic functionality of normalize_input
    assert greet("WORLD") == "Hello, world"

def test_normalize_input_with_kwargs():
    """
    Test case 2: normalize_input with keyword arguments
    """
    # Test case 2: normalize_input with keyword arguments
    @normalize_input(to_lowercase)
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}"
    
    assert greet(name="WORLD") == "Hello, world"
    assert greet(name="WORLD", greeting="Hi") == "Hi, world"

def test_normalize_input_mixed_args():
    """
    Test case 3: normalize_input with mixed positional and keyword arguments
    """
    # Test case 3: normalize_input with mixed positional and keyword arguments
    @normalize_input(to_lowercase)
    def greet(greeting: str, name: str) -> str:
        return f"{greeting}, {name}"
    
    assert greet("HI", "WORLD") == "hi, world"
    assert greet(greeting="HI", name="WORLD") == "hi, world"

def test_normalize_input_non_string():
    """
    Test case 4: normalize_input with non-string arguments
    """
    # Test case 4: normalize_input with non-string arguments
    @normalize_input(to_lowercase)
    def add(a: int, b: int) -> int:
        return a + b
    
    assert add(1, 2) == 3

def test_normalize_input_empty_string():
    """
    Test case 5: normalize_input with empty string
    """
    # Test case 5: normalize_input with empty string
    assert greet("") == "Hello, "

def test_normalize_input_special_characters():
    """
    Test case 6: normalize_input with special characters
    """
    # Test case 6: normalize_input with special characters
    assert greet("WORLD!@#") == "Hello, world!@#"

def test_normalize_input_non_callable():
    """
    Test case 7: Non-callable normalization function
    """
    # Test case 7: Non-callable normalization function
    with pytest.raises(TypeError, match="Normalizer not a function is not callable"):
        @normalize_input("not a function")
        def greet(name: str) -> str:
            return f"Hello, {name}"
