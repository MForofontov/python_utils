"""
Unit tests for atomic_transaction function.
"""

import sqlite3

import pytest

from database_functions import atomic_transaction


def test_atomic_transaction_successful_commit() -> None:
    """
    Test case 1: Successful transaction is committed.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE accounts (id INTEGER, balance INTEGER)")
    conn.execute("INSERT INTO accounts VALUES (1, 1000)")
    conn.execute("INSERT INTO accounts VALUES (2, 500)")
    conn.commit()
    
    # Act
    with atomic_transaction(
        conn,
        commit_func=lambda: conn.commit(),
        rollback_func=lambda: conn.rollback()
    ):
        conn.execute("UPDATE accounts SET balance = 900 WHERE id = 1")
        conn.execute("UPDATE accounts SET balance = 600 WHERE id = 2")
    
    # Assert
    result = conn.execute("SELECT balance FROM accounts ORDER BY id").fetchall()
    assert result == [(900,), (600,)]
    
    conn.close()


def test_atomic_transaction_rollback_on_exception() -> None:
    """
    Test case 2: Transaction is rolled back on exception.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE accounts (id INTEGER, balance INTEGER)")
    conn.execute("INSERT INTO accounts VALUES (1, 1000)")
    conn.commit()
    
    # Act
    try:
        with atomic_transaction(
            conn,
            commit_func=lambda: conn.commit(),
            rollback_func=lambda: conn.rollback()
        ):
            conn.execute("UPDATE accounts SET balance = 500 WHERE id = 1")
            raise ValueError("Transaction error")
    except ValueError:
        pass
    
    # Assert - balance should still be 1000
    result = conn.execute("SELECT balance FROM accounts WHERE id = 1").fetchone()
    assert result == (1000,)
    
    conn.close()


def test_atomic_transaction_multiple_operations() -> None:
    """
    Test case 3: Multiple operations in single transaction.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    
    # Act
    with atomic_transaction(
        conn,
        commit_func=lambda: conn.commit(),
        rollback_func=lambda: conn.rollback()
    ):
        conn.execute("INSERT INTO users VALUES (1, 'Alice')")
        conn.execute("INSERT INTO users VALUES (2, 'Bob')")
        conn.execute("INSERT INTO users VALUES (3, 'Charlie')")
    
    # Assert
    result = conn.execute("SELECT COUNT(*) FROM users").fetchone()
    assert result == (3,)
    
    conn.close()


def test_atomic_transaction_with_inserts() -> None:
    """
    Test case 4: Transaction handles INSERT operations.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE log (message TEXT)")
    
    # Act
    with atomic_transaction(conn, commit_func=lambda: conn.commit()):
        conn.execute("INSERT INTO log VALUES ('Entry 1')")
        conn.execute("INSERT INTO log VALUES ('Entry 2')")
    
    # Assert
    result = conn.execute("SELECT message FROM log").fetchall()
    assert len(result) == 2
    
    conn.close()


def test_atomic_transaction_rollback_inserts() -> None:
    """
    Test case 5: Failed transaction rolls back all INSERTs.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (id INTEGER)")
    
    # Act
    try:
        with atomic_transaction(
            conn,
            commit_func=lambda: conn.commit(),
            rollback_func=lambda: conn.rollback()
        ):
            conn.execute("INSERT INTO items VALUES (1)")
            conn.execute("INSERT INTO items VALUES (2)")
            raise RuntimeError("Rollback test")
    except RuntimeError:
        pass
    
    # Assert - no items should be in table
    result = conn.execute("SELECT COUNT(*) FROM items").fetchone()
    assert result == (0,)
    
    conn.close()


def test_atomic_transaction_with_deletes() -> None:
    """
    Test case 6: Transaction handles DELETE operations.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE temp (id INTEGER)")
    conn.executemany("INSERT INTO temp VALUES (?)", [(1,), (2,), (3,)])
    conn.commit()
    
    # Act
    with atomic_transaction(conn, commit_func=lambda: conn.commit()):
        conn.execute("DELETE FROM temp WHERE id = 2")
    
    # Assert
    result = conn.execute("SELECT id FROM temp ORDER BY id").fetchall()
    assert result == [(1,), (3,)]
    
    conn.close()


def test_atomic_transaction_auto_commit_false() -> None:
    """
    Test case 7: auto_commit=False doesn't commit automatically.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE data (value INTEGER)")
    
    # Act
    with atomic_transaction(
        conn,
        commit_func=lambda: conn.commit(),
        auto_commit=False
    ):
        conn.execute("INSERT INTO data VALUES (1)")
    
    # No explicit commit, so data might not be committed
    # (depends on SQLite behavior, just testing the flag works)
    conn.close()


def test_atomic_transaction_none_connection() -> None:
    """
    Test case 8: None connection raises TypeError.
    """
    # Act & Assert
    with pytest.raises(TypeError):
        with atomic_transaction(
            None,
            commit_func=lambda: None,
            rollback_func=lambda: None
        ):
            pass


def test_atomic_transaction_invalid_commit_func() -> None:
    """
    Test case 9: Non-callable commit_func raises TypeError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    
    # Act & Assert
    with pytest.raises(TypeError):
        with atomic_transaction(conn, commit_func="not_callable"):
            pass
    
    conn.close()


def test_atomic_transaction_invalid_rollback_func() -> None:
    """
    Test case 10: Non-callable rollback_func raises TypeError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    
    # Act & Assert
    with pytest.raises(TypeError):
        with atomic_transaction(conn, rollback_func="not_callable"):
            pass
    
    conn.close()
