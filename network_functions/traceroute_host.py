import subprocess
from typing import List

def traceroute_host(host: str, max_hops: int = 30) -> list[str]:
    """
    Perform a traceroute to a given host and return the hops.

    Parameters
    ----------
    host : str
        Hostname or IP address to traceroute.
    max_hops : int, optional
        Maximum number of hops (default: 30).

    Returns
    -------
    list[str]
        List of hop IPs or hostnames.

    Examples
    --------
    >>> traceroute_host('google.com')
    ['192.168.1.1', '10.0.0.1', ...]
    """
    if not isinstance(host, str):
        raise TypeError(f"host must be a string, got {type(host).__name__}")
    if not host:
        raise ValueError("host cannot be empty")
    cmd = ["traceroute", "-m", str(max_hops), host]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        hops = []
        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            if len(parts) > 1:
                hops.append(parts[1])
        return hops
    except Exception:
        return []

__all__ = ["traceroute_host"]
