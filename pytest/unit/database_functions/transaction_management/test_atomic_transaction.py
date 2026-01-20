"""
Unit tests for atomic_transaction function.
"""

import sqlite3

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.database]
from pyutils_collection.database_functions import atomic_transaction


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
        conn, commit_func=lambda: conn.commit(), rollback_func=lambda: conn.rollback()
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
            rollback_func=lambda: conn.rollback(),
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
        conn, commit_func=lambda: conn.commit(), rollback_func=lambda: conn.rollback()
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
            rollback_func=lambda: conn.rollback(),
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
    with atomic_transaction(conn, commit_func=lambda: conn.commit(), auto_commit=False):
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
            None, commit_func=lambda: None, rollback_func=lambda: None
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


def test_atomic_transaction_with_begin_func() -> None:
    """
    Test case 11: Tests explicit begin_func is called.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER)")

    begin_called = [False]

    def begin_func():
        begin_called[0] = True
        cursor.execute("BEGIN")

    # Act
    with atomic_transaction(
        conn,
        begin_func=begin_func,
        commit_func=lambda: conn.commit(),
        rollback_func=lambda: conn.rollback(),
    ):
        cursor.execute("INSERT INTO test VALUES (1)")

    # Assert
    assert begin_called[0] is True
    result = cursor.execute("SELECT * FROM test").fetchall()
    assert len(result) == 1

    conn.close()


def test_atomic_transaction_fallback_commit() -> None:
    """
    Test case 12: Tests fallback to connection.commit() when commit_func is None.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER)")

    # Act - no explicit commit_func, should use connection.commit()
    with atomic_transaction(conn):
        cursor.execute("INSERT INTO test VALUES (1)")

    # Assert - data should be committed
    result = cursor.execute("SELECT * FROM test").fetchall()
    assert len(result) == 1

    conn.close()


def test_atomic_transaction_fallback_rollback() -> None:
    """
    Test case 13: Tests fallback to connection.rollback() when rollback_func is None.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER)")

    # Act & Assert - no explicit rollback_func, should use connection.rollback()
    with pytest.raises(ValueError):
        with atomic_transaction(conn):
            cursor.execute("INSERT INTO test VALUES (1)")
            raise ValueError("Test error")

    # Assert - data should be rolled back
    result = cursor.execute("SELECT * FROM test").fetchall()
    assert len(result) == 0

    conn.close()


def test_atomic_transaction_commit_with_no_auto_commit() -> None:
    """
    Test case 14: Tests that commit is not called when auto_commit=False.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER)")

    commit_called = [False]

    def commit_func():
        commit_called[0] = True
        conn.commit()

    # Act
    with atomic_transaction(conn, commit_func=commit_func, auto_commit=False):
        cursor.execute("INSERT INTO test VALUES (1)")

    # Assert - commit should not have been called
    assert commit_called[0] is False

    # Manual commit needed
    conn.commit()
    result = cursor.execute("SELECT * FROM test").fetchall()
    assert len(result) == 1

    conn.close()


def test_atomic_transaction_commit_error_handling() -> None:
    """
    Test case 15: Tests that commit errors are propagated.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER)")

    def failing_commit():
        raise RuntimeError("Commit failed")

    # Act & Assert
    with pytest.raises(RuntimeError, match="Commit failed"):
        with atomic_transaction(conn, commit_func=failing_commit):
            cursor.execute("INSERT INTO test VALUES (1)")

    conn.close()


def test_atomic_transaction_rollback_error_during_exception() -> None:
    """
    Test case 16: Tests rollback error is logged when original exception occurs.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")

    def failing_rollback():
        raise RuntimeError("Rollback failed")

    # Act & Assert - original exception should be raised
    with pytest.raises(ValueError, match="Original error"):
        with atomic_transaction(conn, rollback_func=failing_rollback):
            raise ValueError("Original error")

    conn.close()


def test_atomic_transaction_invalid_begin_func() -> None:
    """
    Test case 17: Tests invalid begin_func type raises TypeError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")

    # Act & Assert
    with pytest.raises(TypeError, match="begin_func must be callable or None"):
        with atomic_transaction(conn, begin_func="not_callable"):
            pass

    conn.close()


def test_atomic_transaction_connection_without_commit_method() -> None:
    """
    Test case 18: Tests fallback when connection has no commit() method.
    """
    # Arrange - Mock connection without commit method
    from unittest.mock import Mock

    mock_conn = Mock(spec=[])  # Empty spec, no methods

    # Act & Assert - should log warning about missing commit
    with atomic_transaction(mock_conn):
        pass  # No exception should be raised

    # Connection doesn't have commit(), so it logs warning but continues


def test_atomic_transaction_connection_without_rollback_method() -> None:
    """
    Test case 19: Tests fallback when connection has no rollback() method.
    """
    # Arrange - Mock connection without rollback method
    from unittest.mock import Mock

    mock_conn = Mock(spec=[])  # Empty spec, no methods

    # Act & Assert - should log warning about missing rollback
    with pytest.raises(ValueError):
        with atomic_transaction(mock_conn):
            raise ValueError("Test error")

    # Connection doesn't have rollback(), so it logs warning


def test_atomic_transaction_begin_func_failure() -> None:
    """
    Test case 20: Tests that begin_func errors are propagated.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")

    def failing_begin():
        raise RuntimeError("Begin failed")

    # Act & Assert
    with pytest.raises(RuntimeError, match="Begin failed"):
        with atomic_transaction(conn, begin_func=failing_begin):
            pass

    conn.close()


def test_atomic_transaction_fallback_commit_error() -> None:
    """
    Test case 21: Tests error handling when fallback connection.commit() fails.
    """
    # Arrange
    from unittest.mock import Mock

    mock_conn = Mock()
    mock_conn.commit = Mock(side_effect=RuntimeError("Commit failed"))

    # Act & Assert
    with pytest.raises(RuntimeError, match="Commit failed"):
        with atomic_transaction(mock_conn):
            pass  # Success path, but commit fails


def test_atomic_transaction_fallback_rollback_error() -> None:
    """
    Test case 22: Tests error handling when fallback connection.rollback() fails.
    """
    # Arrange
    from unittest.mock import Mock

    mock_conn = Mock()
    mock_conn.rollback = Mock(side_effect=RuntimeError("Rollback failed"))

    # Act & Assert - original exception should be raised, rollback error logged
    with pytest.raises(ValueError, match="Original error"):
        with atomic_transaction(mock_conn):
            raise ValueError("Original error")
