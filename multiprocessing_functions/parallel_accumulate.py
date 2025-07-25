from multiprocessing import Pool, cpu_count
from itertools import accumulate
from typing import TypeVar
from collections.abc import Callable

# Define type variable for input and output types
T = TypeVar("T")


def parallel_accumulate(
    func: Callable[[T, T], T],
    data: list[T],
    num_processes: int = None,
    chunk_size: int = 1,
) -> list[T]:
    """
    Apply a cumulative computation to a list of items in parallel.

    Parameters
    ----------
    func : Callable[[T, T], T]
        The function to combine two elements into one cumulative value.
    data : List[T]
        The list of data items to process.
    num_processes : int, optional
        The number of processes to use for parallel execution. If None, it defaults
        to the number of available CPUs (by default None).
    chunk_size : int, optional
        The size of chunks to split the data into for parallel processing (default is 1).

    Returns
    -------
    List[T]
        The list of cumulative results.

    Examples
    --------
    >>> def add(x: int, y: int) -> int:
    >>>     return x + y
    >>> parallel_accumulate(add, [1, 2, 3, 4, 5])
    [1, 3, 6, 10, 15]
    """

    def partial_accumulate(chunk):
        """
        Apply the accumulate function to a chunk of data.

        Parameters
        ----------
        chunk : List[T]
            A chunk of the data list.

        Returns
        -------
        List[T]
            The cumulative results for the chunk.
        """
        return list(accumulate(chunk, func))

    # If num_processes is not specified, default to the number of available CPUs minus one
    if num_processes is None:
        num_processes = (
            cpu_count() - 1
        )  # Pool will default to the number of available CPUs (minus 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Split the data into chunks
        data_chunks = [
            data[i : i + chunk_size] for i in range(0, len(data), chunk_size)
        ]
        # Apply the partial_accumulate function to each chunk in parallel
        partial_results = pool.map(partial_accumulate, data_chunks)

    # Initialize the results list and cumulative offset
    results = []
    cumulative_offset = 0

    # Adjust partial results and combine them into the final results list
    for partial in partial_results:
        # Adjust each partial result by adding the cumulative offset
        adjusted_partial = [x + cumulative_offset for x in partial]
        # Update the cumulative offset to the last value of the adjusted partial
        cumulative_offset = adjusted_partial[-1]
        # Extend the results list with the adjusted partial results
        results.extend(adjusted_partial)

    # Return the final cumulative results
    return results
