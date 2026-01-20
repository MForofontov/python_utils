"""Async connection pooling for resource management."""

import asyncio
from collections.abc import Awaitable, Callable
from typing import Generic, TypeVar

# Define type variables for the connection object and the return type of the task
C = TypeVar("C")
T = TypeVar("T")


class AsyncConnectionPool(Generic[C]):
    """
    A simple asynchronous connection pool for managing connections.

    Attributes
    ----------
    max_connections : int
        The maximum number of connections in the pool.
    _pool : asyncio.Queue[C]
        The internal queue to manage connections.
    """

    def __init__(self, max_connections: int) -> None:
        """
        Initialize the connection pool with a maximum number of connections.

        Parameters
        ----------
        max_connections : int
            The maximum number of connections in the pool.

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> pool = AsyncConnectionPool[str](max_connections=2)
        """
        self.max_connections = max_connections
        self._pool: asyncio.Queue[C] = asyncio.Queue(max_connections)

    async def acquire(self) -> C:
        """
        Acquire a connection from the pool.

        Parameters
        ----------
        None

        Returns
        -------
        C
            A connection from the pool.

        Raises
        ------
        None

        Examples
        --------
        >>> pool = AsyncConnectionPool[str](1)
        >>> await pool.add_connection('conn')  # doctest: +SKIP
        >>> await pool.acquire()  # doctest: +SKIP
        'conn'
        """
        # Wait until a connection is available and return it
        conn = await self._pool.get()
        return conn

    async def release(self, conn: C) -> None:
        """
        Release a connection back to the pool.

        Parameters
        ----------
        conn : C
            The connection to release back to the pool.

        Returns
        -------
        None

        Raises
        ------
        None

        Examples
        --------
        >>> pool = AsyncConnectionPool[str](1)
        >>> await pool.add_connection('conn')  # doctest: +SKIP
        >>> conn = await pool.acquire()  # doctest: +SKIP
        >>> await pool.release(conn)  # doctest: +SKIP
        """
        # Put the connection back into the pool
        await self._pool.put(conn)

    async def add_connection(self, conn: C) -> None:
        """
        Add a new connection to the pool.

        Parameters
        ----------
        conn : C
            The connection to add to the pool.

        Raises
        ------
        RuntimeError
            If the connection pool is full.

        Returns
        -------
        None

        Examples
        --------
        >>> pool = AsyncConnectionPool[str](1)
        >>> await pool.add_connection('conn')  # doctest: +SKIP
        """
        # Check if the pool is not full before adding the connection
        if self._pool.qsize() < self.max_connections:
            await self._pool.put(conn)
        else:
            raise RuntimeError("Connection pool is full.")


async def use_connection(
    pool: AsyncConnectionPool[C], task: Callable[[C], Awaitable[T]]
) -> T:
    """
    Use a connection from the pool to perform a task.

    Parameters
    ----------
    pool : AsyncConnectionPool[C]
        The connection pool to use.
    task : Callable[[C], Awaitable[T]]
        The task to perform using the connection.

    Returns
    -------
    T
        The result of the task.

    Raises
    ------
    None

    Examples
    --------
    >>> async def task(conn: str) -> str:
    ...     return conn.upper()
    >>> pool = AsyncConnectionPool[str](1)
    >>> await pool.add_connection('db')  # doctest: +SKIP
    >>> await use_connection(pool, task)  # doctest: +SKIP
    'DB'
    """
    # Acquire a connection from the pool
    conn = await pool.acquire()
    try:
        # Perform the task using the acquired connection
        return await task(conn)
    finally:
        # Release the connection back to the pool
        await pool.release(conn)


__all__ = ["AsyncConnectionPool", "use_connection"]
