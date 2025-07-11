from multiprocessing import Pool, cpu_count
from typing import TypeVar
from collections.abc import Callable

# Define type variables for input and output types
T = TypeVar('T')
R = TypeVar('R')

def parallel_pipeline(funcs: list[Callable[[T], T]], data: list[T], num_processes: int = None) -> list[R]:
    """
    Apply multiple functions in a pipeline to a list of items in parallel.

    Parameters
    ----------
    funcs : List[Callable[[T], T]]
        A list of functions to apply sequentially to each item.
    data : List[T]
        The list of data items to process.
    num_processes : int, optional
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
    # Inner function to apply the pipeline of functions to a single item
    def apply_pipeline(item: T) -> R:
        # Apply each function in the pipeline sequentially
        for func in funcs:
            item = func(item)
        return item

    # If num_processes is not specified, use the number of available CPUs
    if num_processes is None:
        num_processes = cpu_count() - 1  # Pool will default to the number of available CPUs (minus 1)
    
    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Apply the pipeline to each item in the data list in parallel
        results = pool.map(apply_pipeline, data)

    # Return the list of results
    return results
