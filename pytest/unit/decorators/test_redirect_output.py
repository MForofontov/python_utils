import pytest
import logging
import os
from decorators.redirect_output import redirect_output

# Configure test_logger
test_logger = logging.getLogger('test_logger')
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
test_logger.addHandler(handler)

# Sample function to be decorated
@redirect_output('output.txt')
def sample_function() -> None:
    print("Function executed")

def test_redirect_output_basic():
    """
    Test case 1: Basic functionality of redirecting output
    """
    sample_function()
    with open('output.txt', 'r') as f:
        assert f.read().strip() == "Function executed"

def test_redirect_output_with_args():
    """
    Test case 2: Function with positional arguments
    """
    @redirect_output('output_args.txt')
    def function_with_args(a: int, b: int) -> None:
        print(a + b)
    
    function_with_args(1, 2)
    with open('output_args.txt', 'r') as f:
        assert f.read().strip() == "3"

def test_redirect_output_with_kwargs():
    """
    Test case 3: Function with keyword arguments
    """
    @redirect_output('output_kwargs.txt')
    def function_with_kwargs(a: int, b: int = 0) -> None:
        print(a + b)
    
    function_with_kwargs(1, b=2)
    with open('output_kwargs.txt', 'r') as f:
        assert f.read().strip() == "3"

def test_redirect_output_with_var_args():
    """
    Test case 4: Function with variable length arguments (*args and **kwargs)
    """
    @redirect_output('output_var_args.txt')
    def function_with_var_args(a: int, *args: str, **kwargs: float) -> None:
        print(f"{a} - {args} - {kwargs}")
    
    function_with_var_args(1, "arg1", "arg2", kwarg1=1.0, kwarg2=2.0)
    with open('output_var_args.txt', 'r') as f:
        assert f.read().strip() == "1 - ('arg1', 'arg2') - {'kwarg1': 1.0, 'kwarg2': 2.0}"

def test_redirect_output_run_time_error():
    """
    Test case 5: Redirecting output when an error occurs
    """
    @redirect_output('invalid_path/output.txt')
    def error_function() -> None:
        raise RuntimeError("An error occurred")
    
    with pytest.raises(RuntimeError):
        error_function()

def test_redirect_output_run_time_error_with_logger(caplog):
    """
    Test case 6: Logger functionality when an error occurs
    """
    @redirect_output('invalid_path/output.txt', logger=test_logger)
    def error_function() -> None:
        raise RuntimeError("An error occurred")
    
    with caplog.at_level(logging.ERROR):
        with pytest.raises(RuntimeError):
            error_function()
        assert "Failed to redirect output" in caplog.text

def test_invalid_file_path():
    """
    Test case 7: Invalid file path parameter
    """
    with pytest.raises(TypeError, match="file_path must be a string"):
        @redirect_output(123)
        def invalid_file_path_function() -> None:
            pass

def test_invalid_file_path_with_logger(caplog):
    """
    Test case 8: Invalid file path parameter with logger
    """
    with pytest.raises(TypeError, match="file_path must be a string"):
        with caplog.at_level(logging.ERROR):
            @redirect_output(123, logger=test_logger)
            def invalid_file_path_with_logger_function() -> None:
                pass
        assert "file_path must be a string" in caplog.text

def test_invalid_logger_type():
    """
    Test case 9: Invalid logger type
    """
    with pytest.raises(TypeError, match="logger must be an instance of logging.Logger or None"):
        @redirect_output('output.txt', logger="not_a_logger")
        def invalid_logger_function() -> None:
            pass

