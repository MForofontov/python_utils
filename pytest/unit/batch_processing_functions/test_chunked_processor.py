from typing import Any
from unittest.mock import Mock

import pytest
from batch_processing_functions.chunked_processor import (
    chunked_processor,
    ChunkedProcessor,
)


def test_chunked_processor_case_1_normal_operation() -> None:
    """
    Test case 1: Normal operation with valid inputs.
    """
    items = list(range(10))
    processor = Mock(side_effect=lambda x: x * 2)

    results = list(chunked_processor(items, processor, chunk_size=3))

    assert len(results) == 10
    assert results == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    assert processor.call_count == 10


def test_chunked_processor_case_2_exact_chunk_size() -> None:
    """
    Test case 2: Items count is exact multiple of chunk_size.
    """
    items = list(range(12))
    processor = Mock(side_effect=lambda x: x + 1)

    results = list(chunked_processor(items, processor, chunk_size=4))

    assert len(results) == 12
    assert results == list(range(1, 13))


def test_chunked_processor_case_3_single_chunk() -> None:
    """
    Test case 3: All items fit in single chunk.
    """
    items = [1, 2, 3]
    processor = Mock(side_effect=lambda x: x * 2)

    results = list(chunked_processor(items, processor, chunk_size=5))

    assert len(results) == 3
    assert results == [2, 4, 6]


def test_chunked_processor_case_4_with_strings() -> None:
    """
    Test case 4: Processing strings.
    """
    items = ["hello", "world", "test"]
    processor = Mock(side_effect=lambda x: x.upper())

    results = list(chunked_processor(items, processor, chunk_size=2))

    assert results == ["HELLO", "WORLD", "TEST"]


def test_chunked_processor_case_5_edge_case_empty_iterable() -> None:
    """
    Test case 5: Empty iterable.
    """
    items: list[int] = []
    processor = Mock(side_effect=lambda x: x)

    results = list(chunked_processor(items, processor, chunk_size=3))

    assert len(results) == 0
    assert processor.call_count == 0


def test_chunked_processor_case_6_edge_case_single_item() -> None:
    """
    Test case 6: Single item in iterable.
    """
    items = [42]
    processor = Mock(side_effect=lambda x: x * 2)

    results = list(chunked_processor(items, processor, chunk_size=3))

    assert results == [84]


def test_chunked_processor_case_7_edge_case_chunk_size_one() -> None:
    """
    Test case 7: Chunk size of 1.
    """
    items = [1, 2, 3, 4]
    processor = Mock(side_effect=lambda x: x + 10)

    results = list(chunked_processor(items, processor, chunk_size=1))

    assert results == [11, 12, 13, 14]


def test_chunked_processor_case_8_edge_case_processor_returns_none() -> None:
    """
    Test case 8: Processor returns None for some items.
    """
    items = [1, 2, 3, 4]
    processor = Mock(side_effect=lambda x: None if x % 2 == 0 else x)

    results = list(chunked_processor(items, processor, chunk_size=2))

    assert results == [1, None, 3, None]


def test_chunked_processor_case_9_edge_case_large_chunk_size() -> None:
    """
    Test case 9: Chunk size larger than iterable.
    """
    items = [1, 2, 3]
    processor = Mock(side_effect=lambda x: x * 3)

    results = list(chunked_processor(items, processor, chunk_size=100))

    assert results == [3, 6, 9]


def test_chunked_processor_case_10_type_error_non_iterable() -> None:
    """
    Test case 10: TypeError for non-iterable items.
    """
    processor = Mock()

    with pytest.raises(TypeError, match="items must be iterable"):
        list(chunked_processor(42, processor, chunk_size=3))  # type: ignore[arg-type]


def test_chunked_processor_case_11_type_error_non_callable_processor() -> None:
    """
    Test case 11: TypeError for non-callable processor.
    """
    items = [1, 2, 3]

    with pytest.raises(TypeError, match="processor must be callable"):
        list(chunked_processor(items, "not_callable", chunk_size=3))  # type: ignore[arg-type]


def test_chunked_processor_case_12_type_error_invalid_chunk_size_type() -> None:
    """
    Test case 12: TypeError for invalid chunk_size type.
    """
    items = [1, 2, 3]
    processor = Mock()

    with pytest.raises(TypeError, match="chunk_size must be an integer"):
        list(chunked_processor(items, processor, chunk_size="3"))  # type: ignore[arg-type]


def test_chunked_processor_case_13_value_error_zero_chunk_size() -> None:
    """
    Test case 13: ValueError for zero chunk_size.
    """
    items = [1, 2, 3]
    processor = Mock()

    with pytest.raises(ValueError, match="chunk_size must be at least 1"):
        list(chunked_processor(items, processor, chunk_size=0))


def test_chunked_processor_case_14_value_error_negative_chunk_size() -> None:
    """
    Test case 14: ValueError for negative chunk_size.
    """
    items = [1, 2, 3]
    processor = Mock()

    with pytest.raises(ValueError, match="chunk_size must be at least 1"):
        list(chunked_processor(items, processor, chunk_size=-5))


def test_chunked_processor_class_case_1_normal_operation() -> None:
    """
    Test case 15: ChunkedProcessor class normal operation.
    """
    items = list(range(6))
    processor = Mock(side_effect=lambda x: x * 2)

    cp = ChunkedProcessor(chunk_size=2)
    results = list(cp.process(items, processor))

    assert results == [0, 2, 4, 6, 8, 10]


def test_chunked_processor_class_case_2_with_memory_threshold() -> None:
    """
    Test case 16: ChunkedProcessor with memory threshold.
    """
    items = list(range(10))
    processor = Mock(side_effect=lambda x: x + 1)

    cp = ChunkedProcessor(chunk_size=3, memory_threshold=90.0)
    results = list(cp.process(items, processor))

    assert len(results) == 10


def test_chunked_processor_class_case_3_batch_processor() -> None:
    """
    Test case 17: ChunkedProcessor process_batch.
    """
    items = list(range(9))

    def batch_proc(batch: list[int]) -> list[int]:
        return [x * 2 for x in batch]

    cp = ChunkedProcessor(chunk_size=3)
    results = list(cp.process_batch(items, batch_proc))

    assert results == [0, 2, 4, 6, 8, 10, 12, 14, 16]


def test_chunked_processor_class_case_4_get_stats() -> None:
    """
    Test case 18: ChunkedProcessor get_stats.
    """
    items = list(range(5))
    processor = Mock(side_effect=lambda x: x)

    cp = ChunkedProcessor(chunk_size=2)
    list(cp.process(items, processor))

    stats = cp.get_stats()

    assert "chunks_processed" in stats
    assert "items_processed" in stats
    assert stats["items_processed"] == 5
    assert stats["chunks_processed"] == 3  # 5 items / 2 per chunk = 3 chunks


def test_chunked_processor_class_case_5_reset() -> None:
    """
    Test case 19: ChunkedProcessor reset.
    """
    items = list(range(5))
    processor = Mock(side_effect=lambda x: x)

    cp = ChunkedProcessor(chunk_size=2)
    list(cp.process(items, processor))

    stats_before = cp.get_stats()
    assert stats_before["items_processed"] > 0

    cp.reset()

    stats_after = cp.get_stats()
    assert stats_after["items_processed"] == 0
    assert stats_after["chunks_processed"] == 0


def test_chunked_processor_class_case_6_type_error_invalid_chunk_size() -> None:
    """
    Test case 20: TypeError for invalid chunk_size.
    """
    with pytest.raises(TypeError, match="chunk_size must be an integer"):
        ChunkedProcessor(chunk_size=2.5)  # type: ignore[arg-type]


def test_chunked_processor_class_case_7_value_error_zero_chunk_size() -> None:
    """
    Test case 21: ValueError for zero chunk_size.
    """
    with pytest.raises(ValueError, match="chunk_size must be at least 1"):
        ChunkedProcessor(chunk_size=0)


def test_chunked_processor_class_case_8_type_error_invalid_memory_threshold() -> None:
    """
    Test case 22: TypeError for invalid memory_threshold.
    """
    with pytest.raises(TypeError, match="memory_threshold must be a number or None"):
        ChunkedProcessor(chunk_size=3, memory_threshold="90")  # type: ignore[arg-type]


def test_chunked_processor_class_case_9_value_error_memory_threshold_out_of_range() -> (
    None
):
    """
    Test case 23: ValueError for memory_threshold out of range.
    """
    with pytest.raises(ValueError, match="memory_threshold must be between 0 and 100"):
        ChunkedProcessor(chunk_size=3, memory_threshold=150.0)
