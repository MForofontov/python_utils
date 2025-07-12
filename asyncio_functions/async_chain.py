from typing import TypeVar, cast
from collections.abc import Callable
from collections.abc import Awaitable

# Define type variables T and R to represent input and output types
T = TypeVar('T')
R = TypeVar('R')

async def async_chain(functions: list[Callable[[T | R], Awaitable[R]]], input_value: T) -> R:
    """
    Chain multiple asynchronous functions together.

    Parameters
    ----------
    functions : List[Callable[[Union[T, R]], Awaitable[R]]]
        A list of asynchronous functions to chain.
    input_value : T
        The initial input value for the first function.

    Returns
    -------
    R
        The final output after chaining all functions.

    Examples
    --------
    >>> async def func_a(x: int) -> int:
    >>>     await asyncio.sleep(1)
    >>>     return x + 1
    >>> 
    >>> async def func_b(x: int) -> int:
    >>>     await asyncio.sleep(1)
    >>>     return x * 2
    >>> 
    >>> result = await async_chain([func_a, func_b], 5)  # ((5 + 1) * 2)
    >>> print(result)  # Output: 12
    """
    # Initialize the value with the input value
    value: T | R = input_value
    
    # Iterate over each function in the list
    for func in functions:
        # Await the result of the function and update the value
        value = await func(value)
    
    # Return the final result after chaining all functions, cast to R
    return cast(R, value)