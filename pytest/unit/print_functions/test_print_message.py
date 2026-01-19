from unittest.mock import MagicMock

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.print_functions]
from print_functions.print_message import print_message


def test_print_message_info(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Test case 1: Print info message and check output format.
    """
    print_message("Hello World", message_type="info")
    out = capsys.readouterr().out
    assert "[INFO]" in out and "Hello World" in out


def test_print_message_warning(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Test case 2: Print warning message and check output format.
    """
    print_message("Warning!", message_type="warning")
    out = capsys.readouterr().out
    assert "[WARNING]" in out and "Warning!" in out


def test_print_message_error(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Test case 3: Print error message and check output format.
    """
    print_message("Error!", message_type="error")
    out = capsys.readouterr().out
    assert "[ERROR]" in out and "Error!" in out


def test_print_message_debug(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Test case 4: Print debug message and check output format.
    """
    print_message("Debug!", message_type="debug")
    out = capsys.readouterr().out
    assert "[DEBUG]" in out and "Debug!" in out


def test_print_message_none_type(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Test case 5: Print message with None type (no prefix).
    """
    print_message("Just a message", message_type=None)
    out = capsys.readouterr().out
    assert out.strip() == "Just a message"


def test_print_message_custom_type(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Test case 6: Print message with custom type (no prefix).
    """
    print_message("Custom", message_type="custom")
    out = capsys.readouterr().out
    assert "Custom" in out and "- Custom" in out


def test_print_message_with_logger() -> None:
    """
    Test case 7: Print message with custom logger logs to logger.
    """
    mock_logger = MagicMock()
    print_message("Log this", message_type="info", logger=mock_logger)
    mock_logger.info.assert_called_with("Log this")
