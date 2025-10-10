import socket


def resolve_hostname(hostname: str) -> str:
    """
    Resolve a hostname to its IP address.

    Parameters
    ----------
    hostname : str
        Hostname to resolve.

    Returns
    -------
    str
        IP address as a string.

    Raises
    ------
    TypeError
        If hostname is not a string.
    ValueError
        If hostname is empty or cannot be resolved.

    Examples
    --------
    >>> resolve_hostname('example.com')
    '93.184.216.34'
    """
    if not isinstance(hostname, str):
        raise TypeError(f"hostname must be a string, got {type(hostname).__name__}")
    if not hostname:
        raise ValueError("hostname cannot be empty")
    try:
        return socket.gethostbyname(hostname)
    except Exception as exc:
        raise ValueError(f"Could not resolve hostname: {exc}") from exc


__all__ = ["resolve_hostname"]
