import socket
import psutil

def get_ipv6_addresses() -> list[str]:
    """
    List all IPv6 addresses assigned to the machine.

    Returns
    -------
    list[str]
        List of IPv6 addresses.

    Examples
    --------
    >>> get_ipv6_addresses()
    ['fe80::1', '2001:db8::1']
    """
    ipv6_addrs = []
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET6:
                ipv6_addrs.append(addr.address)
    return ipv6_addrs

__all__ = ["get_ipv6_addresses"]
