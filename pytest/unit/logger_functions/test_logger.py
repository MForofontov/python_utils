import pytest
import logging
from logger_functions.logger import get_logger, validate_logger


def test_get_logger_returns_logger_instance() -> None:
    """
    Test case 1: get_logger returns a Logger instance.
    """
    logger = get_logger("test_module")
    assert isinstance(logger, logging.Logger)


def test_get_logger_adds_null_handler() -> None:
    """
    Test case 2: get_logger adds NullHandler if no handlers exist.
    """
    logger = get_logger("test_module_null_handler")
    # Should have at least one handler, and one should be NullHandler
    assert any(isinstance(h, logging.NullHandler) for h in logger.handlers)


def test_validate_logger_accepts_logger() -> None:
    """
    Test case 3: validate_logger accepts Logger instance.
    """
    logger = get_logger("validate_logger_ok")
    validate_logger(logger)


def test_validate_logger_accepts_none_when_allowed() -> None:
    """
    Test case 4: validate_logger accepts None if allow_none=True.
    """
    validate_logger(None, allow_none=True)


def test_validate_logger_type_error_for_non_logger() -> None:
    """
    Test case 5: validate_logger raises TypeError for non-Logger when allow_none=False.
    """
    with pytest.raises(TypeError, match="logger must be an instance of logging.Logger"):
        validate_logger("not_a_logger", allow_none=False)


def test_validate_logger_custom_message() -> None:
    """
    Test case 6: validate_logger raises custom error message.
    """
    with pytest.raises(TypeError, match="Custom error"):
        validate_logger(123, allow_none=False, message="Custom error")
