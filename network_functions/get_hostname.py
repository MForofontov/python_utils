import socket


def get_hostname() -> str:
    """
    Get the local machine's hostname.

    Returns
    -------
    str
        Hostname as a string.

    Examples
    --------
    >>> get_hostname()
    'my-computer.local'
    """
    return socket.gethostname()

__all__ = ["get_hostname"]
