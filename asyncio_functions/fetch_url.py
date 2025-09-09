import aiohttp
import asyncio

async def fetch_url(session: aiohttp.ClientSession, url: str) -> str:
    """
    Fetch the content from a single URL asynchronously.

    Parameters
    ----------
    session : aiohttp.ClientSession
        The session object used to perform the HTTP request.
    url : str
        The URL to fetch data from.

    Returns
    -------
    str
        The content fetched from the URL as a string.
    """
    async with session.get(url) as response:
        return await response.text()

__all__ = ['fetch_url']
