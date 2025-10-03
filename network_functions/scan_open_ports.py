import socket


def scan_open_ports(host: str, start_port: int = 1, end_port: int = 1024, timeout: float = 0.5) -> list[int]:
    """
    Scan a range of ports on a host and return a list of open ports.

    Parameters
    ----------
    host : str
        Hostname or IP address to scan.
    start_port : int, optional
        Starting port number (default: 1).
    end_port : int, optional
        Ending port number (default: 1024).
    timeout : float, optional
        Timeout in seconds for each port (default: 0.5).

    Returns
    -------
    list[int]
        List of open port numbers.

    Examples
    --------
    >>> scan_open_ports('localhost', 22, 25)
    [22, 23, 25]
    """
    # Input validation
    if not isinstance(host, str):
        raise TypeError(f"host must be a string, got {type(host).__name__}")
    if not host:
        raise ValueError("host cannot be empty")
    if not isinstance(start_port, int):
        raise TypeError(f"start_port must be an integer, got {type(start_port).__name__}")
    if not isinstance(end_port, int):
        raise TypeError(f"end_port must be an integer, got {type(end_port).__name__}")
    if not (0 < start_port < 65536):
        raise ValueError("start_port must be between 1 and 65535")
    if not (0 < end_port < 65536):
        raise ValueError("end_port must be between 1 and 65535")
    if start_port > end_port:
        raise ValueError("start_port must be less than or equal to end_port")
    if not isinstance(timeout, (int, float)):
        raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    open_ports = []
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            try:
                sock.connect((host, port))
                open_ports.append(port)
            except Exception:
                continue
    return open_ports

__all__ = ["scan_open_ports"]
