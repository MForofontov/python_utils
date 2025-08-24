"""
Module for pinging a host.
"""

import subprocess
import platform


def ping_host(host: str, count: int = 1, timeout: int = 5) -> bool:
    """
    Ping a host to check if it's reachable.

    Parameters
    ----------
    host : str
        Hostname or IP address to ping.
    count : int, optional
        Number of ping packets to send (by default 1).
    timeout : int, optional
        Timeout in seconds (by default 5).

    Returns
    -------
    bool
        True if host is reachable, False otherwise.

    Raises
    ------
    TypeError
        If host is not a string.

    Examples
    --------
    >>> ping_host('127.0.0.1')  # localhost should be reachable
    True
    >>> ping_host('192.0.2.1', timeout=1)  # RFC5737 test address, should fail
    False
    """
    if not isinstance(host, str):
        raise TypeError("host must be a string")
    
    # Determine the ping command based on the operating system
    system = platform.system().lower()
    if system == "windows":
        cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
    else:  # Linux, macOS, etc.
        cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False
