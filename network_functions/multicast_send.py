import socket


def multicast_send(message: str, group: str, port: int) -> None:
    """
    Send a UDP multicast message to a group.

    Parameters
    ----------
    message : str
        Message to send.
    group : str
        Multicast group IP.
    port : int
        Port number.

    Returns
    -------
    None

    Examples
    --------
    >>> multicast_send('hello', '224.0.0.1', 5007)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto(message.encode(), (group, port))
    sock.close()


__all__ = ["multicast_send"]
