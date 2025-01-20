from typing import Callable, Any
from functools import wraps
import threading

class TimeoutException(Exception):
    """
    Custom exception to be raised when a function times out.
    """
    pass

def timeout(seconds: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator to enforce a timeout on a function, raising a TimeoutException if the function takes longer than the specified time.

    Parameters
    ----------
    seconds : int
        The maximum number of seconds the function is allowed to run.

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
        Callable[..., Any]]
            The wrapped function.
        """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that enforces the timeout.

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

            Raises
            ------
            TimeoutException
                If the function execution exceeds the specified timeout.
            """
            result = [None]  # To store the result of the function call
            exception = [None]  # To store any exception raised by the function

            def target():
                try:
                    # Call the original function and store the result
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    # Store any exception raised by the function
                    exception[0] = e

            # Create a thread to run the target function
            thread = threading.Thread(target=target)
            thread.start()
            # Wait for the thread to complete or timeout
            thread.join(seconds)
            if thread.is_alive():
                # If the thread is still alive after the timeout, raise TimeoutException
                raise TimeoutException(f"{func.__name__} timed out after {seconds} seconds")
            if exception[0]:
                # If an exception was raised by the function, raise it
                raise exception[0]
            # Return the result of the function call
            return result[0]
        return wrapper
    return decorator
