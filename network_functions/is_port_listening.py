import psutil


def is_port_listening(port: int) -> bool:
    """
    Check if a local port is being listened to.

    Parameters
    ----------
    port : int
        Port number to check.

    Returns
    -------
    bool
        True if port is being listened to, False otherwise.

    Examples
    --------
    >>> is_port_listening(80)
    True
    """
    if not isinstance(port, int):
        raise TypeError(f"port must be an integer, got {type(port).__name__}")
    if port < 0 or port > 65535:
        raise ValueError("port must be between 0 and 65535")

    for conn in psutil.net_connections():
        if conn.laddr and conn.laddr.port == port and conn.status == "LISTEN":
            return True
    return False


__all__ = ["is_port_listening"]
