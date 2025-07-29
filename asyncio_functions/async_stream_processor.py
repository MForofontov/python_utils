from collections.abc import Callable
from collections.abc import AsyncIterator
from typing import Awaitable


# Define an asynchronous function to process a stream of data
async def async_stream_processor(
    stream: AsyncIterator[str],
    process: Callable[[str], Awaitable[None]],
) -> None:
    """
    Process a stream of data asynchronously.

    Parameters
    ----------
    stream : AsyncIterator[str]
        An asynchronous iterator representing the data stream.
    process : Callable[[str], Awaitable[None]]
        An asynchronous function to process each item from the stream.

    Returns
    -------
    None

    Examples
    --------
    >>> async def generate_data() -> AsyncIterator[str]:
    >>>     for i in range(5):
    >>>         yield f"Data {i}"
    >>>
    >>> async def process_data(data: str) -> None:
    >>>     print(f"Processing: {data}")
    >>>
    >>> await async_stream_processor(generate_data(), process_data)
    Processing: Data 0
    Processing: Data 1
    Processing: Data 2
    Processing: Data 3
    Processing: Data 4
    """
    # Iterate over each item in the asynchronous stream
    async for item in stream:
        # Process each item using the provided process function
        await process(item)

__all__ = ['async_stream_processor']
