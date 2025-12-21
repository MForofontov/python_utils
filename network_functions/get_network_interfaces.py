import socket

"""Get network interfaces information."""

import psutil


def get_network_interfaces() -> dict[str, list[str]]:
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
    interfaces: dict[str, list[str]] = {}
    for iface, addrs in psutil.net_if_addrs().items():
        ip_list = [addr.address for addr in addrs if addr.family == socket.AF_INET]
        if ip_list:
            interfaces[iface] = ip_list
    return interfaces


__all__ = ["get_network_interfaces"]
