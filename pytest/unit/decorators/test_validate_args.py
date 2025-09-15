import pytest
import logging
from decorators.validate_args import validate_args

# Configure test_logger
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
test_logger.addHandler(handler)


# Sample validation function
def is_positive(*args, **kwargs) -> bool:
    return all(arg > 0 for arg in args) and all(value > 0 for value in kwargs.values())


# Sample function to be decorated
@validate_args(is_positive)
def sample_function(a: int, b: int) -> int:
    return a + b


def test_validate_args_success():
    """
    Test case 1: Function executes successfully with valid arguments
    """
    result = sample_function(1, 2)
    assert result == 3


def test_validate_args_failure():
    """
    Test case 2: Function raises ValueError with invalid arguments
    """
    with pytest.raises(
        ValueError, match="Function sample_function arguments did not pass validation."
    ):
        sample_function(-1, 2)


def test_validate_args_with_logger(caplog):
    """
    Test case 3: Function raises ValueError and logs the validation failure message
    """

    @validate_args(is_positive, logger=test_logger)
    def function_with_logger(a: int, b: int) -> int:
        return a + b

    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            function_with_logger(-1, 2)
        assert (
            "Function function_with_logger arguments did not pass validation."
            in caplog.text
        )


def test_validate_args_with_kwargs():
    """
    Test case 4: Function with keyword arguments
    """

    @validate_args(is_positive)
    def function_with_kwargs(a: int, b: int = 0) -> int:
        return a + b

    result = function_with_kwargs(1, b=2)
    assert result == 3


def test_validate_args_with_var_args():
    """
    Test case 5: Function with variable length arguments (*args and **kwargs)
    """

    @validate_args(is_positive)
    def function_with_var_args(a: int, *args: int, **kwargs: int) -> str:
        return f"{a} - {args} - {kwargs}"

    result = function_with_var_args(1, 2, 3, kwarg1=4, kwarg2=5)
    assert result == "1 - (2, 3) - {'kwarg1': 4, 'kwarg2': 5}"


def test_invalid_validation_func():
    """
    Test case 6: Invalid validation function type
    """
    with pytest.raises(TypeError, match="validation_func must be callable"):

        @validate_args("not_a_function")
        def invalid_validation_func_function() -> None:
            pass


def test_invalid_logger_type():
    """
    Test case 7: Invalid logger type
    """
    with pytest.raises(
        TypeError, match="logger must be an instance of logging.Logger or None"
    ):

        @validate_args(is_positive, logger="not_a_logger")
        def invalid_logger_function() -> None:
            pass
