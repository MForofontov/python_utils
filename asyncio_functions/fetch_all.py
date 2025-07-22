import aiohttp
import asyncio

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    """
    Fetch the content from a URL asynchronously.

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
    # Perform a GET request to the URL
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls: list[str]) -> list[str]:
    """
    Fetch data from multiple URLs asynchronously.

    Parameters
    ----------
    urls : List[str]
        A list of URLs to fetch data from.

    Returns
    -------
    List[str]
        A list of the contents fetched from the URLs.

    Examples
    --------
    >>> urls = ['https://example.com', 'https://httpbin.org']
    >>> asyncio.run(fetch_all(urls))
    ['<html>...</html>', '{"args":{}...']
    """
    # Create a new ClientSession for fetching data
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls] # Create a list of tasks to fetch data from each URL
        return await asyncio.gather(*tasks)

