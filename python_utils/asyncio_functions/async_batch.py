from typing import TypeVar
from collections.abc import Callable
from collections.abc import Awaitable

# Define type variables for input and output types
T = TypeVar("T")
R = TypeVar("R")


async def async_batch(
    func: Callable[[list[T]], Awaitable[list[R]]], items: list[T], batch_size: int
) -> list[R]:
    """
    Process items in batches using an asynchronous function.

    Parameters
    ----------
    func : Callable[[List[T]], List[R]]
        The asynchronous function to apply to each batch of items.
    items : List[T]
        The list of items to process.
    batch_size : int
        The size of each batch.

    Returns
    -------
    List[R]
        A list of results from processing all the batches.

    Examples
    --------
    >>> async def process_batch(batch: List[int]) -> List[int]:
    >>>     await asyncio.sleep(1)
    >>>     return [x * 2 for x in batch]
    >>> asyncio.run(async_batch(process_batch, [1, 2, 3, 4, 5], batch_size=2))
    [2, 4, 6, 8, 10]
    """
    # Initialize an empty list to store the results
    results = []

    # Iterate over the items in batches of the specified batch_size
    for i in range(0, len(items), batch_size):
        # Get the current batch of items
        batch = items[i: i + batch_size]

        # Apply the asynchronous function to the current batch and await the result
        result = await func(batch)

        # Extend the results list with the result of the current batch
        results.extend(result)

    # Return the list of results from processing all the batches
    return results

__all__ = ['async_batch']
