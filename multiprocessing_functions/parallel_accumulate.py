from collections.abc import Callable
from itertools import accumulate
from multiprocessing import Pool, cpu_count
from typing import TypeVar

# Define type variable for input and output types
T = TypeVar("T")


def _partial_accumulate(chunk_func: tuple[list[T], Callable[[T, T], T]]) -> list[T]:
    """Apply ``accumulate`` to a chunk using ``func``."""
    chunk, func = chunk_func
    return list(accumulate(chunk, func))


def parallel_accumulate(
    func: Callable[[T, T], T],
    data: list[T],
    num_processes: int | None = None,
    chunk_size: int = 1,
) -> list[T]:
    """
    Apply a cumulative computation to a list of items in parallel.

    Parameters
    ----------
    func : Callable[[T, T], T]
        The function to combine two elements into one cumulative value.
    data : list[T]
        The list of data items to process.
    num_processes : int | None, optional
        The number of processes to use for parallel execution. If None, it defaults
        to the number of available CPUs (by default None).
    chunk_size : int, optional
        The size of chunks to split the data into for parallel processing (default is 1).

    Returns
    -------
    list[T]
        The list of cumulative results.

    Examples
    --------
    >>> def add(x: int, y: int) -> int:
    >>>     return x + y
    >>> parallel_accumulate(add, [1, 2, 3, 4, 5])
    [1, 3, 6, 10, 15]
    """

    # If num_processes is not specified, default to the number of available CPUs minus one
    if num_processes is None:
        num_processes = max(
            cpu_count() - 1,
            1,
        )  # Pool will default to the number of available CPUs (minus 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Split the data into chunks
        data_chunks = [
            data[i : i + chunk_size] for i in range(0, len(data), chunk_size)
        ]
        # Apply the partial_accumulate function to each chunk in parallel
        partial_results = pool.map(
            _partial_accumulate, [(chunk, func) for chunk in data_chunks]
        )

    # Initialize the results list and cumulative offset
    results: list[T] = []
    cumulative_offset: T = 0  # type: ignore[assignment]

    # Adjust partial results and combine them into the final results list
    for partial in partial_results:
        # Adjust each partial result by adding the cumulative offset
        adjusted_partial = [x + cumulative_offset for x in partial]  # type: ignore[operator]
        # Update the cumulative offset to the last value of the adjusted partial
        cumulative_offset = adjusted_partial[-1]
        # Extend the results list with the adjusted partial results
        results.extend(adjusted_partial)

    # Return the final cumulative results
    return results


__all__ = ["parallel_accumulate"]
