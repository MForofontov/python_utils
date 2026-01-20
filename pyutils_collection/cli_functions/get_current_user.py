"""Current system user retrieval."""

import getpass


def get_current_user() -> str:
    """
    Get the username of the current user.

    Returns
    -------
    str
        Username of the current user.

    Examples
    --------
    >>> user = get_current_user()
    >>> isinstance(user, str)
    True
    >>> len(user) > 0
    True

    Notes
    -----
    This function uses getpass.getuser() which checks environment
    variables (LOGNAME, USER, LNAME, USERNAME) and falls back to
    pwd module on Unix systems.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    return getpass.getuser()


__all__ = ["get_current_user"]
