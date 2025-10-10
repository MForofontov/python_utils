"""Unit tests for async_stream_processor function."""
from collections.abc import AsyncIterator

import pytest

from asyncio_functions.async_stream_processor import async_stream_processor


@pytest.mark.asyncio
async def test_async_stream_processor_normal_stream() -> None:
    """
    Test case 1: Process a normal stream of data.
    """
    # Arrange
    processed_items = []

    async def generate_data() -> AsyncIterator[str]:
        for i in range(5):
            yield f"item_{i}"

    async def process_item(item: str) -> None:
        processed_items.append(item)

    # Act
    await async_stream_processor(generate_data(), process_item)

    # Assert
    assert processed_items == ["item_0", "item_1", "item_2", "item_3", "item_4"]


@pytest.mark.asyncio
async def test_async_stream_processor_empty_stream() -> None:
    """
    Test case 2: Process an empty stream.
    """
    # Arrange
    processed_items = []

    async def generate_empty() -> AsyncIterator[str]:
        return
        yield  # Make it a generator

    async def process_item(item: str) -> None:
        processed_items.append(item)

    # Act
    await async_stream_processor(generate_empty(), process_item)

    # Assert
    assert processed_items == []


@pytest.mark.asyncio
async def test_async_stream_processor_single_item_stream() -> None:
    """
    Test case 3: Process a stream with a single item.
    """
    # Arrange
    processed_items = []

    async def generate_single() -> AsyncIterator[str]:
        yield "single_item"

    async def process_item(item: str) -> None:
        processed_items.append(item.upper())

    # Act
    await async_stream_processor(generate_single(), process_item)

    # Assert
    assert processed_items == ["SINGLE_ITEM"]


@pytest.mark.asyncio
async def test_async_stream_processor_transformation() -> None:
    """
    Test case 4: Stream processing with transformations.
    """
    # Arrange
    results = []

    async def generate_numbers() -> AsyncIterator[str]:
        for i in range(1, 4):
            yield str(i)

    async def process_and_double(item: str) -> None:
        results.append(int(item) * 2)

    # Act
    await async_stream_processor(generate_numbers(), process_and_double)

    # Assert
    assert results == [2, 4, 6]


@pytest.mark.asyncio
async def test_async_stream_processor_large_stream() -> None:
    """
    Test case 5: Process a large stream efficiently.
    """
    # Arrange
    count = []

    async def generate_large_stream() -> AsyncIterator[str]:
        for i in range(100):
            yield f"data_{i}"

    async def count_items(item: str) -> None:
        count.append(1)

    # Act
    await async_stream_processor(generate_large_stream(), count_items)

    # Assert
    assert len(count) == 100
@pytest.mark.asyncio
async def test_async_stream_processor_exception_in_processor() -> None:
    """
    Test case 6: Exception in processor stops processing.
    """
    # Arrange
    processed_items = []

    async def generate_data() -> AsyncIterator[str]:
        for i in range(5):
            yield f"item_{i}"

    async def failing_processor(item: str) -> None:
        processed_items.append(item)
        if len(processed_items) >= 3:
            raise ValueError("Processing error")

    # Act & Assert
    with pytest.raises(ValueError, match="Processing error"):
        await async_stream_processor(generate_data(), failing_processor)

    assert len(processed_items) == 3
