import uuid


def get_mac_address() -> str:
    """
    Get the MAC address of the local machine.

    Returns
    -------
    str
        MAC address as a string.

    Examples
    --------
    >>> get_mac_address()
    '00:1A:2B:3C:4D:5E'
    """
    mac = uuid.getnode()
    mac_str = ':'.join([f'{(mac >> ele) & 0xff:02x}' for ele in range(40, -1, -8)])
    return mac_str

__all__ = ["get_mac_address"]
