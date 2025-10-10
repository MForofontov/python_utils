import requests


def get_public_ip(timeout: float = 5.0) -> str:
    """
    Get the public IP address of the machine using an external service.

    Parameters
    ----------
    timeout : float, optional
        Timeout in seconds (default: 5.0).

    Returns
    -------
    str
        Public IP address as a string, or empty string if unavailable.

    Examples
    --------
    >>> get_public_ip()
    '8.8.8.8'
    """
    try:
        response = requests.get("https://api.ipify.org", timeout=timeout)
        response.raise_for_status()
        return response.text.strip()
    except Exception:
        return ""


__all__ = ["get_public_ip"]
