"""
Module for getting the system hostname.
"""

import socket


def get_hostname() -> str:
    """
    Get the hostname of the current system.

    Returns
    -------
    str
        Hostname of the system.

    Examples
    --------
    >>> hostname = get_hostname()
    >>> isinstance(hostname, str)
    True
    >>> len(hostname) > 0
    True

    Notes
    -----
    Returns the fully qualified domain name (FQDN) when possible.

    Complexity
    ----------
    Time: O(1), Space: O(1)
    """
    return socket.gethostname()


__all__ = ['get_hostname']
