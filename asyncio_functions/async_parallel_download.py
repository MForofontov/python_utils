import aiohttp
import asyncio
import os
from typing import Optional

async def async_parallel_download(url: str, dest_path: str, num_chunks: int = 8, timeout: float = 30.0) -> None:
    """
    Download a file asynchronously from a URL in parallel chunks and save to dest_path.

    Parameters
    ----------
    url : str
        The URL to download from.
    dest_path : str
        The local file path to save the downloaded content.
    num_chunks : int, optional
        Number of parallel chunks (default 8).
    timeout : float, optional
        Timeout in seconds (default 30.0).

    Raises
    ------
    TypeError
        If url or dest_path is not a string, or num_chunks/timeout is not int/float.
    ValueError
        If url is empty, num_chunks < 1, or timeout <= 0.
    RuntimeError
        If download fails.

    Examples
    --------
    >>> asyncio.run(async_parallel_download('https://example.com/file.zip', '/tmp/file.zip'))

    Notes
    -----
    Requires server support for HTTP Range requests.

    Complexity
    ----------
    Time: O(n/num_chunks), Space: O(num_chunks)
    """
    if not isinstance(url, str):
        raise TypeError(f"url must be str, got {type(url).__name__}")
    if not isinstance(dest_path, str):
        raise TypeError(f"dest_path must be str, got {type(dest_path).__name__}")
    if not url:
        raise ValueError("url cannot be empty")
    if not isinstance(num_chunks, int):
        raise TypeError(f"num_chunks must be int, got {type(num_chunks).__name__}")
    if num_chunks < 1:
        raise ValueError("num_chunks must be >= 1")
    if not isinstance(timeout, (int, float)):
        raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            # Get file size
            async with session.head(url) as resp:
                resp.raise_for_status()
                size = int(resp.headers.get("Content-Length", 0))
                accept_ranges = resp.headers.get("Accept-Ranges", "none")
                if size == 0 or accept_ranges.lower() != "bytes":
                    raise RuntimeError("Server does not support range requests or file size unknown")
            # Prepare chunk ranges
            ranges = []
            chunk_size = size // num_chunks
            for i in range(num_chunks):
                start = i * chunk_size
                end = start + chunk_size - 1 if i < num_chunks - 1 else size - 1
                ranges.append((start, end))
            # Download chunks in parallel
            async def fetch_chunk(start, end, idx):
                headers = {"Range": f"bytes={start}-{end}"}
                async with session.get(url, headers=headers) as resp:
                    resp.raise_for_status()
                    data = await resp.content.read()
                    return idx, data
            tasks = [fetch_chunk(start, end, idx) for idx, (start, end) in enumerate(ranges)]
            results = await asyncio.gather(*tasks)
            # Write chunks in order
            results.sort()
            with open(dest_path, "wb") as f:
                for _, data in results:
                    f.write(data)
    except Exception as e:
        raise RuntimeError(f"Parallel download failed: {e}")

__all__ = ["async_parallel_download"]