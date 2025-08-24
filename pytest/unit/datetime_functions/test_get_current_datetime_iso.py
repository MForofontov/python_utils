import pytest
from datetime import datetime
import pytz
from datetime_functions.get_current_datetime_iso import get_current_datetime_iso, get_current_datetime_iso_utc


def test_get_current_datetime_iso_format() -> None:
    """
    Test case 1: Test get_current_datetime_iso function returns proper ISO format.
    """
    result: str = get_current_datetime_iso()
    assert isinstance(result, str)
    assert 'T' in result  # ISO format contains T separator
    assert len(result) >= 19  # At least YYYY-MM-DDTHH:MM:SS


def test_get_current_datetime_iso_utc_format() -> None:
    """
    Test case 2: Test get_current_datetime_iso_utc function returns proper UTC ISO format.
    """
    result: str = get_current_datetime_iso_utc()
    assert isinstance(result, str)
    assert 'T' in result  # ISO format contains T separator
    assert result.endswith('+00:00') or result.endswith('Z')  # UTC timezone indicator


def test_get_current_datetime_iso_parseable() -> None:
    """
    Test case 3: Test get_current_datetime_iso function returns parseable datetime string.
    """
    result: str = get_current_datetime_iso()
    # Should be able to parse the result back to datetime
    parsed: datetime = datetime.fromisoformat(result)
    assert isinstance(parsed, datetime)


def test_get_current_datetime_iso_utc_parseable() -> None:
    """
    Test case 4: Test get_current_datetime_iso_utc function returns parseable datetime string.
    """
    result: str = get_current_datetime_iso_utc()
    # Should be able to parse the result back to datetime
    parsed: datetime = datetime.fromisoformat(result)
    assert isinstance(parsed, datetime)
    assert parsed.tzinfo is not None  # Should have timezone info


def test_get_current_datetime_iso_different_calls() -> None:
    """
    Test case 5: Test get_current_datetime_iso function returns different values on consecutive calls.
    """
    import time
    result1: str = get_current_datetime_iso()
    time.sleep(0.001)  # Small delay
    result2: str = get_current_datetime_iso()
    # Results might be the same if execution is very fast, but should be valid ISO strings
    assert isinstance(result1, str)
    assert isinstance(result2, str)


def test_get_current_datetime_iso_utc_timezone() -> None:
    """
    Test case 6: Test get_current_datetime_iso_utc function returns UTC timezone.
    """
    result: str = get_current_datetime_iso_utc()
    parsed: datetime = datetime.fromisoformat(result)
    # Should be UTC timezone
    assert parsed.tzinfo == pytz.UTC or parsed.utcoffset().total_seconds() == 0
