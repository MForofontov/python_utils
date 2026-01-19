import asyncio

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.asyncio_functions]
from asyncio_functions.async_chain import async_chain


@pytest.mark.asyncio
async def test_async_chain_normal_chaining() -> None:
    """
    Test case 1: Normal chaining of multiple async functions.
    """

    # Arrange
    async def add_one(x: int) -> int:
        await asyncio.sleep(0.001)
        return x + 1

    async def multiply_two(x: int) -> int:
        await asyncio.sleep(0.001)
        return x * 2

    async def subtract_three(x: int) -> int:
        await asyncio.sleep(0.001)
        return x - 3

    # Act
    result = await async_chain([add_one, multiply_two, subtract_three], 5)

    # Assert
    # ((5 + 1) * 2) - 3 = 9
    assert result == 9


@pytest.mark.asyncio
async def test_async_chain_single_function() -> None:
    """
    Test case 2: Chain with a single function.
    """

    # Arrange
    async def double(x: int) -> int:
        return x * 2

    # Act
    result = await async_chain([double], 10)

    # Assert
    assert result == 20


@pytest.mark.asyncio
async def test_async_chain_empty_function_list() -> None:
    """
    Test case 3: Empty function list returns input value.
    """
    # Arrange
    input_value = 42

    # Act
    result: int = await async_chain([], input_value)

    # Assert
    assert result == 42


@pytest.mark.asyncio
async def test_async_chain_string_operations() -> None:
    """
    Test case 4: Chain string transformation functions.
    """

    # Arrange
    async def add_prefix(s: str) -> str:
        await asyncio.sleep(0.001)
        return f"prefix_{s}"

    async def add_suffix(s: str) -> str:
        await asyncio.sleep(0.001)
        return f"{s}_suffix"

    async def uppercase(s: str) -> str:
        return s.upper()

    # Act
    result = await async_chain([add_prefix, add_suffix, uppercase], "test")

    # Assert
    assert result == "PREFIX_TEST_SUFFIX"


@pytest.mark.asyncio
async def test_async_chain_type_preservation() -> None:
    """
    Test case 5: Type is preserved through the chain.
    """

    # Arrange
    async def increment(x: float) -> float:
        return x + 1.5

    async def multiply(x: float) -> float:
        return x * 2.0

    # Act
    result = await async_chain([increment, multiply], 3.0)

    # Assert
    assert result == 9.0  # (3.0 + 1.5) * 2.0


@pytest.mark.asyncio
async def test_async_chain_complex_transformations() -> None:
    """
    Test case 6: Complex transformations with multiple operations.
    """

    # Arrange
    async def square(x: int) -> int:
        await asyncio.sleep(0.001)
        return x * x

    async def add_ten(x: int) -> int:
        return x + 10

    async def divide_by_two(x: int) -> int:
        return x // 2

    # Act
    result = await async_chain([square, add_ten, divide_by_two], 4)

    # Assert
    # ((4 * 4) + 10) // 2 = 13
    assert result == 13
