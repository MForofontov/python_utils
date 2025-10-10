import time

import requests


def get_network_speed(
    test_url: str = "https://speed.hetzner.de/100MB.bin", timeout: float = 10.0
) -> dict[str, float]:
    """
    Measure download speed from a test server.

    Parameters
    ----------
    test_url : str, optional
        URL to download for speed test (default: Hetzner 100MB file).
    timeout : float, optional
        Timeout in seconds (default: 10.0).

    Returns
    -------
    dict[str, float]
        Dictionary with 'download_mbps'.

    Examples
    --------
    >>> get_network_speed()
    {'download_mbps': 85.2}
    """
    # Input validation
    if not isinstance(test_url, str):
        raise TypeError(f"test_url must be a string, got {type(test_url).__name__}")
    if not test_url:
        raise ValueError("test_url cannot be empty")
    if not isinstance(timeout, (int, float)):
        raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    start = time.time()
    response = requests.get(test_url, stream=True, timeout=timeout)
    total_bytes = 0
    for chunk in response.iter_content(chunk_size=8192):
        total_bytes += len(chunk)
    elapsed = time.time() - start
    mbps = (total_bytes * 8) / (elapsed * 1_000_000)
    return {"download_mbps": mbps}


__all__ = ["get_network_speed"]
