"""
Unit tests for execute_bulk_chunked function.

Tests cover bulk database operations with chunking, error handling strategies,
and transaction management.
"""

import pytest
from unittest.mock import Mock, call

from database_functions.bulk_operations.execute_bulk_chunked import (
    execute_bulk_chunked,
    BulkOperationResult,
)


def test_execute_bulk_chunked_successful_operation() -> None:
    """
    Test successful bulk operation with all chunks processed.
    """
    # Arrange
    data = [{"id": i, "name": f"Item{i}"} for i in range(50)]
    executor = Mock()
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=10,
        on_error="fail_fast",
    )
    
    # Assert
    assert result["successful"] == 50
    assert result["failed"] == 0
    assert result["total"] == 50
    assert result["errors"] == []
    assert executor.call_count == 5  # 50 rows / 10 chunk_size


def test_execute_bulk_chunked_empty_data() -> None:
    """
    Test bulk operation with empty dataset.
    """
    # Arrange
    data: list[dict[str, int]] = []
    executor = Mock()
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=10,
    )
    
    # Assert
    assert result["successful"] == 0
    assert result["failed"] == 0
    assert result["total"] == 0
    assert result["errors"] == []
    assert executor.call_count == 0


def test_execute_bulk_chunked_single_chunk() -> None:
    """
    Test bulk operation where data fits in single chunk.
    """
    # Arrange
    data = [{"id": i, "name": f"Item{i}"} for i in range(5)]
    executor = Mock()
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=10,
    )
    
    # Assert
    assert result["successful"] == 5
    assert result["total"] == 5
    assert executor.call_count == 1


def test_execute_bulk_chunked_exact_chunk_boundary() -> None:
    """
    Test bulk operation where data size is exact multiple of chunk_size.
    """
    # Arrange
    data = [{"id": i} for i in range(100)]
    executor = Mock()
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=25,
    )
    
    # Assert
    assert result["successful"] == 100
    assert result["total"] == 100
    assert executor.call_count == 4  # 100 / 25 = 4 exact chunks


def test_execute_bulk_chunked_fail_fast_mode() -> None:
    """
    Test fail_fast error handling - stops on first error.
    """
    # Arrange
    data = [{"id": i} for i in range(50)]
    executor = Mock(side_effect=[None, Exception("Database error"), None])
    
    # Act & Assert
    with pytest.raises(Exception, match="Database error"):
        execute_bulk_chunked(
            connection=Mock(),
            statement_executor=executor,
            data=data,
            chunk_size=10,
            on_error="fail_fast",
        )
    
    # Only first 2 chunks attempted before error
    assert executor.call_count == 2


def test_execute_bulk_chunked_skip_mode() -> None:
    """
    Test skip error handling - skips failed chunks and continues.
    """
    # Arrange
    data = [{"id": i} for i in range(50)]
    # Second chunk fails, others succeed
    executor = Mock(side_effect=[None, Exception("Chunk 2 error"), None, None, None])
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=10,
        on_error="skip",
    )
    
    # Assert
    assert result["successful"] == 40  # 50 - 10 (skipped chunk)
    assert result["failed"] == 10
    assert result["total"] == 50
    assert len(result["errors"]) == 1
    assert "Chunk 2 error" in str(result["errors"][0]["error"])
    assert executor.call_count == 5  # All chunks attempted


def test_execute_bulk_chunked_continue_mode() -> None:
    """
    Test continue error handling - processes chunk row-by-row on failure.
    """
    # Arrange
    data = [{"id": i} for i in range(30)]
    
    # First call fails (chunk), then row-by-row: 2 fail, 8 succeed
    calls = [Exception("Chunk error")]  # First chunk call fails
    calls.extend([None] * 8)  # 8 rows succeed individually
    calls.extend([Exception("Row error 1"), Exception("Row error 2")])  # 2 rows fail
    calls.extend([None, None])  # Remaining chunks succeed
    
    executor = Mock(side_effect=calls)
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=10,
        on_error="continue",
    )
    
    # Assert
    assert result["successful"] == 28  # 30 - 2 failed rows
    assert result["failed"] == 2
    assert result["total"] == 30
    assert len(result["errors"]) == 2


def test_execute_bulk_chunked_with_commit_function() -> None:
    """
    Test bulk operation with commit function called after successful chunks.
    """
    # Arrange
    data = [{"id": i} for i in range(25)]
    executor = Mock()
    commit_func = Mock()
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=10,
        on_error="skip",
        commit_func=commit_func,
    )
    
    # Assert
    assert result["successful"] == 25
    assert commit_func.call_count == 3  # Called after each of 3 chunks


def test_execute_bulk_chunked_with_rollback_function() -> None:
    """
    Test bulk operation with rollback function called on chunk failure.
    """
    # Arrange
    data = [{"id": i} for i in range(30)]
    executor = Mock(side_effect=[None, Exception("Error"), None])
    commit_func = Mock()
    rollback_func = Mock()
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=10,
        on_error="skip",
        commit_func=commit_func,
        rollback_func=rollback_func,
    )
    
    # Assert
    assert result["successful"] == 20  # Chunks 1 and 3
    assert result["failed"] == 10  # Chunk 2
    assert commit_func.call_count == 2  # Chunks 1 and 3
    assert rollback_func.call_count == 1  # Chunk 2


def test_execute_bulk_chunked_with_progress_callback() -> None:
    """
    Test bulk operation with progress callback invoked after each chunk.
    """
    # Arrange
    data = [{"id": i} for i in range(35)]
    executor = Mock()
    progress_callback = Mock()
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=10,
        progress_callback=progress_callback,
    )
    
    # Assert
    assert result["successful"] == 35
    assert progress_callback.call_count == 4  # After each chunk
    
    # Verify progress callback arguments
    expected_calls = [
        call(10, 35),   # After chunk 1
        call(20, 35),   # After chunk 2
        call(30, 35),   # After chunk 3
        call(35, 35),   # After chunk 4 (last partial chunk)
    ]
    progress_callback.assert_has_calls(expected_calls)


def test_execute_bulk_chunked_invalid_connection_type() -> None:
    """
    Test TypeError when connection is None.
    """
    # Arrange
    data = [{"id": 1}]
    executor = Mock()
    
    # Act & Assert
    with pytest.raises(TypeError, match="connection cannot be None"):
        execute_bulk_chunked(
            connection=None,
            statement_executor=executor,
            data=data,
            chunk_size=10,
        )


def test_execute_bulk_chunked_invalid_executor_type() -> None:
    """
    Test TypeError when statement_executor is not callable.
    """
    # Arrange
    data = [{"id": 1}]
    
    # Act & Assert
    with pytest.raises(TypeError, match="statement_executor must be callable"):
        execute_bulk_chunked(
            connection=Mock(),
            statement_executor="not_callable",  # type: ignore
            data=data,
            chunk_size=10,
        )


def test_execute_bulk_chunked_invalid_data_type() -> None:
    """
    Test TypeError when data is not a sequence (dict is not a sequence).
    """
    # Arrange
    executor = Mock()
    
    # Act & Assert
    with pytest.raises(TypeError, match="data must be a Sequence"):
        execute_bulk_chunked(
            connection=Mock(),
            statement_executor=executor,
            data={"not": "a_sequence"},  # type: ignore
            chunk_size=10,
        )


def test_execute_bulk_chunked_invalid_chunk_size_type() -> None:
    """
    Test TypeError when chunk_size is not an integer.
    """
    # Arrange
    data = [{"id": 1}]
    executor = Mock()
    
    # Act & Assert
    with pytest.raises(TypeError, match="chunk_size must be int"):
        execute_bulk_chunked(
            connection=Mock(),
            statement_executor=executor,
            data=data,
            chunk_size="invalid",  # type: ignore
        )


def test_execute_bulk_chunked_invalid_chunk_size_value() -> None:
    """
    Test ValueError when chunk_size is zero or negative.
    """
    # Arrange
    data = [{"id": 1}]
    executor = Mock()
    
    # Act & Assert - Zero
    with pytest.raises(ValueError, match="chunk_size must be positive"):
        execute_bulk_chunked(
            connection=Mock(),
            statement_executor=executor,
            data=data,
            chunk_size=0,
        )
    
    # Act & Assert - Negative
    with pytest.raises(ValueError, match="chunk_size must be positive"):
        execute_bulk_chunked(
            connection=Mock(),
            statement_executor=executor,
            data=data,
            chunk_size=-10,
        )


def test_execute_bulk_chunked_invalid_on_error_value() -> None:
    """
    Test ValueError when on_error has invalid value.
    """
    # Arrange
    data = [{"id": 1}]
    executor = Mock()
    
    # Act & Assert
    with pytest.raises(ValueError, match="on_error must be"):
        execute_bulk_chunked(
            connection=Mock(),
            statement_executor=executor,
            data=data,
            chunk_size=10,
            on_error="invalid_mode",  # type: ignore
        )


def test_execute_bulk_chunked_commit_func_not_callable() -> None:
    """
    Test TypeError when commit_func is not callable.
    """
    # Arrange
    data = [{"id": 1}]
    executor = Mock()
    
    # Act & Assert
    with pytest.raises(TypeError, match="commit_func must be callable or None"):
        execute_bulk_chunked(
            connection=Mock(),
            statement_executor=executor,
            data=data,
            chunk_size=10,
            commit_func="not_callable",  # type: ignore
        )


def test_execute_bulk_chunked_rollback_func_not_callable() -> None:
    """
    Test TypeError when rollback_func is not callable.
    """
    # Arrange
    data = [{"id": 1}]
    executor = Mock()
    
    # Act & Assert
    with pytest.raises(TypeError, match="rollback_func must be callable or None"):
        execute_bulk_chunked(
            connection=Mock(),
            statement_executor=executor,
            data=data,
            chunk_size=10,
            rollback_func="not_callable",  # type: ignore
        )


def test_execute_bulk_chunked_progress_callback_not_callable() -> None:
    """
    Test TypeError when progress_callback is not callable.
    """
    # Arrange
    data = [{"id": 1}]
    executor = Mock()
    
    # Act & Assert
    with pytest.raises(TypeError, match="progress_callback must be callable or None"):
        execute_bulk_chunked(
            connection=Mock(),
            statement_executor=executor,
            data=data,
            chunk_size=10,
            progress_callback="not_callable",  # type: ignore
        )


def test_execute_bulk_chunked_large_dataset() -> None:
    """
    Test bulk operation with large dataset (10,000 rows).
    """
    # Arrange
    data = [{"id": i, "value": i * 2} for i in range(10000)]
    executor = Mock()
    progress_callback = Mock()
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=500,
        progress_callback=progress_callback,
    )
    
    # Assert
    assert result["successful"] == 10000
    assert result["failed"] == 0
    assert result["total"] == 10000
    assert executor.call_count == 20  # 10000 / 500
    assert progress_callback.call_count == 20


def test_execute_bulk_chunked_error_details_in_skip_mode() -> None:
    """
    Test error details are properly captured in skip mode.
    """
    # Arrange
    data = [{"id": i} for i in range(30)]
    error_msg = "Unique constraint violation"
    executor = Mock(side_effect=[
        None,
        Exception(error_msg),
        None,
    ])
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=10,
        on_error="skip",
    )
    
    # Assert
    assert len(result["errors"]) == 1
    error_record = result["errors"][0]
    assert "error" in error_record
    assert error_msg in str(error_record["error"])
    assert "chunk_index" in error_record
    assert error_record["chunk_index"] == 2  # Second chunk (1-based indexing)


def test_execute_bulk_chunked_continue_mode_all_rows_fail() -> None:
    """
    Test continue mode when all rows in a chunk fail individually.
    """
    # Arrange
    data = [{"id": i} for i in range(15)]
    
    # First chunk call fails, then all 10 individual rows fail
    calls = [Exception("Chunk error")]
    calls.extend([Exception(f"Row {i} error") for i in range(10)])
    calls.append(None)  # Second chunk succeeds
    
    executor = Mock(side_effect=calls)
    
    # Act
    result = execute_bulk_chunked(
        connection=Mock(),
        statement_executor=executor,
        data=data,
        chunk_size=10,
        on_error="continue",
    )
    
    # Assert
    assert result["successful"] == 5  # Only second chunk (5 rows)
    assert result["failed"] == 10  # All rows in first chunk
    assert result["total"] == 15
    assert len(result["errors"]) == 10  # One error per failed row
