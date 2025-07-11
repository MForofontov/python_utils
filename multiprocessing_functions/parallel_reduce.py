from multiprocessing import Pool, cpu_count
from typing import TypeVar
from collections.abc import Callable
from functools import reduce

# Define a type variable for generic type support
T = TypeVar('T')

def parallel_reduce(func: Callable[[T, T], T], data: list[T], num_processes: int = None, chunk_size: int = 1) -> T:
    """
    Reduce a list to a single value in parallel using the given reduction function.

    Parameters
    ----------
    func : Callable[[T, T], T]
        A function that takes two elements and returns a single value.
    data : List[T]
        The list of data items to reduce.
    num_processes : int, optional
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
    # Inner function to reduce a chunk of data using the provided function
    def pair_reduce(data_chunk):
        return reduce(func, data_chunk)

    # If num_processes is not specified, use the number of available CPUs
    if num_processes is None:
        num_processes = cpu_count() - 1  # Pool will default to the number of available CPUs (minus 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Split the data into chunks
        data_chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        # Apply the pair_reduce function to each chunk in parallel
        reduced_chunks = pool.map(pair_reduce, data_chunks)

    # Reduce the results from each chunk to a single value
    return reduce(func, reduced_chunks)