import pytest
import logging
import time
from decorators.timeout import timeout, TimeoutException

# Configure test_logger
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
test_logger.addHandler(handler)


# Sample function to be decorated
@timeout(seconds=2)
def sample_function() -> str:
    time.sleep(1)
    return "Function executed"


def test_timeout_success():
    """
    Test case 1: Function executes successfully within the timeout period
    """
    result = sample_function()
    assert result == "Function executed"


def test_timeout_exceeded():
    """
    Test case 2: Function exceeds the timeout period and raises TimeoutException
    """

    @timeout(seconds=1)
    def long_running_function() -> None:
        time.sleep(2)

    with pytest.raises(
        TimeoutException,
        match="Function long_running_function timed out after 1 seconds",
    ):
        long_running_function()


def test_timeout_with_logger(caplog):
    """
    Test case 3: Function exceeds the timeout period and logs the timeout message
    """

    @timeout(seconds=1, logger=test_logger)
    def long_running_function_with_logger() -> None:
        time.sleep(2)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(TimeoutException):
            long_running_function_with_logger()
        assert (
            "Function long_running_function_with_logger timed out after 1 seconds"
            in caplog.text
        )


def test_timeout_with_args():
    """
    Test case 4: Function with positional arguments
    """

    @timeout(seconds=2)
    def function_with_args(a: int, b: int) -> int:
        time.sleep(1)
        return a + b

    result = function_with_args(1, 2)
    assert result == 3


def test_timeout_with_kwargs():
    """
    Test case 5: Function with keyword arguments
    """

    @timeout(seconds=2)
    def function_with_kwargs(a: int, b: int = 0) -> int:
        time.sleep(1)
        return a + b

    result = function_with_kwargs(1, b=2)
    assert result == 3


def test_timeout_with_var_args():
    """
    Test case 6: Function with variable length arguments (*args and **kwargs)
    """

    @timeout(seconds=2)
    def function_with_var_args(a: int, *args: str, **kwargs: float) -> str:
        time.sleep(1)
        return f"{a} - {args} - {kwargs}"

    result = function_with_var_args(1, "arg1", "arg2", kwarg1=1.0, kwarg2=2.0)
    assert result == "1 - ('arg1', 'arg2') - {'kwarg1': 1.0, 'kwarg2': 2.0}"


def test_invalid_logger_type():
    """
    Test case 7: Invalid logger type
    """
    with pytest.raises(
        TypeError, match="logger must be an instance of logging.Logger or None"
    ):

        @timeout(seconds=2, logger="not_a_logger")
        def invalid_logger_function() -> None:
            pass


def test_invalid_seconds_type():
    """
    Test case 8: Invalid seconds type
    """
    with pytest.raises(TypeError, match="seconds must be a positive integer"):

        @timeout(seconds="two")
        def invalid_seconds_function() -> None:
            pass


def test_negative_seconds_value():
    """
    Test case 9: Negative seconds value
    """
    with pytest.raises(TypeError, match="seconds must be a positive integer"):

        @timeout(seconds=-1)
        def negative_seconds_function() -> None:
            pass
