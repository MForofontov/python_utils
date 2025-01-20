import time
from typing import Callable, Any
from functools import wraps

def time_function(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that measures and prints the execution time of a function.

    Parameters
    ----------
    func : Callable[..., Any]
        The function to be timed.

    Returns
    -------
    Callable[..., Any]
        The wrapped function that measures and prints its execution time.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        The wrapper function that measures the execution time.

        Parameters
        ----------
        *args : Any
            Positional arguments for the decorated function.
        **kwargs : Any
            Keyword arguments for the decorated function.

        Returns
        -------
        Any
            The result of the decorated function.
        """
        # Record the start time
        start_time = time.time()
        # Call the original function and get the result
        result = func(*args, **kwargs)
        # Record the end time
        end_time = time.time()
        # Print the execution time
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper
