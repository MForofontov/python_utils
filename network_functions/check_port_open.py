import socket


def check_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Check if a TCP port is open on a host.

    Parameters
    ----------
    host : str
        Hostname or IP address to check.
    port : int
        Port number to check.
    timeout : float, optional
        Timeout in seconds (default: 2.0).

    Returns
    -------
    bool
        True if port is open, False otherwise.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If host is empty or port is invalid.

    Examples
    --------
    >>> check_port_open('localhost', 80)
    True
    """
    if not isinstance(host, str):
        raise TypeError(f"host must be a string, got {type(host).__name__}")
    if not host:
        raise ValueError("host cannot be empty")
    if not isinstance(port, int):
        raise TypeError(f"port must be an integer, got {type(port).__name__}")
    if not (0 < port < 65536):
        raise ValueError("port must be between 1 and 65535")
    if not isinstance(timeout, (int, float)):
        raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return True
        except Exception:
            return False

__all__ = ["check_port_open"]
