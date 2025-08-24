"""
Module for getting network interface information.
"""

import psutil
from typing import List, Dict, Any


def get_network_interfaces() -> Dict[str, List[Dict[str, Any]]]:
    """
    Get information about network interfaces.

    Returns
    -------
    Dict[str, List[Dict[str, Any]]]
        Dictionary mapping interface names to their address information.

    Examples
    --------
    >>> interfaces = get_network_interfaces()
    >>> isinstance(interfaces, dict)
    True
    """
    return dict(psutil.net_if_addrs())
