"""
Module for getting system uptime.
"""

import time

import psutil


def get_uptime() -> float:
    """
    Get system uptime in seconds.

    Returns
    -------
    float
        System uptime in seconds since boot.

    Examples
    --------
    >>> uptime = get_uptime()
    >>> uptime > 0
    True
    """
    return time.time() - psutil.boot_time()  # type: ignore[no-any-return]


__all__ = ['get_uptime']
