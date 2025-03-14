from multiprocessing import Pool, cpu_count
from typing import List, TypeVar

# Define type variable for input type
T = TypeVar('T')

def parallel_unique(data: List[T], num_processes: int = None, chunk_size: int = 1) -> List[T]:
    """
    Get the unique elements from a list in parallel.

    Parameters
    ----------
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
        A list containing the unique elements from the input list.

    Examples
    --------
    >>> parallel_unique([1, 2, 2, 3, 4, 4, 5])
    [1, 2, 3, 4, 5]
    """
    # If num_processes is not specified, use the number of available CPUs minus one
    if num_processes is None:
        num_processes = cpu_count() - 1  # Pool will default to the number of available CPUs (minus 1)

    # Split the data into chunks of specified chunk_size
    data_chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Apply the set function to each chunk in parallel to get unique elements in each chunk
        unique_chunks = pool.map(lambda chunk: list(set(chunk)), data_chunks)

    # Combine the unique elements from all chunks into a single set
    unique_combined = set()
    for chunk in unique_chunks:
        unique_combined.update(chunk)

    # Convert the set of unique elements back to a list and return
    return list(unique_combined)