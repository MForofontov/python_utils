import socket


def get_local_ip() -> str:
    """
    Get the local IP address of the current machine.

    Returns
    -------
    str
        Local IP address as a string.

    Examples
    --------
    >>> get_local_ip()
    '192.168.1.100'
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return str(ip)
    except Exception:
        return "127.0.0.1"

__all__ = ["get_local_ip"]
