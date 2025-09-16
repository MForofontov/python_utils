from collections.abc import Callable
from functools import reduce
from multiprocessing import Pool, cpu_count
from typing import TypeVar

# Define a type variable for generic type support
T = TypeVar("T")


def _pair_reduce(args: tuple[list[T], Callable[[T, T], T]]) -> T:
    """Reduce a chunk using ``func``."""
    data_chunk, func = args
    return reduce(func, data_chunk)


def parallel_reduce(
    func: Callable[[T, T], T],
    data: list[T],
    num_processes: int | None = None,
    chunk_size: int = 1,
) -> T:
    """
    Reduce a list to a single value in parallel using the given reduction function.

    Parameters
    ----------
    func : Callable[[T, T], T]
        A function that takes two elements and returns a single value.
    data : list[T]
        The list of data items to reduce.
    num_processes : int | None, optional
        The number of processes to use for parallel execution. If None, it defaults
        to the number of available CPUs (by default None).
    chunk_size : int, optional
        The size of chunks to split the data into for parallel processing (default is 1).

    Returns
    -------
    T
        The final reduced value.

    Examples
    --------
    >>> def sum_two(a: int, b: int) -> int:
    >>>     return a + b
    >>> parallel_reduce(sum_two, [1, 2, 3, 4, 5])
    15
    """

    # If num_processes is not specified, use the number of available CPUs
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
        # Apply the pair_reduce function to each chunk in parallel
        reduced_chunks = pool.map(
            _pair_reduce, [(chunk, func) for chunk in data_chunks]
        )

    # Reduce the results from each chunk to a single value
    return reduce(func, reduced_chunks)


__all__ = ["parallel_reduce"]
