import pytest
from typing import Callable
from decorators.multi_decorator import multi_decorator

def uppercase_decorator(func: Callable[[str], str]) -> Callable[[str], str]:
    """
    A decorator that converts the result of a function to uppercase.
    """
    def wrapper(text: str) -> str:
        return func(text).upper()
    return wrapper

def exclamation_decorator(func: Callable[[str], str]) -> Callable[[str], str]:
    """
    A decorator that adds an exclamation mark to the result of a function.
    """
    def wrapper(text: str) -> str:
        return func(text) + "!"
    return wrapper

def reverse_decorator(func: Callable[[str], str]) -> Callable[[str], str]:
    """
    A decorator that reverses the result of a function.
    """
    def wrapper(text: str) -> str:
        return func(text)[::-1]
    return wrapper

@multi_decorator(uppercase_decorator, exclamation_decorator)
def greet(name: str) -> str:
    """
    A function that returns a greeting message.
    """
    return f"Hello, {name}"

def test_multi_decorator_basic():
    """
    Test case 1: Basic functionality of multi_decorator
    """
    # Test case 1: Basic functionality of multi_decorator
    assert greet("world") == "HELLO, WORLD!"

def test_multi_decorator_order():
    """
    Test case 2: Order of decorators in multi_decorator
    """
    # Test case 2: Order of decorators in multi_decorator
    @multi_decorator(exclamation_decorator, uppercase_decorator)
    def greet(name: str) -> str:
        return f"Hello, {name}"
    
    assert greet("world") == "HELLO, WORLD!"

def test_multi_decorator_single():
    """
    Test case 3: Single decorator in multi_decorator
    """
    # Test case 3: Single decorator in multi_decorator
    @multi_decorator(uppercase_decorator)
    def greet(name: str) -> str:
        return f"Hello, {name}"
    
    assert greet("world") == "HELLO, WORLD"

def test_multi_decorator_no_decorator():
    """
    Test case 4: No decorator in multi_decorator
    """
    # Test case 4: No decorator in multi_decorator
    @multi_decorator()
    def greet(name: str) -> str:
        return f"Hello, {name}"
    
    assert greet("world") == "Hello, world"

def test_multi_decorator_multiple():
    """
    Test case 5: Multiple decorators in multi_decorator
    """
    # Test case 5: Multiple decorators in multi_decorator
    @multi_decorator(uppercase_decorator, exclamation_decorator, reverse_decorator)
    def greet(name: str) -> str:
        return f"Hello, {name}"
    
    assert greet("world") == "!DLROW ,OLLEH"

def test_multi_decorator_empty_string():
    """
    Test case 6: Empty string input
    """
    # Test case 6: Empty string input
    @multi_decorator(uppercase_decorator, exclamation_decorator)
    def greet(name: str) -> str:
        return f"Hello, {name}"
    
    assert greet("") == "HELLO, !"

def test_multi_decorator_special_characters():
    """
    Test case 7: Special characters in input
    """
    # Test case 7: Special characters in input
    @multi_decorator(uppercase_decorator, exclamation_decorator)
    def greet(name: str) -> str:
        return f"Hello, {name}"
    
    assert greet("world!@#") == "HELLO, WORLD!@#!"

def test_multi_decorator_non_callable():
    """
    Test case 8: Non-callable decorator in multi_decorator
    """
    # Test case 8: Non-callable decorator in multi_decorator
    with pytest.raises(TypeError, match="Decorator not a decorator is not callable"):
        @multi_decorator("not a decorator")
        def greet(name: str) -> str:
            return f"Hello, {name}"