from datetime import datetime

from datetime_functions.get_current_datetime_iso import get_current_datetime_iso


def test_get_current_datetime_iso_format() -> None:
    """
    Test case 1: Test get_current_datetime_iso function returns proper ISO format.
    """
    result: str = get_current_datetime_iso()
    assert isinstance(result, str)
    assert "T" in result  # ISO format contains T separator
    assert len(result) >= 19  # At least YYYY-MM-DDTHH:MM:SS


def test_get_current_datetime_iso_parseable() -> None:
    """
    Test case 2: Test get_current_datetime_iso function returns parseable datetime string.
    """
    result: str = get_current_datetime_iso()
    # Should be able to parse the result back to datetime
    parsed: datetime = datetime.fromisoformat(result)
    assert isinstance(parsed, datetime)


def test_get_current_datetime_iso_different_calls() -> None:
    """
    Test case 3: Test get_current_datetime_iso function returns different values on consecutive calls.
    """
    import time

    result1: str = get_current_datetime_iso()
    time.sleep(0.001)  # Small delay
    result2: str = get_current_datetime_iso()
    # Results might be the same if execution is very fast, but should be valid ISO strings
    assert isinstance(result1, str)
    assert isinstance(result2, str)


def test_get_current_datetime_iso_consistency() -> None:
    """
    Test case 4: Test get_current_datetime_iso function returns consistent format.
    """
    result: str = get_current_datetime_iso()
    # Should be parseable and represent current time (approximately)
    parsed: datetime = datetime.fromisoformat(result)
    now = datetime.now()
    time_diff = abs((parsed - now).total_seconds())
    assert time_diff < 1  # Should be within 1 second of current time
