from multiprocessing import Pool, cpu_count
from typing import TypeVar
from collections.abc import Callable

R = TypeVar("R")


def parallel_starmap(
    func: Callable[..., R], data: list[tuple], num_processes: int = None
) -> list[R]:
    """
    Apply a function to multiple arguments in parallel using `starmap`.

    Parameters
    ----------
    func : Callable[..., R]
        The function to apply to each set of arguments.
    data : List[Tuple]
        A list of tuples, where each tuple contains the arguments for the function.
    num_processes : int, optional
        The number of processes to use for parallel execution. If None, it defaults
        to the number of available CPUs (by default None).

    Returns
    -------
    List[R]
        The list of results after applying the function to each set of arguments in parallel.

    Examples
    --------
    >>> def multiply(a: int, b: int) -> int:
    >>>     return a * b
    >>> parallel_starmap(multiply, [(1, 2), (3, 4), (5, 6)])
    [2, 12, 30]
    """
    # If num_processes is not specified, use the number of available CPUs
    if num_processes is None:
        num_processes = (
            cpu_count() - 1
        )  # Pool will default to the number of available CPUs (minus 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Use starmap to apply the function to the data in parallel
        results = pool.starmap(func, data)

    # Return the list of results
    return results
