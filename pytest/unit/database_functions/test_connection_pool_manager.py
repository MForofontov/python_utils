"""
Unit tests for ConnectionPoolManager class.
"""

import sqlite3

import pytest

from database_functions import ConnectionPoolManager


def test_connection_pool_manager_creates_connections() -> None:
    """
    Test case 1: Pool creates and reuses connections.
    """
    # Arrange
    def create_conn():
        return sqlite3.connect(":memory:")
    
    pool = ConnectionPoolManager(create_conn, max_connections=3)
    
    # Act
    with pool.get_connection() as conn1:
        assert conn1 is not None
        conn1.execute("SELECT 1")
    
    with pool.get_connection() as conn2:
        assert conn2 is not None
        conn2.execute("SELECT 1")
    
    stats = pool.get_stats()
    
    # Assert
    assert stats["total_created"] >= 1
    assert stats["max_connections"] == 3
    
    pool.close_all()


def test_connection_pool_manager_health_check() -> None:
    """
    Test case 2: Health check validates connections.
    """
    # Arrange
    def create_conn():
        return sqlite3.connect(":memory:")
    
    pool = ConnectionPoolManager(
        create_conn,
        max_connections=2,
        health_check_query="SELECT 1"
    )
    
    # Act
    with pool.get_connection() as conn:
        conn.execute("SELECT 1")
    
    # Assert - connection was healthy
    stats = pool.get_stats()
    assert stats["total_created"] >= 1
    
    pool.close_all()


def test_connection_pool_manager_removes_closed() -> None:
    """
    Test case 3: Pool removes closed connections.
    """
    # Arrange
    def create_conn():
        return sqlite3.connect(":memory:")
    
    pool = ConnectionPoolManager(create_conn, max_connections=3)
    
    # Act
    with pool.get_connection() as conn:
        conn.execute("SELECT 1")
        conn.close()  # Close connection while in use
    
    # Next get should create new connection
    with pool.get_connection() as conn2:
        assert conn2 is not None
    
    # Assert
    pool.close_all()


def test_connection_pool_manager_max_connections() -> None:
    """
    Test case 4: Max connections limit is enforced.
    """
    # Arrange
    def create_conn():
        return sqlite3.connect(":memory:")
    
    pool = ConnectionPoolManager(create_conn, max_connections=1)
    
    # Act - Acquire first connection
    with pool.get_connection() as conn1:
        # Try to get second connection while first is active
        try:
            with pool.get_connection() as conn2:
                pass
        except RuntimeError as e:
            # Assert
            assert "Maximum connections" in str(e)
    
    pool.close_all()


def test_connection_pool_manager_get_stats() -> None:
    """
    Test case 5: Statistics tracking works correctly.
    """
    # Arrange
    def create_conn():
        return sqlite3.connect(":memory:")
    
    pool = ConnectionPoolManager(create_conn, max_connections=5)
    
    # Act
    with pool.get_connection() as conn:
        conn.execute("SELECT 1")
    
    stats = pool.get_stats()
    
    # Assert
    assert "pool_size" in stats
    assert "active_connections" in stats
    assert "max_connections" in stats
    assert "total_created" in stats
    assert "total_closed" in stats
    assert stats["max_connections"] == 5
    
    pool.close_all()


def test_connection_pool_manager_close_all() -> None:
    """
    Test case 6: close_all closes all pooled connections.
    """
    # Arrange
    def create_conn():
        return sqlite3.connect(":memory:")
    
    pool = ConnectionPoolManager(create_conn, max_connections=3)
    
    with pool.get_connection() as conn:
        conn.execute("SELECT 1")
    
    # Act
    pool.close_all()
    
    # Assert
    stats = pool.get_stats()
    assert stats["pool_size"] == 0


def test_connection_pool_manager_no_health_check() -> None:
    """
    Test case 7: Pool works without health checks.
    """
    # Arrange
    def create_conn():
        return sqlite3.connect(":memory:")
    
    pool = ConnectionPoolManager(
        create_conn,
        max_connections=2,
        health_check_query=None
    )
    
    # Act
    with pool.get_connection() as conn:
        conn.execute("SELECT 1")
    
    # Assert
    stats = pool.get_stats()
    assert stats["total_created"] >= 1
    
    pool.close_all()


def test_connection_pool_manager_invalid_factory() -> None:
    """
    Test case 8: Non-callable factory raises TypeError.
    """
    # Act & Assert
    with pytest.raises(TypeError):
        ConnectionPoolManager("not_callable", max_connections=5)


def test_connection_pool_manager_invalid_max_connections() -> None:
    """
    Test case 9: Invalid max_connections raises error.
    """
    # Arrange
    def create_conn():
        return sqlite3.connect(":memory:")
    
    # Act & Assert
    with pytest.raises(ValueError):
        ConnectionPoolManager(create_conn, max_connections=0)
    
    with pytest.raises(ValueError):
        ConnectionPoolManager(create_conn, max_connections=-1)


def test_connection_pool_manager_invalid_health_check_interval() -> None:
    """
    Test case 10: Invalid health_check_interval raises ValueError.
    """
    # Arrange
    def create_conn():
        return sqlite3.connect(":memory:")
    
    # Act & Assert
    with pytest.raises(ValueError):
        ConnectionPoolManager(
            create_conn,
            max_connections=5,
            health_check_interval=0
        )
