import pytest
import time
import logging
from decorators.rate_limit import rate_limit, RateLimitExceededException

# Configure test_logger
test_logger = logging.getLogger('test_logger')
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
test_logger.addHandler(handler)

@rate_limit(2, 1, test_logger)
def limited_function() -> str:
    """
    A function that returns a simple message.
    """
    return "Function called"

@rate_limit(2, 1, test_logger, exception_message="Custom rate limit exceeded message.")
def limited_function_custom_message() -> str:
    """
    A function that returns a simple message with a custom exception message.
    """
    return "Function called"

@rate_limit(2, 1, test_logger)
def limited_function_args_kwargs(*args: Any, **kwargs: Any) -> str:
    """
    A function that accepts *args and **kwargs and returns a formatted string.
    """
    return f"Function called with args: {args} and kwargs: {kwargs}"

@rate_limit(2, 1, test_logger)
def limited_function_raises_error(a: int, b: str) -> str:
    """
    A function that raises an error.
    """
    raise ValueError("An error occurred")

def test_rate_limit_basic(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 1: Basic functionality of rate_limit
    """
    with caplog.at_level(logging.WARNING):
        result = limited_function()
        assert result == "Function called"
        result = limited_function()
        assert result == "Function called"
        with pytest.raises(RateLimitExceededException, match="Rate limit exceeded for limited_function. Try again later."):
            limited_function()
        assert "Rate limit exceeded for limited_function. Try again later." in caplog.text

def test_rate_limit_reset(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 2: Rate limit reset after period
    """
    with caplog.at_level(logging.WARNING):
        result = limited_function()
        assert result == "Function called"
        result = limited_function()
        assert result == "Function called"
        with pytest.raises(RateLimitExceededException, match="Rate limit exceeded for limited_function. Try again later."):
            limited_function()
        assert "Rate limit exceeded for limited_function. Try again later." in caplog.text
        time.sleep(1)
        result = limited_function()
        assert result == "Function called"

def test_rate_limit_different_period(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 3: Rate limit with different period
    """
    @rate_limit(2, 2, test_logger)
    def limited_function_2() -> str:
        return "Function called"
    
    with caplog.at_level(logging.WARNING):
        result = limited_function_2()
        assert result == "Function called"
        result = limited_function_2()
        assert result == "Function called"
        with pytest.raises(RateLimitExceededException, match="Rate limit exceeded for limited_function_2. Try again later."):
            limited_function_2()
        assert "Rate limit exceeded for limited_function_2. Try again later." in caplog.text
        time.sleep(2)
        result = limited_function_2()
        assert result == "Function called"

def test_rate_limit_custom_message(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 4: Rate limit with custom exception message
    """
    with caplog.at_level(logging.WARNING):
        result = limited_function_custom_message()
        assert result == "Function called"
        result = limited_function_custom_message()
        assert result == "Function called"
        with pytest.raises(RateLimitExceededException, match="Custom rate limit exceeded message."):
            limited_function_custom_message()
        assert "Custom rate limit exceeded message." in caplog.text

def test_rate_limit_no_logger() -> None:
    """
    Test case 5: Rate limit without logger
    """
    @rate_limit(2, 1)
    def limited_function_no_logger() -> str:
        return "Function called"
    
    result = limited_function_no_logger()
    assert result == "Function called"
    result = limited_function_no_logger()
    assert result == "Function called"
    with pytest.raises(RateLimitExceededException, match="Rate limit exceeded for limited_function_no_logger. Try again later."):
        limited_function_no_logger()

def test_rate_limit_args_kwargs(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 6: Rate limit with *args and **kwargs
    """
    with caplog.at_level(logging.WARNING):
        result = limited_function_args_kwargs(1, 2, a="test", b="example")
        assert result == "Function called with args: (1, 2) and kwargs: {'a': 'test', 'b': 'example'}"
        result = limited_function_args_kwargs(3, 4, c="another", d="case")
        assert result == "Function called with args: (3, 4) and kwargs: {'c': 'another', 'd': 'case'}"
        with pytest.raises(RateLimitExceededException, match="Rate limit exceeded for limited_function_args_kwargs. Try again later."):
            limited_function_args_kwargs(5, 6, e="one", f="more")
        assert "Rate limit exceeded for limited_function_args_kwargs. Try again later." in caplog.text

def test_rate_limit_function_raises_error(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 7: Rate limit when the wrapped function raises an error
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="An error occurred"):
            limited_function_raises_error(1, "test")
        with pytest.raises(ValueError, match="An error occurred"):
            limited_function_raises_error(1, "test")
        with pytest.raises(RateLimitExceededException, match="Rate limit exceeded for limited_function_raises_error. Try again later."):
            limited_function_raises_error(1, "test")
        assert "Rate limit exceeded for limited_function_raises_error. Try again later." in caplog.text

def test_rate_limit_mixed_type_arguments(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 8: Rate limit with mixed type arguments
    """
    @rate_limit(2, 1, test_logger)
    def limited_function_mixed(a: int, b: str, c: float) -> str:
        return f"{a} - {b} - {c}"
    
    with caplog.at_level(logging.WARNING):
        result = limited_function_mixed(1, "test", 2.0)
        assert result == "1 - test - 2.0"
        result = limited_function_mixed(3, "example", 4.0)
        assert result == "3 - example - 4.0"
        with pytest.raises(RateLimitExceededException, match="Rate limit exceeded for limited_function_mixed. Try again later."):
            limited_function_mixed(5, "another", 6.0)
        assert "Rate limit exceeded for limited_function_mixed. Try again later." in caplog.text

def test_rate_limit_non_integer_calls_per_period(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 9: Non-integer calls_per_period
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="max_calls must be a positive integer"):
            @rate_limit("two", 1, test_logger)
            def limited_function_invalid() -> str:
                return "Function called"
        assert "max_calls must be a positive integer" in caplog.text

def test_rate_limit_non_integer_period(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 10: Non-integer period
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="period must be a positive integer"):
            @rate_limit(2, "one", test_logger)
            def limited_function_invalid() -> str:
                return "Function called"
        assert "period must be a positive integer" in caplog.text

def test_rate_limit_zero_calls_per_period(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 11: Zero calls_per_period
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="max_calls must be a positive integer"):
            @rate_limit(0, 1, test_logger)
            def limited_function_invalid() -> str:
                return "Function called"
        assert "max_calls must be a positive integer" in caplog.text

def test_rate_limit_zero_period(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test case 12: Zero period
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError, match="period must be a positive integer"):
            @rate_limit(2, 0, test_logger)
            def limited_function_invalid() -> str:
                return "Function called"
        assert "period must be a positive integer" in caplog.text

def test_rate_limit_non_integer_calls_per_period_no_logger() -> None:
    """
    Test case 13: Non-integer calls_per_period without logger
    """
    with pytest.raises(ValueError, match="max_calls must be a positive integer"):
        @rate_limit("two", 1)
        def limited_function_invalid() -> str:
            return "Function called"

def test_rate_limit_non_integer_period_no_logger() -> None:
    """
    Test case 14: Non-integer period without logger
    """
    with pytest.raises(ValueError, match="period must be a positive integer"):
        @rate_limit(2, "one")
        def limited_function_invalid() -> str:
            return "Function called"

def test_rate_limit_zero_calls_per_period_no_logger() -> None:
    """
    Test case 15: Zero calls_per_period without logger
    """
    with pytest.raises(ValueError, match="max_calls must be a positive integer"):
        @rate_limit(0, 1)
        def limited_function_invalid() -> str:
            return "Function called"

def test_rate_limit_zero_period_no_logger() -> None:
    """
    Test case 16: Zero period without logger
    """
    with pytest.raises(ValueError, match="period must be a positive integer"):
        @rate_limit(2, 0)
        def limited_function_invalid() -> str:
            return "Function called"
