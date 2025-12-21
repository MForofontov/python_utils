import socket

"""Get subnet mask."""

import psutil


def get_subnet_mask(interface: str) -> str:
    """
    Get the subnet mask for a given network interface.

    Parameters
    ----------
    interface : str
        Name of the network interface.

    Returns
    -------
    str
        Subnet mask as a string, or empty string if not found.

    Examples
    --------
    >>> get_subnet_mask('eth0')
    '255.255.255.0'
    """
    # Input validation
    if not isinstance(interface, str):
        raise TypeError(f"interface must be a string, got {type(interface).__name__}")
    if not interface:
        raise ValueError("interface cannot be empty")

    for addr in psutil.net_if_addrs().get(interface, []):
        if addr.family == socket.AF_INET:
            return addr.netmask or ""
    return ""


__all__ = ["get_subnet_mask"]
