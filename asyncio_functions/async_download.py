import aiohttp
import asyncio
from typing import Optional

async def async_download(url: str, dest_path: str, timeout: float = 30.0) -> None:
    """
    Download a file asynchronously from a URL and save to dest_path.

    Parameters
    ----------
    url : str
        The URL to download from.
    dest_path : str
        The local file path to save the downloaded content.
    timeout : float, optional
        Timeout in seconds (default 30.0).

    Raises
    ------
    TypeError
        If url or dest_path is not a string.
    ValueError
        If url is empty.
    RuntimeError
        If download fails.

    Examples
    --------
    >>> asyncio.run(async_download('https://example.com/file.txt', '/tmp/file.txt'))

    Complexity
    ----------
    Time: O(n), Space: O(1)
    """
    if not isinstance(url, str):
        raise TypeError(f"url must be str, got {type(url).__name__}")
    if not isinstance(dest_path, str):
        raise TypeError(f"dest_path must be str, got {type(dest_path).__name__}")
    if not url:
        raise ValueError("url cannot be empty")
    if not isinstance(timeout, (int, float)):
        raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                with open(dest_path, 'wb') as f:
                    async for chunk in resp.content.iter_chunked(8192):
                        f.write(chunk)
    except Exception as e:
        raise RuntimeError(f"Download failed: {e}")

__all__ = ["async_download"]