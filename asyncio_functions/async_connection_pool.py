from typing import TypeVar, Any
from collections.abc import Callable
from collections.abc import Awaitable
import asyncio

# Define a type variable T to represent the return type of the task
T = TypeVar("T")


class AsyncConnectionPool:
    """
    A simple asynchronous connection pool for managing connections.

    Attributes
    ----------
    max_connections : int
        The maximum number of connections in the pool.
    _pool : asyncio.Queue
        The internal queue to manage connections.
    """

    def __init__(self, max_connections: int):
        """
        Initialize the connection pool with a maximum number of connections.

        Parameters
        ----------
        max_connections : int
            The maximum number of connections in the pool.
        """
        self.max_connections = max_connections
        self._pool: asyncio.Queue[Any] = asyncio.Queue(max_connections)

    async def acquire(self) -> Any:
        """
        Acquire a connection from the pool.

        Returns
        -------
        Any
            A connection from the pool.
        """
        # Wait until a connection is available and return it
        conn = await self._pool.get()
        return conn

    async def release(self, conn: Any) -> None:
        """
        Release a connection back to the pool.

        Parameters
        ----------
        conn : Any
            The connection to release back to the pool.
        """
        # Put the connection back into the pool
        await self._pool.put(conn)

    async def add_connection(self, conn: Any) -> None:
        """
        Add a new connection to the pool.

        Parameters
        ----------
        conn : Any
            The connection to add to the pool.

        Raises
        ------
        RuntimeError
            If the connection pool is full.
        """
        # Check if the pool is not full before adding the connection
        if self._pool.qsize() < self.max_connections:
            await self._pool.put(conn)
        else:
            raise RuntimeError("Connection pool is full.")


async def use_connection(
    pool: AsyncConnectionPool, task: Callable[[Any], Awaitable[T]]
) -> T:
    """
    Use a connection from the pool to perform a task.

    Parameters
    ----------
    pool : AsyncConnectionPool
        The connection pool to use.
    task : Callable[[Any], Awaitable[T]]
        The task to perform using the connection.

    Returns
    -------
    T
        The result of the task.
    """
    # Acquire a connection from the pool
    conn = await pool.acquire()
    try:
        # Perform the task using the acquired connection
        return await task(conn)
    finally:
        # Release the connection back to the pool
        await pool.release(conn)
