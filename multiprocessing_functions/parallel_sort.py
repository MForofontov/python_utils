from multiprocessing import Pool, cpu_count


def parallel_sort(
    data: list[int], num_processes: int = None, chunk_size: int = 1
) -> list[int]:
    """
    Sort a list of integers in parallel.

    Parameters
    ----------
    data : List[int]
        The list of integers to sort.
    num_processes : int, optional
        The number of processes to use for parallel execution. If None, it defaults
        to the number of available CPUs (by default None).
    chunk_size : int, optional
        The size of chunks to split the data into for parallel processing (default is 1).

    Returns
    -------
    List[int]
        The sorted list of integers.

    Examples
    --------
    >>> parallel_sort([5, 3, 2, 4, 1])
    [1, 2, 3, 4, 5]
    """

    # Inner function to merge two sorted lists
    def merge(left: list[int], right: list[int]) -> list[int]:
        result = []
        i = j = 0
        # Merge the two lists by comparing elements
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        # Append remaining elements from both lists
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    if num_processes is None:
        num_processes = max(
            cpu_count() - 1,
            1,
        )  # Pool will default to the number of available CPUs (minus 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Split the data into chunks
        data_chunks = [
            data[i : i + chunk_size] for i in range(0, len(data), chunk_size)
        ]
        # Sort each chunk in parallel
        sorted_chunks = pool.map(sorted, data_chunks)

    # Merge sorted chunks until only one sorted list remains
    while len(sorted_chunks) > 1:
        with Pool(processes=num_processes) as pool:
            # Create pairs of sorted chunks to merge
            merge_chunks = [
                (sorted_chunks[i], sorted_chunks[i + 1])
                for i in range(0, len(sorted_chunks) - 1, 2)
            ]
            # Merge the pairs of chunks in parallel
            sorted_chunks = pool.starmap(merge, merge_chunks)

    # Return the final sorted list
    return sorted_chunks[0] if sorted_chunks else []

__all__ = ['parallel_sort']
