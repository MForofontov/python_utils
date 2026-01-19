"""Check internet connectivity."""

import socket


def is_internet_available(timeout: float = 2.0) -> bool:
    """
    Check if the machine has internet connectivity.

    Parameters
    ----------
    timeout : float, optional
        Timeout in seconds (default: 2.0).

    Returns
    -------
    bool
        True if internet is available, False otherwise.

    Examples
    --------
    >>> is_internet_available()
    True
    """
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("8.8.8.8", 53))
        s.close()
        return True
    except Exception:
        return False


__all__ = ["is_internet_available"]
