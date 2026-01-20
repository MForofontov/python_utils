"""Get DNS servers configured on system."""


def get_dns_servers() -> list[str]:
    """
    Get DNS servers configured on the system.

    Returns
    -------
    list[str]
        List of DNS server IPs.

    Examples
    --------
    >>> get_dns_servers()
    ['8.8.8.8', '1.1.1.1']
    """
    servers = []
    try:
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    servers.append(line.split()[1])
    except Exception:
        pass
    return servers


__all__ = ["get_dns_servers"]
