import pytest
import logging
from decorators.log_function_calls import log_function_calls

# Configure test_logger
test_logger = logging.getLogger('test_logger')
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
test_logger.addHandler(handler)

@log_function_calls(logger=test_logger)
def add(a, b):
    return a + b

@log_function_calls(logger=test_logger)
def greet(name):
    return f"Hello, {name}!"

@log_function_calls(logger=test_logger)
def raise_value_error():
    raise ValueError("This is a ValueError")

@log_function_calls(logger=test_logger)
def return_value(value):
    return value

def test_log_function_calls_add(caplog):
    """
    Test case 1: Logging function calls for add function
    """
    # Test case 1: Logging function calls for add function
    with caplog.at_level(logging.DEBUG):
        result = add(1, 2)
        assert result == 3
        assert "Calling add with args: (1, 2) and kwargs: {}" in caplog.text
        assert "add returned: 3" in caplog.text

def test_log_function_calls_greet(caplog):
    """
    Test case 2: Logging function calls for greet function
    """
    # Test case 2: Logging function calls for greet function
    with caplog.at_level(logging.DEBUG):
        result = greet("Alice")
        assert result == "Hello, Alice!"
        assert "Calling greet with args: ('Alice',) and kwargs: {}" in caplog.text
        assert "greet returned: Hello, Alice!" in caplog.text

def test_log_function_calls_raise_value_error(caplog):
    """
    Test case 3: Logging function calls for function that raises ValueError
    """
    # Test case 3: Logging function calls for function that raises ValueError
    with caplog.at_level(logging.DEBUG):
        with pytest.raises(ValueError, match="This is a ValueError"):
            raise_value_error()
        assert "Calling raise_value_error with args: () and kwargs: {}" in caplog.text
        assert "raise_value_error raised an exception: This is a ValueError" in caplog.text

def test_log_function_calls_return_value(caplog):
    """
    Test case 4: Logging function calls for return_value function
    """
    # Test case 4: Logging function calls for return_value function
    with caplog.at_level(logging.DEBUG):
        result = return_value(5)
        assert result == 5
        assert "Calling return_value with args: (5,) and kwargs: {}" in caplog.text
        assert "return_value returned: 5" in caplog.text

def test_log_function_calls_with_kwargs(caplog):
    """
    Test case 5: Logging function calls with keyword arguments
    """
    # Test case 5: Logging function calls with keyword arguments
    @log_function_calls(logger=test_logger)
    def with_kwargs(a, b=0):
        return a + b

    with caplog.at_level(logging.DEBUG):
        result = with_kwargs(1, b=2)
        assert result == 3
        assert "Calling with_kwargs with args: (1,) and kwargs: {'b': 2}" in caplog.text
        assert "with_kwargs returned: 3" in caplog.text

def test_log_function_calls_with_multiple_args(caplog):
    """
    Test case 6: Logging function calls with multiple arguments
    """
    # Test case 6: Logging function calls with multiple arguments
    @log_function_calls(logger=test_logger)
    def multiple_args(a, b, c):
        return a + b + c

    with caplog.at_level(logging.DEBUG):
        result = multiple_args(1, 2, 3)
        assert result == 6
        assert "Calling multiple_args with args: (1, 2, 3) and kwargs: {}" in caplog.text
        assert "multiple_args returned: 6" in caplog.text

def test_log_function_calls_with_custom_exception(caplog):
    """
    Test case 7: Logging function calls for function that raises a custom exception
    """
    # Test case 7: Logging function calls for function that raises a custom exception
    class CustomException(Exception):
        pass

    @log_function_calls(logger=test_logger)
    def raise_custom_exception():
        raise CustomException("This is a CustomException")

    with caplog.at_level(logging.DEBUG):
        with pytest.raises(CustomException, match="This is a CustomException"):
            raise_custom_exception()
        assert "Calling raise_custom_exception with args: () and kwargs: {}" in caplog.text
        assert "raise_custom_exception raised an exception: This is a CustomException" in caplog.text

def test_log_function_invalid_logger():
    """
    Test case 8: Invalid logger (not an instance of logging.Logger or None)
    """
    # Test case 8: Invalid logger (not an instance of logging.Logger or None)
    with pytest.raises(TypeError, match="logger must be an instance of logging.Logger or None"):
        @log_function_calls(logger="not_a_logger")
        def example_function_invalid_logger(a, b):
            return f"Result: {a + b}"