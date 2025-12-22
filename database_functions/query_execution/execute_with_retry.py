"""
Execute query with automatic retry on failure.
"""

import logging
import time
from collections.abc import Callable
from typing import TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def execute_with_retry(
    execute_func: Callable[[], T],
    max_retries: int = 3,
    retry_delay: float = 1.0,
    backoff_multiplier: float = 2.0,
    retriable_exceptions: tuple[type[Exception], ...] = (Exception,),
) -> T:
    """
    Execute a query with automatic retry on failure.

    Parameters
    ----------
    execute_func : Callable[[], T]
        Function that executes the query and returns the result.
    max_retries : int, optional
        Maximum number of retry attempts (by default 3).
    retry_delay : float, optional
        Initial delay between retries in seconds (by default 1.0).
    backoff_multiplier : float, optional
        Multiplier for exponential backoff (by default 2.0).
    retriable_exceptions : tuple[type[Exception], ...], optional
        Tuple of exception types that should trigger a retry (by default (Exception,)).

    Returns
    -------
    T
        Result from execute_func.

    Raises
    ------
    TypeError
        If parameters are of wrong type.
    ValueError
        If parameters have invalid values.
    Exception
        The last exception if all retries are exhausted.

    Examples
    --------
    >>> def query_func():
    ...     return conn.execute("SELECT * FROM users WHERE active = true")
    >>> result = execute_with_retry(query_func, max_retries=3)
    >>> for row in result:
    ...     print(row)

    Notes
    -----
    - Uses exponential backoff: delay * (multiplier ** attempt)
    - Logs each retry attempt with exception details
    - Non-retriable exceptions are raised immediately

    Complexity
    ----------
    Time: O(1) per attempt, Space: O(1)
    """
    # Input validation
    if not callable(execute_func):
        raise TypeError("execute_func must be callable")
    if not isinstance(max_retries, int):
        raise TypeError(f"max_retries must be int, got {type(max_retries).__name__}")
    if max_retries < 1:
        raise ValueError(f"max_retries must be at least 1, got {max_retries}")
    if not isinstance(retry_delay, (int, float)):
        raise TypeError(f"retry_delay must be a number, got {type(retry_delay).__name__}")
    if retry_delay <= 0:
        raise ValueError(f"retry_delay must be positive, got {retry_delay}")
    if not isinstance(backoff_multiplier, (int, float)):
        raise TypeError(f"backoff_multiplier must be a number, got {type(backoff_multiplier).__name__}")
    if backoff_multiplier < 1:
        raise ValueError(f"backoff_multiplier must be >= 1, got {backoff_multiplier}")
    if not isinstance(retriable_exceptions, tuple):
        raise TypeError(f"retriable_exceptions must be a tuple, got {type(retriable_exceptions).__name__}")

    last_exception = None

    for attempt in range(max_retries):
        try:
            result = execute_func()
            if attempt > 0:
                logger.info(f"Query succeeded on attempt {attempt + 1}")
            return result

        except retriable_exceptions as e:
            last_exception = e
            logger.warning(
                f"Query attempt {attempt + 1}/{max_retries} failed: "
                f"{type(e).__name__}: {e}"
            )

            if attempt < max_retries - 1:
                # Calculate backoff delay
                sleep_time = retry_delay * (backoff_multiplier**attempt)
                logger.debug(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                logger.error(
                    f"All {max_retries} query attempts failed. Last error: {e}"
                )

        except Exception as e:
            # Non-retriable exception
            logger.error(f"Query failed with non-retriable exception: {type(e).__name__}: {e}")
            raise

    # All retries exhausted
    raise last_exception  # type: ignore


__all__ = ["execute_with_retry"]
