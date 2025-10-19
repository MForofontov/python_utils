import pytest
from asyncio_functions.async_await_with_error_handling import (
    async_await_with_error_handling,
)


@pytest.mark.asyncio
async def test_async_await_with_error_handling_all_tasks_succeed() -> None:
    """
    Test case 1: All tasks succeed and return results.
    """

    # Arrange
    async def task1() -> int:
        return 1

    async def task2() -> int:
        return 2

    async def task3() -> int:
        return 3

    errors: list[Exception] = []

    def error_handler(e: Exception) -> None:
        errors.append(e)

    # Act
    results = await async_await_with_error_handling(
        [task1, task2, task3], error_handler
    )

    # Assert
    assert results == [1, 2, 3]
    assert len(errors) == 0


@pytest.mark.asyncio
async def test_async_await_with_error_handling_some_tasks_fail() -> None:
    """
    Test case 2: Some tasks fail but error handler captures them.
    """

    # Arrange
    async def task1() -> int:
        return 1

    async def task2() -> int:
        raise ValueError("Task 2 failed")

    async def task3() -> int:
        return 3

    errors: list[Exception] = []

    def error_handler(e: Exception) -> None:
        errors.append(e)

    # Act
    results = await async_await_with_error_handling(
        [task1, task2, task3], error_handler
    )

    # Assert
    assert results == [1, 3]
    assert len(errors) == 1
    assert isinstance(errors[0], ValueError)
    assert str(errors[0]) == "Task 2 failed"


@pytest.mark.asyncio
async def test_async_await_with_error_handling_all_tasks_fail() -> None:
    """
    Test case 3: All tasks fail and error handler captures all exceptions.
    """

    # Arrange
    async def task1() -> int:
        raise ValueError("Task 1 failed")

    async def task2() -> int:
        raise RuntimeError("Task 2 failed")

    async def task3() -> int:
        raise TypeError("Task 3 failed")

    errors: list[Exception] = []

    def error_handler(e: Exception) -> None:
        errors.append(e)

    # Act
    results = await async_await_with_error_handling(
        [task1, task2, task3], error_handler
    )

    # Assert
    assert results == []
    assert len(errors) == 3
    assert isinstance(errors[0], ValueError)
    assert isinstance(errors[1], RuntimeError)
    assert isinstance(errors[2], TypeError)


@pytest.mark.asyncio
async def test_async_await_with_error_handling_empty_task_list() -> None:
    """
    Test case 4: Empty task list returns empty results.
    """
    # Arrange
    errors: list[Exception] = []

    def error_handler(e: Exception) -> None:
        errors.append(e)

    # Act
    results: list[int] = await async_await_with_error_handling([], error_handler)

    # Assert
    assert results == []
    assert len(errors) == 0


@pytest.mark.asyncio
async def test_async_await_with_error_handling_error_handler_invoked() -> None:
    """
    Test case 5: Error handler is called with the correct exception.
    """

    # Arrange
    async def failing_task() -> int:
        raise ValueError("Specific error message")

    captured_exception: list[Exception] = []

    def error_handler(e: Exception) -> None:
        captured_exception.append(e)

    # Act
    await async_await_with_error_handling([failing_task], error_handler)

    # Assert
    assert len(captured_exception) == 1
    assert str(captured_exception[0]) == "Specific error message"


@pytest.mark.asyncio
async def test_async_await_with_error_handling_mixed_return_types() -> None:
    """
    Test case 6: Tasks with different return types work correctly.
    """

    # Arrange
    async def task1() -> str:
        return "hello"

    async def task2() -> str:
        return "world"

    errors: list[Exception] = []

    def error_handler(e: Exception) -> None:
        errors.append(e)

    # Act
    results = await async_await_with_error_handling([task1, task2], error_handler)

    # Assert
    assert results == ["hello", "world"]
    assert len(errors) == 0
