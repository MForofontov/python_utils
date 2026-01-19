import asyncio

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.asyncio_functions]
from asyncio_functions.async_cleanup import async_cleanup


@pytest.mark.asyncio
async def test_async_cleanup_successful_task_with_cleanup() -> None:
    """
    Test case 1: Successful task execution with cleanup.
    """
    # Arrange
    cleanup_called = []

    async def successful_task() -> str:
        await asyncio.sleep(0.001)
        return "success"

    async def cleanup_function() -> None:
        cleanup_called.append(True)

    # Act
    result = await async_cleanup(successful_task, cleanup_function)

    # Assert
    assert result == "success"
    assert len(cleanup_called) == 1


@pytest.mark.asyncio
async def test_async_cleanup_immediate_task_completion() -> None:
    """
    Test case 2: Immediate task completion with cleanup.
    """
    # Arrange
    cleanup_called = []

    async def immediate_task() -> int:
        return 42

    async def cleanup_function() -> None:
        cleanup_called.append(True)

    # Act
    result = await async_cleanup(immediate_task, cleanup_function)

    # Assert
    assert result == 42
    assert len(cleanup_called) == 1


@pytest.mark.asyncio
async def test_async_cleanup_execution_order() -> None:
    """
    Test case 3: Verify cleanup is called after task completes.
    """
    # Arrange
    execution_order = []

    async def task_with_logging() -> str:
        execution_order.append("task_start")
        await asyncio.sleep(0.001)
        execution_order.append("task_end")
        return "completed"

    async def cleanup_function() -> None:
        execution_order.append("cleanup")

    # Act
    result = await async_cleanup(task_with_logging, cleanup_function)

    # Assert
    assert result == "completed"
    assert execution_order == ["task_start", "task_end", "cleanup"]


@pytest.mark.asyncio
async def test_async_cleanup_different_return_types() -> None:
    """
    Test case 4: Different return value types are preserved.
    """
    # Arrange
    cleanup_called = []

    async def list_task() -> list[int]:
        return [1, 2, 3]

    async def cleanup_function() -> None:
        cleanup_called.append(True)

    # Act
    result = await async_cleanup(list_task, cleanup_function)

    # Assert
    assert result == [1, 2, 3]
    assert len(cleanup_called) == 1


@pytest.mark.asyncio
async def test_async_cleanup_failing_task_with_cleanup() -> None:
    """
    Test case 5: Task fails but cleanup is still called.
    """
    # Arrange
    cleanup_called = []

    async def failing_task() -> str:
        await asyncio.sleep(0.001)
        raise ValueError("Task failed")

    async def cleanup_function() -> None:
        cleanup_called.append(True)

    # Act & Assert
    with pytest.raises(ValueError, match="Task failed"):
        await async_cleanup(failing_task, cleanup_function)

    # Cleanup should still have been called
    assert len(cleanup_called) == 1


@pytest.mark.asyncio
async def test_async_cleanup_on_exception() -> None:
    """
    Test case 6: Cleanup is called even when task raises exception.
    """
    # Arrange
    cleanup_called = []

    async def task_with_exception() -> None:
        raise RuntimeError("Critical error")

    async def cleanup_function() -> None:
        cleanup_called.append(True)

    # Act & Assert
    with pytest.raises(RuntimeError, match="Critical error"):
        await async_cleanup(task_with_exception, cleanup_function)

    assert len(cleanup_called) == 1
