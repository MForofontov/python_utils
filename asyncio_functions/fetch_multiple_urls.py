import aiohttp
import asyncio
from .fetch_url import fetch_url

async def fetch_multiple_urls(urls: list[str]) -> list[str]:
    """
    Fetch data from multiple URLs asynchronously.

    Parameters
    ----------
    urls : list[str]
        A list of URLs to fetch data from.

    Returns
    -------
    list[str]
        A list of the contents fetched from the URLs.

    Examples
    --------
    >>> urls = ['https://example.com', 'https://httpbin.org']
    >>> asyncio.run(fetch_multiple_urls(urls))
    ['<html>...</html>', '{"args":{}...']
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

__all__ = ['fetch_multiple_urls']
