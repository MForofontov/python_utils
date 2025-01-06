import pytest
import logging
from typing import Any
from decorators.manipulate_output import manipulate_output

# Configure test_logger
test_logger = logging.getLogger('test_logger')
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
test_logger.addHandler(handler)

def test_uppercase_manipulation():
    """
    Test case 1: Uppercase manipulation
    """
    # Test case 1: Uppercase manipulation
    def uppercase(text: str) -> str:
        return text.upper()

    @manipulate_output(uppercase)
    def greet(name: str) -> str:
        return f"Hello, {name}"

    assert greet("world") == "HELLO, WORLD"

def test_reverse_manipulation():
    """
    Test case 2: Reverse manipulation
    """
    # Test case 2: Reverse manipulation
    def reverse(text: str) -> str:
        return text[::-1]

    @manipulate_output(reverse)
    def greet(name: str) -> str:
        return f"Hello, {name}"

    assert greet("world") == "dlrow ,olleH"

def test_non_string_output():
    """
    Test case 3: Non-string output manipulation
    """
    # Test case 3: Non-string output manipulation
    def to_string(text: Any) -> str:
        return str(text)

    @manipulate_output(to_string)
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == "3"

def test_convert_to_string():
    """
    Test case 4: Convert to string
    """
    # Test case 4: Convert to string
    def to_string(input: Any) -> str:
        return str(input)

    @manipulate_output(to_string)
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == '3'

def test_invalid_manipulation_func():
    """
    Test case 5: Invalid manipulation function, no logger
    """
    # Test case 5: Invalid manipulation function, no logger
    with pytest.raises(TypeError, match="manipulation_func must be a callable function."):
        @manipulate_output("not a function")
        def greet(name: str) -> str:
            return f"Hello, {name}"

def test_invalid_manipulation_func_with_logger(caplog):
    """
    Test case 6: Invalid manipulation function with logger
    """
    # Test case 6: Invalid manipulation function with logger
    with caplog.at_level(logging.ERROR):
        @manipulate_output("not a function", logger=test_logger)
        def greet(name: str) -> str:
            return f"Hello, {name}"
        assert "manipulation_func must be a callable function." in caplog.text

def test_logger_invalid_logger():
    """
    Test case 7: Invalid logger type
    """
    # Test case 7: Invalid logger type
    with pytest.raises(TypeError):
        @manipulate_output(lambda x: x, logger="not a logger")
        def greet(name: str) -> str:
            return f"Hello, {name}"
