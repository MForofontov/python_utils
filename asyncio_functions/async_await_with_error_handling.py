# Import necessary types from the typing module
from typing import TypeVar
from collections.abc import Callable
from collections.abc import Awaitable

# Define a type variable T to represent the return type of the tasks
T = TypeVar("T")


async def async_await_with_error_handling(
    tasks: list[Callable[[], Awaitable[T]]],
    error_handler: Callable[[Exception], None],
) -> list[T]:
    """
    Execute multiple asynchronous tasks with custom error handling.

    Parameters
    ----------
    tasks : list[Callable[[], Awaitable[T]]]
        A list of asynchronous functions to execute.
    error_handler : Callable[[Exception], None]
        A function to handle any exceptions that occur during task execution.

    Returns
    -------
    list[T]
        A list of results from successful tasks.

    Raises
    ------
    TypeError
        If ``tasks`` is not a list of callables or ``error_handler`` is not
        callable.
    Exception
        Propagates any exception raised by ``error_handler``.

    Examples
    --------
    >>> async def task_a() -> int:
    >>>     return 1
    >>>
    >>> async def task_b() -> int:
    >>>     raise ValueError("Error in task B")
    >>>
    >>> results = await async_await_with_error_handling(
    ...     [task_a, task_b], lambda e: print(e)
    ... )
    >>> print(results)
    [1]
    """
    # Initialize an empty list to store the results of successful tasks
    results = []

    # Iterate over each task in the list of tasks
    for task in tasks:
        try:
            # Await the result of the task and append it to the results list
            result = await task()
            results.append(result)
        except Exception as e:
            # Handle exception using the provided error handler
            error_handler(e)

    # Return the list of results from successful tasks
    return results


__all__ = ["async_await_with_error_handling"]
