from multiprocessing import Pool, cpu_count
from typing import TypeVar
from collections.abc import Callable

# Define type variables for input and output types
T = TypeVar("T")
R = TypeVar("R")


def parallel_broadcast(
    func: Callable[[T, T], R], shared_input: T, data: list[T], num_processes: int = None
) -> list[R]:
    """
    Apply a function in parallel to a list of items, with a shared input broadcasted to all processes.

    Parameters
    ----------
    func : Callable[[T, T], R]
        The function to apply to each item in the list. It takes two arguments: the item and the shared input.
    shared_input : T
        The shared input to broadcast to all processes.
    data : List[T]
        The list of data items to process.
    num_processes : int, optional
        The number of processes to use for parallel execution. If None, it defaults
        to the number of available CPUs (by default None).

    Returns
    -------
    List[R]
        The list of results after applying the function to each item with the shared input.

    Examples
    --------
    >>> def multiply_with_shared(x: int, shared: int) -> int:
    >>>     return x * shared
    >>> parallel_broadcast(multiply_with_shared, 10, [1, 2, 3, 4])
    [10, 20, 30, 40]
    """

    def wrapped_func(item):
        """
        Wrapper function to apply the given function with the shared input.

        Parameters
        ----------
        item : T
            The data item to process.

        Returns
        -------
        R
            The result of applying the function to the item with the shared input.
        """
        return func(item, shared_input)

    # If num_processes is not specified, default to the number of available CPUs minus one
    if num_processes is None:
        num_processes = (
            cpu_count() - 1
        )  # Pool will default to the number of available CPUs (minus 1)

    # Create a pool of worker processes
    with Pool(processes=num_processes) as pool:
        # Apply the wrapped function to each item in the data list in parallel
        results = pool.map(wrapped_func, data)

    # Return the list of results
    return results
