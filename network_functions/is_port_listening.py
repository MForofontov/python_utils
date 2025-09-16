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
    for conn in psutil.net_connections():
        if conn.laddr and conn.laddr.port == port and conn.status == 'LISTEN':
            return True
    return False

__all__ = ["is_port_listening"]
