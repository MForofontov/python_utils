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
