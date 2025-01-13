import pytest
import time
import logging
from decorators.rate_limit import rate_limit

# Configure test_logger
test_logger = logging.getLogger('test_logger')
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevel)s - %(message)s')
handler.setFormatter(formatter)
test_logger.addHandler(handler)

@rate_limit(2, 1, test_logger)
def limited_function() -> str:
    """
    A function that returns a simple message.
    """
    return "Function called"

def test_rate_limit_basic():
    """
    Test case 1: Basic functionality of rate_limit
    """
    assert limited_function() == "Function called"
    assert limited_function() == "Function called"
    with pytest.raises(Exception, match="Rate limit exceeded. Try again later."):
        limited_function()

def test_rate_limit_reset():
    """
    Test case 2: Rate limit reset after period
    """
    assert limited_function() == "Function called"
    assert limited_function() == "Function called"
    with pytest.raises(Exception, match="Rate limit exceeded. Try again later."):
        limited_function()
    time.sleep(1)
    assert limited_function() == "Function called"

def test_rate_limit_different_period():
    """
    Test case 3: Rate limit with different period
    """
    @rate_limit(2, 2, test_logger)
    def limited_function_2() -> str:
        return "Function called"
    
    assert limited_function_2() == "Function called"
    assert limited_function_2() == "Function called"
    with pytest.raises(Exception, match="Rate limit exceeded. Try again later."):
        limited_function_2()
    time.sleep(2)
    assert limited_function_2() == "Function called"

def test_rate_limit_non_integer_calls_per_period():
    """
    Test case 4: Non-integer calls_per_period
    """
    with pytest.raises(ValueError, match="max_calls must be a positive integer"):
        @rate_limit("two", 1, test_logger)
        def limited_function_invalid() -> str:
            return "Function called"

def test_rate_limit_non_integer_period():
    """
    Test case 5: Non-integer period
    """
    with pytest.raises(ValueError, match="period must be a positive integer"):
        @rate_limit(2, "one", test_logger)
        def limited_function_invalid() -> str:
            return "Function called"

def test_rate_limit_zero_calls_per_period():
    """
    Test case 6: Zero calls_per_period
    """
    with pytest.raises(ValueError, match="max_calls must be a positive integer"):
        @rate_limit(0, 1, test_logger)
        def limited_function_invalid() -> str:
            return "Function called"

def test_rate_limit_zero_period():
    """
    Test case 7: Zero period
    """
    with pytest.raises(ValueError, match="period must be a positive integer"):
        @rate_limit(2, 0, test_logger)
        def limited_function_invalid() -> str:
            return "Function called"

def test_rate_limit_logger():
    """
    Test case 8: Rate limit with logger
    """
    assert limited_function() == "Function called"
    assert limited_function() == "Function called"
    with pytest.raises(Exception, match="Rate limit exceeded. Try again later."):
        limited_function()
    assert "Rate limit exceeded" in log_handler.stream.getvalue()

if __name__ == "__main__":
    pytest.main()