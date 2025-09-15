from multiprocessing import Pool, cpu_count
from typing import TypeVar, Any
from collections.abc import Callable

# Define type variables for input and output types
T = TypeVar("T")
R = TypeVar("R")


def parallel_apply_with_args(
    func: Callable[[T, Any], R],
    data: list[T],
    args: tuple = (),
    num_processes: int | None = None,
) -> list[R]:
    """
    Apply a function to a list of items in parallel, passing additional arguments to the function.

    Parameters
    ----------
    func : Callable[[T, Any], R]
        The function to apply to each item in the list.
    data : list[T]
        The list of data items to process.
    args : Tuple, optional
        Additional arguments to pass to the function (by default an empty tuple).
    num_processes : int | None, optional
        The number of processes to use for parallel execution. If None, it defaults
        to the number of available CPUs (by default None).

    Returns
    -------
    list[R]
        The list of results after applying the function to each item with the additional arguments in parallel.

    Examples
    --------
    >>> def add_with_offset(x: int, offset: int) -> int:
    >>>     return x + offset
    >>> parallel_apply_with_args(add_with_offset, [1, 2, 3], args=(10,))
    [11, 12, 13]
    """
    # If num_processes is not specified, use the number of available CPUs
    if num_processes is None:
        num_processes = max(
            cpu_count() - 1,
            1,
        )  # Pool will default to the number of available CPUs (minus 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Use starmap to apply the function to the data in parallel, passing additional arguments
        results = pool.starmap(func, [(item, *args) for item in data])

    # Return the list of results
    return results


__all__ = ["parallel_apply_with_args"]
