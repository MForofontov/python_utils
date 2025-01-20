from typing import Callable, Any
from functools import wraps
import time

def throttle(rate_limit: float) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to enforce a rate limit on a function, ensuring it is not called more often than the specified rate.

    Parameters
    ----------
    rate_limit : float
        The minimum time interval (in seconds) between consecutive calls to the function.

    Returns
    -------
    Callable[[Callable[..., Any]], Callable[..., Any]]
        The decorator function.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        The actual decorator function.

        Parameters
        ----------
        func : Callable[..., Any]
            The function to be decorated.

        Returns
        -------
        Callable[..., Any]
            The wrapped function.
        """
        # Store the time of the last function call
        last_called = [0.0]

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that enforces the rate limit.

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
            # Get the current time
            current_time = time.time()
            # Calculate the time elapsed since the last function call
            elapsed_time = current_time - last_called[0]
            # If the elapsed time is less than the rate limit, sleep for the remaining time
            if elapsed_time < rate_limit:
                time.sleep(rate_limit - elapsed_time)
            # Update the time of the last function call
            last_called[0] = time.time()
            # Call the original function with the provided arguments and keyword arguments
            return func(*args, **kwargs)

        return wrapper
    return decorator
