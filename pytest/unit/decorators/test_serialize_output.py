import pytest
import logging
import json
from decorators.serialize_output import serialize_output

# Configure test_logger
test_logger = logging.getLogger("test_logger")
test_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
test_logger.addHandler(handler)


# Sample function to be decorated
@serialize_output("json")
def sample_function() -> dict:
    return {"key": "value"}


def test_serialize_output_success():
    """
    Test case 1: Function output is serialized to JSON
    """
    assert sample_function() == json.dumps({"key": "value"})


def test_serialize_output_with_args():
    """
    Test case 2: Function with positional arguments
    """

    @serialize_output("json")
    def function_with_args(a: int, b: int) -> dict:
        return {"sum": a + b}

    assert function_with_args(1, 2) == json.dumps({"sum": 3})


def test_serialize_output_with_kwargs():
    """
    Test case 3: Function with keyword arguments
    """

    @serialize_output("json")
    def function_with_kwargs(a: int, b: int = 0) -> dict:
        return {"sum": a + b}

    assert function_with_kwargs(1, b=2) == json.dumps({"sum": 3})


def test_serialize_output_with_var_args():
    """
    Test case 4: Function with variable length arguments (*args and **kwargs)
    """

    @serialize_output("json")
    def function_with_var_args(a: int, *args: str, **kwargs: float) -> dict:
        return {"args": args, "kwargs": kwargs}

    assert function_with_var_args(
        1, "arg1", "arg2", kwarg1=1.0, kwarg2=2.0
    ) == json.dumps(
        {"args": ("arg1", "arg2"), "kwargs": {"kwarg1": 1.0, "kwarg2": 2.0}}
    )


def test_serialize_output_with_logger(caplog):
    """
    Test case 5: Logger functionality when an error occurs
    """
    logger = logging.getLogger("serialize_output_logger")
    logger.setLevel(logging.ERROR)

    @serialize_output("json", logger=logger)
    def error_function() -> dict:
        raise ValueError("Sample error")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(ValueError):
            error_function()
        assert "Error serializing output in error_function: Sample error" in caplog.text


def test_serialize_invalid_logger():
    """
    Test case 6: Invalid logger
    """

    @serialize_output("json", logger="invalid_logger")
    def invalid_logger_function() -> None:
        pass


def test_invalid_format_type():
    """
    Test case 7: Invalid format type
    """
    with pytest.raises(TypeError, match="format must be a string."):

        @serialize_output(123)
        def invalid_format_type_function() -> None:
            pass


def test_invalid_format_type_with_logger(caplog):
    """
    Test case 8: Invalid format type with logger
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(TypeError, match="format must be a string."):

            @serialize_output(123, logger=test_logger)
            def invalid_format_type_with_logger_function() -> None:
                pass

        assert (
            "Type error in serialize_output decorator: format must be a string."
            in caplog.text
        )


def test_invalid_format():
    """
    Test case 6: Invalid format
    """
    with pytest.raises(
        ValueError, match="Unsupported format. Currently, only 'json' is supported."
    ):

        @serialize_output("xml")
        def invalid_format_function() -> None:
            pass


def test_invalid_format_with_logger(caplog):
    """
    Test case 7: Invalid format with logger
    """
    with caplog.at_level(logging.ERROR):
        with pytest.raises(
            ValueError, match="Unsupported format. Currently, only 'json' is supported."
        ):

            @serialize_output("xml", logger=test_logger)
            def invalid_format_with_logger_function() -> None:
                pass

        assert (
            "Value error in serialize_output decorator: Unsupported format."
            in caplog.text
        )
