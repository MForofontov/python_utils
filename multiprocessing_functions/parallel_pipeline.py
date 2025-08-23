from multiprocessing import Pool, cpu_count
from typing import TypeVar
from collections.abc import Callable

# Define type variables for input and output types
T = TypeVar("T")
R = TypeVar("R")


def _apply_pipeline(args: tuple[T, list[Callable[[T], T]]]) -> R:
    """Apply a pipeline of functions to ``item``."""
    item, funcs = args
    for func in funcs:
        item = func(item)
    return item


def parallel_pipeline(
    funcs: list[Callable[[T], T]], data: list[T], num_processes: int | None = None
) -> list[R]:
    """
    Apply multiple functions in a pipeline to a list of items in parallel.

    Parameters
    ----------
    funcs : List[Callable[[T], T]]
        A list of functions to apply sequentially to each item.
    data : List[T]
        The list of data items to process.
    num_processes : int | None, optional
        The number of processes to use for parallel execution. If None, it defaults
        to the number of available CPUs (by default None).

    Returns
    -------
    List[R]
        The list of results after applying the pipeline of functions to each item.

    Examples
    --------
    >>> def square(x: int) -> int:
    >>>     return x * x
    >>> def add_one(x: int) -> int:
    >>>     return x + 1
    >>> parallel_pipeline([square, add_one], [1, 2, 3, 4])
    [2, 5, 10, 17]
    """

    # If num_processes is not specified, use the number of available CPUs
    if num_processes is None:
        num_processes = max(
            cpu_count() - 1,
            1,
        )  # Pool will default to the number of available CPUs (minus 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Apply the pipeline to each item in the data list in parallel
        results = pool.map(_apply_pipeline, [(item, funcs) for item in data])

    # Return the list of results
    return results


__all__ = ['parallel_pipeline']
