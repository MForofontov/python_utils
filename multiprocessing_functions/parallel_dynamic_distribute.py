from multiprocessing import Pool, cpu_count
from typing import TypeVar
from collections.abc import Callable

# Define type variables for input and output types
T = TypeVar('T')
R = TypeVar('R')

def parallel_dynamic_distribute(func: Callable[[T], R], data: list[T], num_processes: int = None, chunk_size: int = 1) -> list[R]:
    """
    Dynamically distribute tasks to worker processes for parallel execution.

    Parameters
    ----------
    func : Callable[[T], R]
        The function to apply to each item in the list.
    data : List[T]
        The list of data items to process.
    num_processes : int, optional
        The number of processes to use for parallel execution. If None, it defaults 
        to the number of available CPUs (by default None).
    chunk_size : int, optional
        The number of tasks to submit to each worker at once (by default 1).

    Returns
    -------
    List[R]
        The list of results after applying the function to each item in parallel.

    Examples
    --------
    >>> def process_item(x: int) -> int:
    >>>     return x * x
    >>> parallel_dynamic_distribute(process_item, [1, 2, 3, 4, 5], chunk_size=2)
    [1, 4, 9, 16, 25]
    """
    if num_processes is None:
        num_processes = cpu_count() - 1 # Pool will default to the number of available CPUs (minus 1)
    
    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Use imap to apply the function to the data in parallel with dynamic task distribution
        results = pool.imap(func, data, chunksize=chunk_size)
    # Convert the results to a list and return
    return list(results)
