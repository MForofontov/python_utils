import asyncio
from typing import Callable, List, TypeVar

T = TypeVar('T')
R = TypeVar('R')

async def async_map(func: Callable[[T], R], items: List[T]) -> List[R]:
    """
    Apply an asynchronous function to a list of items concurrently.

    Parameters
    ----------
    func : Callable[[T], R]
        The asynchronous function to apply to each item.
    items : List[T]
        The list of items to process.

    Returns
    -------
    List[R]
        A list of results after applying the function to each item.

    Examples
    --------
    >>> async def square(x: int) -> int:
    >>>     return x * x
    >>> asyncio.run(async_map(square, [1, 2, 3]))
    [1, 4, 9]
    """
    tasks = [func(item) for item in items]
    return await asyncio.gather(*tasks)
