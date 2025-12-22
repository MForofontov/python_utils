"""
Unit tests for nested_transaction function.
"""

import sqlite3

import pytest

from database_functions import nested_transaction


def test_nested_transaction_successful_release() -> None:
    """
    Test case 1: Successful nested transaction is released.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE accounts (id INTEGER, balance INTEGER)")
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO accounts VALUES (1, 1000)")
    
    # Act
    with nested_transaction(
        cursor,
        savepoint_name="sp1",
        create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
        release_savepoint_func=lambda name: cursor.execute(f"RELEASE SAVEPOINT {name}")
    ):
        cursor.execute("INSERT INTO accounts VALUES (2, 500)")
    
    conn.commit()
    
    # Assert
    result = cursor.execute("SELECT COUNT(*) FROM accounts").fetchone()
    assert result == (2,)
    
    conn.close()


def test_nested_transaction_rollback_on_error() -> None:
    """
    Test case 2: Nested transaction rolls back on error.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE data (value INTEGER)")
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO data VALUES (1)")
    
    # Act
    try:
        with nested_transaction(
            cursor,
            savepoint_name="sp1",
            create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
            rollback_savepoint_func=lambda name: cursor.execute(f"ROLLBACK TO SAVEPOINT {name}")
        ):
            cursor.execute("INSERT INTO data VALUES (2)")
            raise ValueError("Rollback test")
    except ValueError:
        pass
    
    conn.commit()
    
    # Assert - only first insert should remain
    result = cursor.execute("SELECT value FROM data").fetchall()
    assert result == [(1,)]
    
    conn.close()


def test_nested_transaction_multiple_levels() -> None:
    """
    Test case 3: Multiple levels of nesting work correctly.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE items (id INTEGER)")
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO items VALUES (1)")
    
    # Act
    with nested_transaction(
        cursor,
        savepoint_name="outer",
        create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
        release_savepoint_func=lambda name: cursor.execute(f"RELEASE SAVEPOINT {name}")
    ):
        cursor.execute("INSERT INTO items VALUES (2)")
        
        with nested_transaction(
            cursor,
            savepoint_name="inner",
            create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
            release_savepoint_func=lambda name: cursor.execute(f"RELEASE SAVEPOINT {name}")
        ):
            cursor.execute("INSERT INTO items VALUES (3)")
    
    conn.commit()
    
    # Assert
    result = cursor.execute("SELECT COUNT(*) FROM items").fetchone()
    assert result == (3,)
    
    conn.close()


def test_nested_transaction_partial_rollback() -> None:
    """
    Test case 4: Inner savepoint rollback doesn't affect outer.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE log (message TEXT)")
    cursor.execute("BEGIN")
    
    # Act
    with nested_transaction(
        cursor,
        savepoint_name="outer",
        create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
        release_savepoint_func=lambda name: cursor.execute(f"RELEASE SAVEPOINT {name}")
    ):
        cursor.execute("INSERT INTO log VALUES ('Outer entry')")
        
        try:
            with nested_transaction(
                cursor,
                savepoint_name="inner",
                create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
                rollback_savepoint_func=lambda name: cursor.execute(f"ROLLBACK TO SAVEPOINT {name}")
            ):
                cursor.execute("INSERT INTO log VALUES ('Inner entry')")
                raise ValueError("Inner rollback")
        except ValueError:
            pass
    
    conn.commit()
    
    # Assert - outer entry should remain
    result = cursor.execute("SELECT message FROM log").fetchall()
    assert result == [("Outer entry",)]
    
    conn.close()


def test_nested_transaction_auto_generated_name() -> None:
    """
    Test case 5: Auto-generates savepoint name when not provided.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE data (value INTEGER)")
    cursor.execute("BEGIN")
    
    # Act
    with nested_transaction(
        cursor,
        create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
        release_savepoint_func=lambda name: cursor.execute(f"RELEASE SAVEPOINT {name}")
    ):
        cursor.execute("INSERT INTO data VALUES (1)")
    
    conn.commit()
    
    # Assert
    result = cursor.execute("SELECT COUNT(*) FROM data").fetchone()
    assert result == (1,)
    
    conn.close()


def test_nested_transaction_complex_operations() -> None:
    """
    Test case 6: Handles complex UPDATE and INSERT operations.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE accounts (id INTEGER, balance INTEGER)")
    cursor.executemany(
        "INSERT INTO accounts VALUES (?, ?)",
        [(1, 1000), (2, 500)]
    )
    conn.commit()
    
    # Act - SQLite implicitly starts a transaction when we start modifying
    with nested_transaction(
        cursor,
        savepoint_name="transfer",
        create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
        release_savepoint_func=lambda name: cursor.execute(f"RELEASE SAVEPOINT {name}")
    ):
        cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
        cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    
    conn.commit()
    
    # Assert
    result = cursor.execute("SELECT balance FROM accounts ORDER BY id").fetchall()
    assert result == [(900,), (600,)]
    
    conn.close()


def test_nested_transaction_with_constraint_violation() -> None:
    """
    Test case 7: Handles constraint violations in nested transaction.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
    
    # Act & Assert
    try:
        with nested_transaction(
            cursor,
            savepoint_name="sp1",
            create_savepoint_func=lambda name: cursor.execute(f"SAVEPOINT {name}"),
            rollback_savepoint_func=lambda name: cursor.execute(f"ROLLBACK TO SAVEPOINT {name}")
        ):
            cursor.execute("INSERT INTO users VALUES (1, 'Duplicate')")  # Will fail
    except sqlite3.IntegrityError:
        pass
    
    conn.commit()
    
    # Assert - first insert should remain
    result = cursor.execute("SELECT name FROM users WHERE id = 1").fetchone()
    assert result == ("Alice",)
    
    conn.close()


def test_nested_transaction_none_connection() -> None:
    """
    Test case 8: None connection raises TypeError.
    """
    # Act & Assert
    with pytest.raises(TypeError):
        with nested_transaction(
            None,
            savepoint_name="sp1",
            create_savepoint_func=lambda name: None
        ):
            pass


def test_nested_transaction_invalid_savepoint_name_type() -> None:
    """
    Test case 9: Invalid savepoint_name type raises TypeError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    
    # Act & Assert
    with pytest.raises(TypeError):
        with nested_transaction(conn, savepoint_name=123):
            pass
    
    conn.close()


def test_nested_transaction_invalid_create_func() -> None:
    """
    Test case 10: Non-callable create_savepoint_func raises TypeError.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    
    # Act & Assert
    with pytest.raises(TypeError):
        with nested_transaction(conn, create_savepoint_func="not_callable"):
            pass
    
    conn.close()
