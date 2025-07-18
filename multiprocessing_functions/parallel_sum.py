from multiprocessing import Pool, cpu_count

def parallel_sum(data: list[int], num_processes: int = None, chunk_size: int = 1) -> int:
    """
    Sum a list of integers in parallel.

    Parameters
    ----------
    data : List[int]
        The list of integers to sum.
    num_processes : int, optional
        The number of processes to use for parallel execution. If None, it defaults 
        to the number of available CPUs (by default None).
    chunk_size : int, optional
        The size of chunks to split the data into for parallel processing (default is 1).

    Returns
    -------
    int
        The sum of the list of integers.

    Examples
    --------
    >>> parallel_sum([1, 2, 3, 4, 5])
    15
    """
    if num_processes is None:
        num_processes = cpu_count() - 1 # Pool will default to the number of available CPUs (minus 1)
    
    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Split the data into chunks
        data_chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        # Apply the sum function to each chunk in parallel
        chunk_sums = pool.map(sum, data_chunks)

    # Sum the results from each chunk to get the final result
    return sum(chunk_sums)