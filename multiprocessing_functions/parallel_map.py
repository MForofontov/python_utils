from multiprocessing import Pool, cpu_count
from typing import TypeVar
from collections.abc import Callable

T = TypeVar("T")
R = TypeVar("R")


def parallel_map(
    func: Callable[[T], R], data: list[T], num_processes: int | None = None
) -> list[R]:
    """
    Apply a function to a list of items in parallel.

    Parameters
    ----------
    func : Callable[[T], R]
        The function to apply to each item in the list.
    data : list[T]
        The list of data items to process.
    num_processes : int | None, optional
        The number of processes to use for parallel execution. If ``None``,
        it defaults to the number of available CPUs minus one with a minimum
        of one process.

    Returns
    -------
    list[R]
        The list of results after applying the function to each item in parallel.

    Examples
    --------
    >>> def square(x: int) -> int:
    >>>     return x * x
    >>> parallel_map(square, [1, 2, 3, 4, 5])
    [1, 4, 9, 16, 25]
    """
    # If num_processes is not specified, use the number of available CPUs
    if num_processes is None:
        # Ensure at least one process is used
        num_processes = max(cpu_count() - 1, 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Map the function to the data in parallel
        results = pool.map(func, data)

    # Return the list of results
    return results


__all__ = ["parallel_map"]
