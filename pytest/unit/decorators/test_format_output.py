import pytest
from decorators.format_output import format_output

@format_output("Result: {}")
def return_value(value):
    return value

@format_output("Sum: {}")
def add(a, b):
    return a + b

@format_output("Greeting: {}")
def greet(name):
    return f"Hello, {name}!"

@format_output("List: {}")
def return_list():
    return [1, 2, 3]

@format_output("Dict: {}")
def return_dict():
    return {"key": "value"}

@format_output("None: {}")
def return_none():
    return None

def test_format_output_basic():
    """
    Test case 1: Basic formatting functionality
    """
    # Test case 1: Basic formatting functionality
    assert return_value(5) == "Result: 5"
    assert return_value("test") == "Result: test"

def test_format_output_add():
    """
    Test case 2: Formatting the output of an addition function
    """
    # Test case 2: Formatting the output of an addition function
    assert add(1, 2) == "Sum: 3"
    assert add(-1, 1) == "Sum: 0"

def test_format_output_greet():
    """
    Test case 3: Formatting the output of a greeting function
    """
    # Test case 3: Formatting the output of a greeting function
    assert greet("Alice") == "Greeting: Hello, Alice!"
    assert greet("Bob") == "Greeting: Hello, Bob!"

def test_format_output_list():
    """
    Test case 4: Formatting the output of a function returning a list
    """
    # Test case 4: Formatting the output of a function returning a list
    assert return_list() == "List: [1, 2, 3]"

def test_format_output_dict():
    """
    Test case 5: Formatting the output of a function returning a dictionary
    """
    # Test case 5: Formatting the output of a function returning a dictionary
    assert return_dict() == "Dict: {'key': 'value'}"

def test_format_output_none():
    """
    Test case 6: Formatting the output of a function returning None
    """
    # Test case 6: Formatting the output of a function returning None
    assert return_none() == "None: None"

def test_format_output_with_custom_format():
    """
    Test case 7: Custom format string
    """
    # Test case 7: Custom format string
    @format_output("Custom: {}")
    def custom_format(value):
        return value

    assert custom_format("test") == "Custom: test"
    assert custom_format(123) == "Custom: 123"

def test_format_output_with_multiple_args():
    """
    Test case 8: Function with multiple arguments
    """
    # Test case 8: Function with multiple arguments
    @format_output("Result: {}")
    def multiple_args(a, b, c):
        return a + b + c

    assert multiple_args(1, 2, 3) == "Result: 6"
    assert multiple_args("a", "b", "c") == "Result: abc"

def test_format_output_with_kwargs():
    """
    Test case 9: Function with keyword arguments
    """
    # Test case 9: Function with keyword arguments
    @format_output("Result: {}")
    def with_kwargs(a, b=0):
        return a + b

    assert with_kwargs(1, b=2) == "Result: 3"
    assert with_kwargs(a=1, b=2) == "Result: 3"

def test_format_output_with_exception():
    """
    Test case 10: Function that raises an exception
    """
    # Test case 10: Function that raises an exception
    @format_output("Error: {}")
    def raise_exception():
        raise ValueError("An error occurred")

    with pytest.raises(ValueError, match="An error occurred"):
        raise_exception()