"""Unit tests for async_event_loop function."""
import asyncio

import pytest

from asyncio_functions.async_event_loop import async_event_loop


def test_async_event_loop_simple_async_function() -> None:
    """
    Test case 1: Run a simple async function.
    """
    # Arrange
    async def simple_task() -> str:
        await asyncio.sleep(0.001)
        return "completed"

    # Act
    result = async_event_loop(simple_task)

    # Assert
    assert result == "completed"


def test_async_event_loop_return_integer() -> None:
    """
    Test case 2: Return integer value from async function.
    """
    # Arrange
    async def number_task() -> int:
        await asyncio.sleep(0.001)
        return 42

    # Act
    result = async_event_loop(number_task)

    # Assert
    assert result == 42


def test_async_event_loop_return_list() -> None:
    """
    Test case 3: Return list from async function.
    """
    # Arrange
    async def list_task() -> list[int]:
        await asyncio.sleep(0.001)
        return [1, 2, 3, 4, 5]

    # Act
    result = async_event_loop(list_task)

    # Assert
    assert result == [1, 2, 3, 4, 5]


def test_async_event_loop_immediate_return() -> None:
    """
    Test case 4: Immediate return without await.
    """
    # Arrange
    async def immediate_task() -> str:
        return "immediate"

    # Act
    result = async_event_loop(immediate_task)

    # Assert
    assert result == "immediate"


def test_async_event_loop_complex_computation() -> None:
    """
    Test case 5: Complex computation with multiple awaits.
    """
    # Arrange
    async def complex_task() -> int:
        await asyncio.sleep(0.001)
        result = 0
        for i in range(5):
            await asyncio.sleep(0.0001)
            result += i
        return result

    # Act
    result = async_event_loop(complex_task)

    # Assert
    assert result == 10  # 0+1+2+3+4
def test_async_event_loop_exception_propagation() -> None:
    """
    Test case 6: Exceptions are properly propagated.
    """
    # Arrange
    async def failing_task() -> None:
        await asyncio.sleep(0.001)
        raise ValueError("Task failed")

    # Act & Assert
    with pytest.raises(ValueError, match="Task failed"):
        async_event_loop(failing_task)
