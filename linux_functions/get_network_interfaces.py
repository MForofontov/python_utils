"""
Module for getting network interface information.
"""

import psutil
from typing import Any


def get_network_interfaces() -> dict[str, list[dict[str, Any]]]:
    """
    Get information about network interfaces.

    Returns
    -------
    dict[str, list[dict[str, Any]]]
        Dictionary mapping interface names to their address information.

    Examples
    --------
    >>> interfaces = get_network_interfaces()
    >>> isinstance(interfaces, dict)
    True
    """
    return dict(psutil.net_if_addrs())
