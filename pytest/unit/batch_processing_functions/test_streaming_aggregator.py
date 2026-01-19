import pytest

pytestmark = [pytest.mark.unit, pytest.mark.batch_processing]
from python_utils.batch_processing_functions.streaming_aggregator import StreamingAggregator


def test_streaming_aggregator_normal_operation() -> None:
    """
    Test case 1: Normal operation with numeric values.
    """
    agg = StreamingAggregator()

    agg.add(10.0)
    agg.add(20.0)
    agg.add(30.0)

    stats = agg.get_stats()

    assert stats["count"] == 3
    assert stats["mean"] == pytest.approx(20.0)
    assert stats["sum"] == pytest.approx(60.0)


def test_streaming_aggregator_single_value() -> None:
    """
    Test case 2: Single value aggregation.
    """
    agg = StreamingAggregator()

    agg.add(42.0)

    stats = agg.get_stats()

    assert stats["count"] == 1
    assert stats["mean"] == pytest.approx(42.0)
    assert stats["variance"] == 0.0
    assert stats["std_dev"] == 0.0


def test_streaming_aggregator_multiple_additions() -> None:
    """
    Test case 3: Multiple sequential additions.
    """
    agg = StreamingAggregator()

    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    for val in values:
        agg.add(val)

    stats = agg.get_stats()

    assert stats["count"] == 5
    assert stats["mean"] == pytest.approx(3.0)
    assert stats["sum"] == pytest.approx(15.0)
    assert stats["min"] == 1.0
    assert stats["max"] == 5.0


def test_streaming_aggregator_with_integers() -> None:
    """
    Test case 4: Aggregation with integer inputs.
    """
    agg = StreamingAggregator()

    agg.add(10)
    agg.add(20)
    agg.add(30)

    stats = agg.get_stats()

    assert stats["count"] == 3
    assert stats["mean"] == pytest.approx(20.0)


def test_streaming_aggregator_variance_and_std_dev() -> None:
    """
    Test case 5: Variance and standard deviation calculation.
    """
    agg = StreamingAggregator()

    # Values with known statistics
    values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    for val in values:
        agg.add(val)

    stats = agg.get_stats()

    assert stats["count"] == 8
    assert stats["mean"] == pytest.approx(5.0)
    # Sample variance = 4.571 for this dataset (using n-1)
    assert stats["variance"] == pytest.approx(4.571, rel=1e-2)
    assert stats["std_dev"] == pytest.approx(2.138, rel=1e-2)


def test_streaming_aggregator_edge_case_zero_values() -> None:
    """
    Test case 6: Aggregation with zero values.
    """
    agg = StreamingAggregator()

    agg.add(0.0)
    agg.add(0.0)
    agg.add(0.0)

    stats = agg.get_stats()

    assert stats["count"] == 3
    assert stats["mean"] == 0.0
    assert stats["variance"] == 0.0
    assert stats["min"] == 0.0
    assert stats["max"] == 0.0


def test_streaming_aggregator_edge_case_negative_values() -> None:
    """
    Test case 7: Aggregation with negative values.
    """
    agg = StreamingAggregator()

    agg.add(-10.0)
    agg.add(-5.0)
    agg.add(5.0)
    agg.add(10.0)

    stats = agg.get_stats()

    assert stats["count"] == 4
    assert stats["mean"] == pytest.approx(0.0)
    assert stats["min"] == -10.0
    assert stats["max"] == 10.0


def test_streaming_aggregator_edge_case_large_numbers() -> None:
    """
    Test case 8: Aggregation with large numbers.
    """
    agg = StreamingAggregator()

    agg.add(1e10)
    agg.add(2e10)
    agg.add(3e10)

    stats = agg.get_stats()

    assert stats["count"] == 3
    assert stats["mean"] == pytest.approx(2e10)
    assert stats["sum"] == pytest.approx(6e10)


def test_streaming_aggregator_edge_case_small_numbers() -> None:
    """
    Test case 9: Aggregation with very small numbers.
    """
    agg = StreamingAggregator()

    agg.add(1e-10)
    agg.add(2e-10)
    agg.add(3e-10)

    stats = agg.get_stats()

    assert stats["count"] == 3
    assert stats["mean"] == pytest.approx(2e-10, rel=1e-6)


def test_streaming_aggregator_edge_case_mixed_magnitudes() -> None:
    """
    Test case 10: Values with very different magnitudes.
    """
    agg = StreamingAggregator()

    agg.add(1e-5)
    agg.add(1e5)
    agg.add(1e-5)

    stats = agg.get_stats()

    assert stats["count"] == 3
    assert stats["min"] == pytest.approx(1e-5)
    assert stats["max"] == pytest.approx(1e5)


def test_streaming_aggregator_reset() -> None:
    """
    Test case 11: Reset functionality.
    """
    agg = StreamingAggregator()

    agg.add(10.0)
    agg.add(20.0)
    agg.add(30.0)

    stats_before = agg.get_stats()
    assert stats_before["count"] == 3

    agg.reset()

    stats_after = agg.get_stats()
    assert stats_after["count"] == 0
    assert stats_after["mean"] == 0.0
    assert stats_after["variance"] == 0.0


def test_streaming_aggregator_get_stats_empty() -> None:
    """
    Test case 12: get_stats on empty aggregator.
    """
    agg = StreamingAggregator()

    stats = agg.get_stats()

    assert stats["count"] == 0
    assert stats["mean"] == 0.0
    assert stats["variance"] == 0.0
    assert stats["std_dev"] == 0.0
    assert stats["min"] is None
    assert stats["max"] is None
    assert stats["sum"] == 0.0


def test_streaming_aggregator_merge_aggregators() -> None:
    """
    Test case 13: Merge two aggregators.
    """
    agg1 = StreamingAggregator()
    agg2 = StreamingAggregator()

    agg1.add(10.0)
    agg1.add(20.0)

    agg2.add(30.0)
    agg2.add(40.0)

    agg1.merge(agg2)

    stats = agg1.get_stats()

    assert stats["count"] == 4
    assert stats["mean"] == pytest.approx(25.0)
    assert stats["sum"] == pytest.approx(100.0)
    assert stats["min"] == 10.0
    assert stats["max"] == 40.0


def test_streaming_aggregator_merge_empty_aggregator() -> None:
    """
    Test case 14: Merge with empty aggregator.
    """
    agg1 = StreamingAggregator()
    agg2 = StreamingAggregator()

    agg1.add(10.0)
    agg1.add(20.0)

    stats_before = agg1.get_stats()

    agg1.merge(agg2)

    stats_after = agg1.get_stats()

    # Should be unchanged
    assert stats_after["count"] == stats_before["count"]
    assert stats_after["mean"] == stats_before["mean"]


def test_streaming_aggregator_merge_into_empty() -> None:
    """
    Test case 15: Merge into empty aggregator.
    """
    agg1 = StreamingAggregator()
    agg2 = StreamingAggregator()

    agg2.add(10.0)
    agg2.add(20.0)

    agg1.merge(agg2)

    stats = agg1.get_stats()

    assert stats["count"] == 2
    assert stats["mean"] == pytest.approx(15.0)


def test_streaming_aggregator_min_max_tracking() -> None:
    """
    Test case 16: Min and max value tracking.
    """
    agg = StreamingAggregator()

    # Add values 1 through 100
    for i in range(1, 101):
        agg.add(float(i))

    stats = agg.get_stats()

    assert stats["min"] == 1.0
    assert stats["max"] == 100.0
    assert stats["count"] == 100


def test_streaming_aggregator_type_error_invalid_value_type() -> None:
    """
    Test case 17: TypeError for invalid value type.
    """
    agg = StreamingAggregator()

    with pytest.raises(TypeError, match="value must be a number"):
        agg.add("not_a_number")  # type: ignore[arg-type]


def test_streaming_aggregator_type_error_merge_non_aggregator() -> None:
    """
    Test case 18: TypeError when merging with non-StreamingAggregator.
    """
    agg = StreamingAggregator()

    with pytest.raises(TypeError, match="other must be a StreamingAggregator"):
        agg.merge("not_an_aggregator")  # type: ignore[arg-type]


def test_streaming_aggregator_type_error_add_batch_non_list() -> None:
    """
    Test case 19: TypeError for invalid add_batch type.
    """
    agg = StreamingAggregator()

    with pytest.raises(TypeError, match="values must be a list"):
        agg.add_batch("not a list")  # type: ignore[arg-type]


def test_streaming_aggregator_add_batch_functionality() -> None:
    """
    Test case 20: add_batch functionality.
    """
    agg = StreamingAggregator()

    agg.add_batch([1.0, 2.0, 3.0, 4.0, 5.0])

    stats = agg.get_stats()
    assert stats["count"] == 5
    assert stats["mean"] == pytest.approx(3.0)
    assert stats["sum"] == pytest.approx(15.0)


def test_streaming_aggregator_properties_access() -> None:
    """
    Test case 21: Accessing mean, variance, std_dev as properties.
    """
    agg = StreamingAggregator()

    agg.add_batch([2.0, 4.0, 6.0, 8.0])

    assert agg.mean == pytest.approx(5.0)
    assert agg.count == 4
    assert agg.sum == pytest.approx(20.0)
    assert agg.variance > 0.0
    assert agg.std_dev > 0.0


def test_streaming_aggregator_negative_values() -> None:
    """
    Test case 22: Aggregation with negative values.
    """
    agg = StreamingAggregator()

    agg.add_batch([-5.0, -2.0, 0.0, 2.0, 5.0])

    stats = agg.get_stats()
    assert stats["count"] == 5
    assert stats["mean"] == pytest.approx(0.0)
    assert stats["min"] == -5.0
    assert stats["max"] == 5.0


def test_streaming_aggregator_large_numbers() -> None:
    """
    Test case 23: Aggregation with large numbers.
    """
    agg = StreamingAggregator()

    large_values = [1e10, 2e10, 3e10]
    agg.add_batch(large_values)

    stats = agg.get_stats()
    assert stats["count"] == 3
    assert stats["mean"] == pytest.approx(2e10)
    assert stats["sum"] == pytest.approx(6e10)


def test_streaming_aggregator_merge_variance_preservation() -> None:
    """
    Test case 24: Variance is correctly preserved when merging.
    """
    agg1 = StreamingAggregator()
    agg2 = StreamingAggregator()

    agg1.add_batch([1.0, 2.0, 3.0])
    agg2.add_batch([4.0, 5.0, 6.0])

    # Merge and check that combined stats are correct
    agg1.merge(agg2)

    stats = agg1.get_stats()
    assert stats["count"] == 6
    assert stats["mean"] == pytest.approx(3.5)
    # Combined variance should be approximately 3.5
    assert stats["variance"] == pytest.approx(3.5, rel=0.1)
