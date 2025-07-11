from multiprocessing import Pool, cpu_count
from typing import Callable, List, TypeVar
from tqdm import tqdm  # Install using: pip install tqdm

# Define type variables for input and output types
T = TypeVar('T')
R = TypeVar('R')

def parallel_progress_bar(func: Callable[[T], R], data: List[T], num_processes: int = None) -> List[R]:
    """
    Apply a function to a list of items in parallel and display a progress bar.

    Parameters
    ----------
    func : Callable[[T], R]
        The function to apply to each item in the list.
    data : List[T]
        The list of data items to process.
    num_processes : int, optional
        The number of processes to use for parallel execution. If None, it defaults 
        to the number of available CPUs (by default None).

    Returns
    -------
    List[R]
        The list of results after applying the function to each item in parallel.

    Examples
    --------
    >>> def process_item(x: int) -> int:
    >>>     return x * x
    >>> parallel_progress_bar(process_item, [1, 2, 3, 4, 5])
    [1, 4, 9, 16, 25]
    """
    if num_processes is None:
        num_processes = cpu_count() - 1 # Pool will default to the number of available CPUs (minus 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Use tqdm to display a progress bar for the parallel processing
        results = list(tqdm(pool.imap(func, data), total=len(data)))
    # Return the list of results
    return results