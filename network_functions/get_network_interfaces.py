import socket
import psutil
from typing import Dict

def get_network_interfaces() -> dict[str, str]:
    """
    List all network interfaces and their IP addresses.

    Returns
    -------
    dict[str, str]
        Mapping of interface name to IP address.

    Examples
    --------
    >>> get_network_interfaces()
    {'eth0': '192.168.1.100', 'lo': '127.0.0.1'}
    """
    interfaces = {}
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                interfaces[iface] = addr.address
    return interfaces

__all__ = ["get_network_interfaces"]
