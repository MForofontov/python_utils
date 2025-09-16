import logging
from unittest.mock import patch

from logging_debugging.colored_formatter import colored_formatter


def test_colored_formatter_basic():
    """Test basic colored formatter functionality."""
    formatter = colored_formatter()
    assert isinstance(formatter, logging.Formatter)

    # Create a test log record
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    # Format the record
    result = formatter.format(record)

    # Should contain the message
    assert "Test message" in result
    assert "INFO" in result


def test_colored_formatter_colors():
    """Test that colored formatter adds ANSI color codes."""
    formatter = colored_formatter(use_color=True)

    # Test different log levels
    test_cases = [
        (logging.DEBUG, "\033[36m"),  # Cyan
        (logging.INFO, "\033[32m"),  # Green
        (logging.WARNING, "\033[33m"),  # Yellow
        (logging.ERROR, "\033[31m"),  # Red
        (logging.CRITICAL, "\033[35m"),  # Magenta
    ]

    for level, expected_color in test_cases:
        record = logging.LogRecord(
            name="test_logger",
            level=level,
            pathname="test.py",
            lineno=10,
            msg=f"Level {level} message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)

        # Should contain color codes and reset
        assert expected_color in result
        assert "\033[0m" in result  # Reset code


def test_colored_formatter_no_color():
    """Test colored formatter with colors disabled."""
    formatter = colored_formatter(use_color=False)

    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    result = formatter.format(record)

    # Should not contain color codes
    assert "\033[" not in result
    assert "Test message" in result


@patch("sys.stdout.isatty")
def test_colored_formatter_auto_detect_color(mock_isatty):
    """Test automatic color detection."""
    # Test when TTY is available
    mock_isatty.return_value = True
    formatter = colored_formatter(use_color=True)
    assert formatter.use_color is True

    # Test when TTY is not available
    mock_isatty.return_value = False
    formatter = colored_formatter(use_color=True)
    assert formatter.use_color is False


def test_colored_formatter_custom_format():
    """Test colored formatter with custom format string."""
    custom_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = colored_formatter(fmt=custom_fmt, use_color=False)

    record = logging.LogRecord(
        name="test_logger",
        level=logging.WARNING,
        pathname="test.py",
        lineno=10,
        msg="Custom format message",
        args=(),
        exc_info=None,
    )

    result = formatter.format(record)

    # Should contain all expected fields
    assert "test_logger" in result
    assert "WARNING" in result
    assert "Custom format message" in result


def test_colored_formatter_unknown_level():
    """Test colored formatter with unknown log level."""
    formatter = colored_formatter(use_color=True)

    # Create record with custom level
    record = logging.LogRecord(
        name="test_logger",
        level=60,  # Custom level
        pathname="test.py",
        lineno=10,
        msg="Unknown level message",
        args=(),
        exc_info=None,
    )
    record.levelname = "UNKNOWN"

    result = formatter.format(record)

    # Should not have color codes for unknown level
    assert "\033[" not in result or not any(
        color in result for color in ["[31m", "[32m", "[33m", "[35m", "[36m"]
    )
    assert "Unknown level message" in result


def test_colored_formatter_with_args():
    """Test colored formatter with message formatting arguments."""
    formatter = colored_formatter(use_color=False)

    record = logging.LogRecord(
        name="test_logger",
        level=logging.ERROR,
        pathname="test.py",
        lineno=10,
        msg="Error: %s occurred at %s",
        args=("ValueError", "line 42"),
        exc_info=None,
    )

    result = formatter.format(record)

    # Should have formatted message
    assert "Error: ValueError occurred at line 42" in result
