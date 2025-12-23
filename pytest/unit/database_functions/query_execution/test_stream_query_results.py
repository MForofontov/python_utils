"""
Unit tests for stream_query_results function.
"""

import sqlite3

import pytest

from database_functions import stream_query_results


def test_stream_query_results_basic_streaming() -> None:
    """
    Test case 1: Basic streaming of query results.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    conn.executemany(
        "INSERT INTO users VALUES (?, ?)",
        [(1, "Alice"), (2, "Bob"), (3, "Charlie")]
    )
    
    def query_func():
        return conn.execute("SELECT * FROM users")
    
    # Act
    results = list(stream_query_results(query_func, fetch_size=2))
    
    # Assert
    assert len(results) == 3
    assert results[0] == (1, "Alice")
    
    conn.close()


def test_stream_query_results_with_transformation() -> None:
    """
    Test case 2: Streaming with row transformation.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    conn.executemany(
        "INSERT INTO users VALUES (?, ?)",
        [(1, "Alice"), (2, "Bob")]
    )
    
    def query_func():
        return conn.execute("SELECT * FROM users")
    
    def transform(row):
        return {"id": row[0], "name": row[1].upper()}
    
    # Act
    results = list(stream_query_results(
        query_func,
        fetch_size=10,
        transform_func=transform
    ))
    
    # Assert
    assert len(results) == 2
    assert results[0] == {"id": 1, "name": "ALICE"}
    assert results[1] == {"id": 2, "name": "BOB"}
    
    conn.close()


def test_stream_query_results_large_dataset() -> None:
    """
    Test case 3: Streaming handles large datasets efficiently.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE data (value INTEGER)")
    conn.executemany(
        "INSERT INTO data VALUES (?)",
        [(i,) for i in range(1000)]
    )
    
    def query_func():
        return conn.execute("SELECT * FROM data")
    
    # Act
    results = list(stream_query_results(query_func, fetch_size=100))
    
    # Assert
    assert len(results) == 1000
    assert results[0] == (0,)
    assert results[-1] == (999,)
    
    conn.close()


def test_stream_query_results_custom_fetch_size() -> None:
    """
    Test case 4: Custom fetch size controls batching.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (id INTEGER)")
    conn.executemany("INSERT INTO items VALUES (?)", [(i,) for i in range(10)])
    
    def query_func():
        return conn.execute("SELECT * FROM items")
    
    # Act
    results = list(stream_query_results(query_func, fetch_size=3))
    
    # Assert
    assert len(results) == 10
    
    conn.close()


def test_stream_query_results_with_filtering() -> None:
    """
    Test case 5: Transformation can filter results.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE numbers (value INTEGER)")
    conn.executemany("INSERT INTO numbers VALUES (?)", [(i,) for i in range(1, 11)])
    
    def query_func():
        return conn.execute("SELECT * FROM numbers")
    
    def only_even(row):
        value = row[0]
        return value if value % 2 == 0 else None
    
    # Act
    results = [r for r in stream_query_results(
        query_func,
        transform_func=only_even
    ) if r is not None]
    
    # Assert
    assert len(results) == 5
    assert results == [2, 4, 6, 8, 10]
    
    conn.close()


def test_stream_query_results_empty_result_set() -> None:
    """
    Test case 6: Empty result set returns no rows.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    
    def query_func():
        return conn.execute("SELECT * FROM users")
    
    # Act
    results = list(stream_query_results(query_func, fetch_size=10))
    
    # Assert
    assert len(results) == 0
    
    conn.close()


def test_stream_query_results_single_row() -> None:
    """
    Test case 7: Single row is streamed correctly.
    """
    # Arrange
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")
    
    def query_func():
        return conn.execute("SELECT * FROM users")
    
    # Act
    results = list(stream_query_results(query_func, fetch_size=100))
    
    # Assert
    assert len(results) == 1
    assert results[0] == (1, "Alice")
    
    conn.close()


def test_stream_query_results_invalid_execute_func() -> None:
    """
    Test case 8: Non-callable execute_func raises TypeError.
    """
    # Act & Assert
    with pytest.raises(TypeError):
        list(stream_query_results("not_callable", fetch_size=10))


def test_stream_query_results_invalid_fetch_size() -> None:
    """
    Test case 9: Invalid fetch_size raises ValueError.
    """
    # Arrange
    def query_func():
        pass
    
    # Act & Assert
    with pytest.raises(ValueError):
        list(stream_query_results(query_func, fetch_size=0))
    
    with pytest.raises(ValueError):
        list(stream_query_results(query_func, fetch_size=-1))


def test_stream_query_results_invalid_transform_func() -> None:
    """
    Test case 10: Non-callable transform_func raises TypeError.
    """
    # Arrange
    def query_func():
        pass
    
    # Act & Assert
    with pytest.raises(TypeError):
        list(stream_query_results(query_func, transform_func="not_callable"))
