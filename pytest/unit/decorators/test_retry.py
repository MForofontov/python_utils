import pytest
import logging
from decorators.retry import retry

# Configure test_logger
test_logger = logging.getLogger('test_logger')
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
test_logger.addHandler(handler)

# Sample function to be decorated
@retry(max_retries=3, delay=0.1)
def sample_function() -> str:
    raise ValueError("Sample error")

def test_retry_success():
    """
    Test case 1: Function succeeds without retries
    """
    @retry(max_retries=3, delay=0.1)
    def success_function() -> str:
        return "Function executed"
    
    assert success_function() == "Function executed"

def test_retry_failure():
    """
    Test case 2: Function fails after maximum retries
    """
    with pytest.raises(ValueError, match="Sample error"):
        sample_function()

def test_retry_with_logger(caplog):
    """
    Test case 3: Logger functionality when retries occur
    """
    logger = logging.getLogger("retry_logger")
    logger.setLevel(logging.ERROR)
    
    @retry(max_retries=3, delay=0.1, logger=logger)
    def logged_function() -> str:
        raise ValueError("Sample error")
    
    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            logged_function()
        assert "Attempt 1 failed for logged_function: Sample error" in caplog.text
        assert "Attempt 2 failed for logged_function: Sample error" in caplog.text
        assert "Attempt 3 failed for logged_function: Sample error" in caplog.text

def test_retry_with_args():
    """
    Test case 4: Function with positional arguments
    """
    @retry(max_retries=3, delay=0.1)
    def function_with_args(a: int, b: int) -> int:
        return a + b
    
    assert function_with_args(1, 2) == 3

def test_retry_with_kwargs():
    """
    Test case 5: Function with keyword arguments
    """
    @retry(max_retries=3, delay=0.1)
    def function_with_kwargs(a: int, b: int = 0) -> int:
        return a + b
    
    assert function_with_kwargs(1, b=2) == 3

def test_retry_with_var_args():
    """
    Test case 6: Function with variable length arguments (*args and **kwargs)
    """
    @retry(max_retries=3, delay=0.1)
    def function_with_var_args(a: int, *args: str, **kwargs: float) -> str:
        return f"{a} - {args} - {kwargs}"
    
    assert function_with_var_args(1, "arg1", "arg2", kwarg1=1.0, kwarg2=2.0) == "1 - ('arg1', 'arg2') - {'kwarg1': 1.0, 'kwarg2': 2.0}"

def test_invalid_max_retries_type():
    """
    Test case 7: Invalid max_retries type
    """
    with pytest.raises(TypeError, match="max_retries must be an integer"):
        @retry(max_retries="three")
        def invalid_max_retries_function() -> None:
            pass

def test_invalid_delay_type():
    """
    Test case 8: Invalid delay type
    """
    with pytest.raises(TypeError, match="delay must be a float or an integer"):
        @retry(max_retries=3, delay="one")
        def invalid_delay_function() -> None:
            pass

def test_invalid_logger_type():
    """
    Test case 9: Invalid logger type
    """
    with pytest.raises(TypeError, match="logger must be an instance of logging.Logger or None"):
        @retry(max_retries=3, delay=0.1, logger="not_a_logger")
        def invalid_logger_function() -> None:
            pass