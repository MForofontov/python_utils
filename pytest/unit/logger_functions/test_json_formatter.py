import pytest

pytestmark = [pytest.mark.unit, pytest.mark.logger_functions]
import json
import logging
import sys
from datetime import datetime

from python_utils.logger_functions.json_formatter import json_formatter


def test_json_formatter_basic() -> None:
    """Test case 1: Test basic JSON formatter functionality."""
    formatter = json_formatter()
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

    # Parse the JSON
    parsed = json.loads(result)

    # Check required fields
    assert parsed["level"] == "INFO"
    assert parsed["logger"] == "test_logger"
    assert parsed["message"] == "Test message"
    assert parsed["module"] == "test"
    assert parsed["function"] is None
    assert parsed["line"] == 10
    assert "timestamp" in parsed
    assert isinstance(parsed["process"], int)
    assert isinstance(parsed["thread"], int)


def test_json_formatter_with_extra() -> None:
    """Test case 2: Test JSON formatter with extra fields."""
    formatter = json_formatter(include_extra=True)

    record = logging.LogRecord(
        name="test_logger",
        level=logging.DEBUG,
        pathname="test.py",
        lineno=5,
        msg="Debug message",
        args=(),
        exc_info=None,
    )

    # Add extra field
    record.custom_field = "custom_value"

    result = formatter.format(record)
    parsed = json.loads(result)

    assert parsed["custom_field"] == "custom_value"


def test_json_formatter_pretty_print() -> None:
    """Test case 3: Test JSON formatter with pretty printing."""
    formatter = json_formatter(pretty_print=True)

    record = logging.LogRecord(
        name="test_logger",
        level=logging.WARNING,
        pathname="test.py",
        lineno=15,
        msg="Warning message",
        args=(),
        exc_info=None,
    )

    result = formatter.format(record)

    # Should contain newlines for pretty printing
    assert "\n" in result
    assert "  " in result  # Indentation

    # Should still be valid JSON
    parsed = json.loads(result)
    assert parsed["level"] == "WARNING"
    assert parsed["message"] == "Warning message"


def test_json_formatter_timestamp_format() -> None:
    """Test case 4: Test that timestamp is in ISO format."""
    formatter = json_formatter()

    record = logging.LogRecord(
        name="test_logger",
        level=logging.ERROR,
        pathname="test.py",
        lineno=20,
        msg="Error message",
        args=(),
        exc_info=None,
    )

    result = formatter.format(record)
    parsed = json.loads(result)

    # Should be able to parse as ISO format
    timestamp = parsed["timestamp"]
    datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def test_json_formatter_exception_handling() -> None:
    """Test case 5: Test JSON formatter with exception information."""
    formatter = json_formatter()

    try:
        raise ValueError("Test exception")
    except ValueError:
        exc_info = sys.exc_info()

    record = logging.LogRecord(
        name="test_logger",
        level=logging.CRITICAL,
        pathname="test.py",
        lineno=25,
        msg="Exception occurred",
        args=(),
        exc_info=exc_info,
    )

    result = formatter.format(record)
    parsed = json.loads(result)

    assert "exception" in parsed
    assert "ValueError" in parsed["exception"]
    assert "Test exception" in parsed["exception"]


def test_json_formatter_no_extra_fields() -> None:
    """Test case 6: Test JSON formatter without extra fields."""
    formatter = json_formatter(include_extra=False)

    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test.py",
        lineno=30,
        msg="No extra message",
        args=(),
        exc_info=None,
    )

    # Add extra field that should be ignored
    record.ignored_field = "should_not_appear"

    result = formatter.format(record)
    parsed = json.loads(result)

    assert "ignored_field" not in parsed
    assert parsed["level"] == "INFO"
    assert parsed["message"] == "No extra message"
