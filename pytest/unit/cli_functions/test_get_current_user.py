import pytest

try:
    import psutil
    from pyutils_collection.cli_functions.get_current_user import get_current_user
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None  # type: ignore
    get_current_user = None  # type: ignore

pytestmark = [
    pytest.mark.unit,
    pytest.mark.cli_functions,
    pytest.mark.skipif(not PSUTIL_AVAILABLE, reason="psutil not installed"),
]


def test_get_current_user_returns_string() -> None:
    """
    Test case 1: Test get_current_user returns a string.
    """
    user = get_current_user()
    assert isinstance(user, str)


def test_get_current_user_non_empty() -> None:
    """
    Test case 2: Test get_current_user returns non-empty string.
    """
    user = get_current_user()
    assert len(user) > 0


def test_get_current_user_consistency() -> None:
    """
    Test case 3: Test get_current_user returns consistent value.
    """
    user1 = get_current_user()
    user2 = get_current_user()
    assert user1 == user2


def test_get_current_user_no_whitespace_only() -> None:
    """
    Test case 4: Test username is not just whitespace.
    """
    user = get_current_user()
    assert user.strip() == user
    assert len(user.strip()) > 0


def test_get_current_user_valid_characters() -> None:
    """
    Test case 5: Test username contains valid characters.
    """
    user = get_current_user()
    # Username should contain alphanumeric or common special chars
    assert any(c.isalnum() or c in "_-." for c in user)


def test_get_current_user_multiple_calls() -> None:
    """
    Test case 6: Test multiple calls return same value.
    """
    users = [get_current_user() for _ in range(5)]
    assert all(u == users[0] for u in users)
