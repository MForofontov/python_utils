import pytest
from cli_functions.get_hostname import get_hostname


def test_get_hostname_case_1_returns_string() -> None:
    """
    Test case 1: Test get_hostname returns a string.
    """
    hostname = get_hostname()
    assert isinstance(hostname, str)


def test_get_hostname_case_2_non_empty() -> None:
    """
    Test case 2: Test get_hostname returns non-empty string.
    """
    hostname = get_hostname()
    assert len(hostname) > 0


def test_get_hostname_case_3_consistency() -> None:
    """
    Test case 3: Test get_hostname returns consistent value.
    """
    hostname1 = get_hostname()
    hostname2 = get_hostname()
    assert hostname1 == hostname2


def test_get_hostname_case_4_valid_characters() -> None:
    """
    Test case 4: Test hostname contains valid characters.
    """
    hostname = get_hostname()
    # Hostname should contain alphanumeric, dots, or hyphens
    assert all(c.isalnum() or c in '.-_' for c in hostname)


def test_get_hostname_case_5_no_spaces() -> None:
    """
    Test case 5: Test hostname does not contain spaces.
    """
    hostname = get_hostname()
    assert ' ' not in hostname


def test_get_hostname_case_6_multiple_calls() -> None:
    """
    Test case 6: Test multiple calls return same value.
    """
    hostnames = [get_hostname() for _ in range(5)]
    assert all(h == hostnames[0] for h in hostnames)
