from typing import Any
from unittest.mock import Mock

import pytest
from pipeline_functions.pipeline_builder import Pipeline, pipeline_builder


def test_pipeline_case_1_normal_operation() -> None:
    """
    Test case 1: Basic pipeline with single step.
    """
    pipeline = Pipeline()
    pipeline.add_step(lambda x: x * 2)

    result = pipeline.execute(5)

    assert result == 10


def test_pipeline_case_2_multiple_steps() -> None:
    """
    Test case 2: Pipeline with multiple sequential steps.
    """
    pipeline = Pipeline()
    pipeline.add_step(lambda x: x + 10)
    pipeline.add_step(lambda x: x * 2)
    pipeline.add_step(lambda x: x - 5)

    result = pipeline.execute(5)

    assert result == 25  # (5 + 10) * 2 - 5 = 25


def test_pipeline_case_3_callable_execution() -> None:
    """
    Test case 3: Pipeline as callable.
    """
    pipeline = Pipeline()
    pipeline.add_step(lambda x: x**2)

    result = pipeline(4)

    assert result == 16


def test_pipeline_case_4_map_step() -> None:
    """
    Test case 4: Map step with iterable.
    """
    pipeline = Pipeline()
    pipeline.map_step(lambda x: x * 2)

    result = list(pipeline.execute([1, 2, 3, 4]))

    assert result == [2, 4, 6, 8]


def test_pipeline_case_5_filter_step() -> None:
    """
    Test case 5: Filter step with predicate.
    """
    pipeline = Pipeline()
    pipeline.filter_step(lambda x: x % 2 == 0)

    result = list(pipeline.execute([1, 2, 3, 4, 5, 6]))

    assert result == [2, 4, 6]


def test_pipeline_case_6_conditional_step() -> None:
    """
    Test case 6: Conditional step execution.
    """
    pipeline = Pipeline()
    pipeline.add_conditional_step(
        condition=lambda x: x > 10,
        true_func=lambda x: x * 2,
        false_func=lambda x: x + 10,
    )

    result1 = pipeline.execute(5)
    result2 = pipeline.execute(15)

    assert result1 == 15  # 5 + 10
    assert result2 == 30  # 15 * 2


def test_pipeline_case_7_reduce_step() -> None:
    """
    Test case 7: Reduce step aggregation.
    """
    pipeline = Pipeline()
    pipeline.reduce_step(lambda acc, x: acc + x, initial=0)

    result = pipeline.execute([1, 2, 3, 4, 5])

    assert result == 15


def test_pipeline_case_8_tap_step() -> None:
    """
    Test case 8: Tap step for side effects.
    """
    side_effects: list[int] = []

    pipeline = Pipeline()
    pipeline.add_step(lambda x: x * 2)
    pipeline.add_tap_step(lambda x: side_effects.append(x))
    pipeline.add_step(lambda x: x + 5)

    result = pipeline.execute(10)

    assert result == 25  # (10 * 2) + 5
    assert side_effects == [20]  # Tapped value after first step


def test_pipeline_case_9_flatten_step() -> None:
    """
    Test case 9: Flatten step for nested iterables.
    """
    pipeline = Pipeline()
    pipeline.add_flatten_step()

    result = list(pipeline.execute([[1, 2], [3, 4], [5]]))

    assert result == [1, 2, 3, 4, 5]


def test_pipeline_case_10_batch_step() -> None:
    """
    Test case 10: Batch step grouping.
    """
    pipeline = Pipeline()
    pipeline.add_batch_step(batch_size=3)

    result = list(pipeline.execute([1, 2, 3, 4, 5]))

    assert result == [[1, 2, 3], [4, 5]]


def test_pipeline_case_11_distinct_step() -> None:
    """
    Test case 11: Distinct step removes duplicates.
    """
    pipeline = Pipeline()
    pipeline.add_distinct_step()

    result = list(pipeline.execute([1, 2, 2, 3, 1, 4, 3, 5]))

    assert result == [1, 2, 3, 4, 5]


def test_pipeline_case_12_group_by_step() -> None:
    """
    Test case 12: Group by step categorization.
    """
    pipeline = Pipeline()
    pipeline.group_by_step(lambda x: x % 2)

    result_iter = pipeline.execute([1, 2, 3, 4, 5, 6])
    result = {k: list(g) for k, g in result_iter}

    assert result == {0: [2, 4, 6], 1: [1, 3, 5]}


def test_pipeline_case_13_error_handler() -> None:
    """
    Test case 13: Error handler with fallback.
    """
    pipeline = Pipeline()
    pipeline.add_step(lambda x: x / 0)  # Will raise ZeroDivisionError
    pipeline.add_error_handler(lambda x, e: -1)

    result = pipeline.execute(10)

    assert result == -1


def test_pipeline_case_14_combine_pipelines() -> None:
    """
    Test case 14: Combine two pipelines.
    """
    pipeline1 = Pipeline()
    pipeline1.add_step(lambda x: x * 2)

    pipeline2 = Pipeline()
    pipeline2.add_step(lambda x: x + 10)

    combined = pipeline1.combine(pipeline2)

    result = combined.execute(5)

    assert result == 20  # (5 * 2) + 10


def test_pipeline_case_15_complex_pipeline() -> None:
    """
    Test case 15: Complex pipeline with multiple operations.
    """
    pipeline = Pipeline()
    pipeline.add_step(lambda x: x)  # Pass through
    pipeline.map_step(lambda x: x * 2)
    pipeline.filter_step(lambda x: x > 5)
    pipeline.add_distinct_step()
    pipeline.reduce_step(lambda acc, x: acc + x, initial=0)

    result = pipeline.execute([1, 2, 3, 4, 5, 3])

    # [1, 2, 3, 4, 5, 3] -> map(*2) -> [2, 4, 6, 8, 10, 6]
    # -> filter(>5) -> [6, 8, 10, 6]
    # -> distinct -> [6, 8, 10]
    # -> reduce(sum) -> 24
    assert result == 24


def test_pipeline_case_16_edge_case_empty_pipeline() -> None:
    """
    Test case 16: Execute empty pipeline.
    """
    pipeline = Pipeline()

    result = pipeline.execute(42)

    assert result == 42  # No transformations


def test_pipeline_case_17_edge_case_empty_input_list() -> None:
    """
    Test case 17: Pipeline with empty input list.
    """
    pipeline = Pipeline()
    pipeline.map_step(lambda x: x * 2)

    result = list(pipeline.execute([]))

    assert result == []


def test_pipeline_case_18_edge_case_none_input() -> None:
    """
    Test case 18: Pipeline with None input.
    """
    pipeline = Pipeline()
    pipeline.add_step(lambda x: x if x is not None else 0)

    result = pipeline.execute(None)

    assert result == 0


def test_pipeline_case_19_edge_case_single_element_list() -> None:
    """
    Test case 19: Pipeline with single element list.
    """
    pipeline = Pipeline()
    pipeline.map_step(lambda x: x + 1)

    result = list(pipeline.execute([42]))

    assert result == [43]


def test_pipeline_case_20_edge_case_batch_with_remainder() -> None:
    """
    Test case 20: Batch step with remainder elements.
    """
    pipeline = Pipeline()
    pipeline.add_batch_step(batch_size=3)

    result = list(pipeline.execute([1, 2, 3, 4, 5, 6, 7, 8]))

    assert result == [[1, 2, 3], [4, 5, 6], [7, 8]]


def test_pipeline_case_21_edge_case_flatten_empty_sublists() -> None:
    """
    Test case 21: Flatten with empty sublists.
    """
    pipeline = Pipeline()
    pipeline.add_flatten_step()

    result = list(pipeline.execute([[1, 2], [], [3], []]))

    assert result == [1, 2, 3]


def test_pipeline_case_22_edge_case_distinct_all_unique() -> None:
    """
    Test case 22: Distinct with all unique values.
    """
    pipeline = Pipeline()
    pipeline.add_distinct_step()

    result = list(pipeline.execute([1, 2, 3, 4, 5]))

    assert result == [1, 2, 3, 4, 5]


def test_pipeline_case_23_edge_case_distinct_all_duplicates() -> None:
    """
    Test case 23: Distinct with all duplicates.
    """
    pipeline = Pipeline()
    pipeline.add_distinct_step()

    result = list(pipeline.execute([1, 1, 1, 1, 1]))

    assert result == [1]


def test_pipeline_case_24_edge_case_group_by_empty_list() -> None:
    """
    Test case 24: Group by with empty list.
    """
    pipeline = Pipeline()
    pipeline.group_by_step(lambda x: x % 2)

    result_iter = pipeline.execute([])
    result = {k: list(g) for k, g in result_iter}

    assert result == {}


def test_pipeline_case_25_edge_case_reduce_single_element() -> None:
    """
    Test case 25: Reduce with single element.
    """
    pipeline = Pipeline()
    pipeline.reduce_step(lambda acc, x: acc + x, initial=10)

    result = pipeline.execute([5])

    assert result == 15


def test_pipeline_case_26_edge_case_reduce_empty_list() -> None:
    """
    Test case 26: Reduce with empty list returns initial.
    """
    pipeline = Pipeline()
    pipeline.reduce_step(lambda acc, x: acc + x, initial=42)

    result = pipeline.execute([])

    assert result == 42


def test_pipeline_case_27_edge_case_filter_none_match() -> None:
    """
    Test case 27: Filter where no elements match.
    """
    pipeline = Pipeline()
    pipeline.filter_step(lambda x: x > 100)

    result = list(pipeline.execute([1, 2, 3, 4, 5]))

    assert result == []


def test_pipeline_case_28_edge_case_filter_all_match() -> None:
    """
    Test case 28: Filter where all elements match.
    """
    pipeline = Pipeline()
    pipeline.filter_step(lambda x: x > 0)

    result = list(pipeline.execute([1, 2, 3, 4, 5]))

    assert result == [1, 2, 3, 4, 5]


def test_pipeline_case_29_edge_case_conditional_no_false_func() -> None:
    """
    Test case 29: Conditional without false_func.
    """
    pipeline = Pipeline()
    pipeline.add_conditional_step(condition=lambda x: x > 10, true_func=lambda x: x * 2)

    result1 = pipeline.execute(5)
    result2 = pipeline.execute(15)

    assert result1 == 5  # Unchanged
    assert result2 == 30  # 15 * 2


def test_pipeline_case_30_pipeline_builder_function() -> None:
    """
    Test case 30: Use pipeline_builder convenience function.
    """
    pipeline = pipeline_builder()
    pipeline.add_step(lambda x: x * 3)

    result = pipeline.execute(7)

    assert result == 21


def test_pipeline_case_31_type_error_non_callable_step() -> None:
    """
    Test case 31: TypeError for non-callable step.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="func must be callable"):
        pipeline.add_step("not_callable")  # type: ignore[arg-type]


def test_pipeline_case_32_type_error_non_callable_map() -> None:
    """
    Test case 32: TypeError for non-callable map function.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="func must be callable"):
        pipeline.map_step(42)  # type: ignore[arg-type]


def test_pipeline_case_33_type_error_non_callable_filter() -> None:
    """
    Test case 33: TypeError for non-callable filter predicate.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="predicate must be callable"):
        pipeline.filter_step("not_callable")  # type: ignore[arg-type]


def test_pipeline_case_34_type_error_non_callable_condition() -> None:
    """
    Test case 34: TypeError for non-callable condition.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="condition must be callable"):
        pipeline.add_conditional_step(
            condition="not_callable",  # type: ignore[arg-type]
            true_func=lambda x: x,
        )


def test_pipeline_case_35_type_error_non_callable_true_func() -> None:
    """
    Test case 35: TypeError for non-callable true_func.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="true_func must be callable"):
        pipeline.add_conditional_step(
            condition=lambda x: x > 0,
            true_func="not_callable",  # type: ignore[arg-type]
        )


def test_pipeline_case_36_type_error_non_callable_false_func() -> None:
    """
    Test case 36: TypeError for non-callable false_func.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="false_func must be callable or None"):
        pipeline.add_conditional_step(
            condition=lambda x: x > 0,
            true_func=lambda x: x,
            false_func=123,  # type: ignore[arg-type]
        )


def test_pipeline_case_37_type_error_non_callable_reduce_func() -> None:
    """
    Test case 37: TypeError for non-callable reduce function.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="func must be callable"):
        pipeline.reduce_step("not_callable", initial=0)  # type: ignore[arg-type]


def test_pipeline_case_38_type_error_non_callable_tap() -> None:
    """
    Test case 38: TypeError for non-callable tap function.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="func must be callable"):
        pipeline.add_tap_step(None)  # type: ignore[arg-type]


def test_pipeline_case_39_type_error_invalid_batch_size() -> None:
    """
    Test case 39: TypeError for invalid batch size type.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="batch_size must be an integer"):
        pipeline.add_batch_step(batch_size="3")  # type: ignore[arg-type]


def test_pipeline_case_40_value_error_zero_batch_size() -> None:
    """
    Test case 40: ValueError for zero batch size.
    """
    pipeline = Pipeline()

    with pytest.raises(ValueError, match="batch_size must be at least 1"):
        pipeline.add_batch_step(batch_size=0)


def test_pipeline_case_41_value_error_negative_batch_size() -> None:
    """
    Test case 41: ValueError for negative batch size.
    """
    pipeline = Pipeline()

    with pytest.raises(ValueError, match="batch_size must be at least 1"):
        pipeline.add_batch_step(batch_size=-5)


def test_pipeline_case_42_type_error_non_callable_key_func() -> None:
    """
    Test case 42: TypeError for non-callable key function.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="key must be callable"):
        pipeline.group_by_step(key=42)  # type: ignore[arg-type]


def test_pipeline_case_43_type_error_non_callable_error_handler() -> None:
    """
    Test case 43: TypeError for non-callable error handler.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="handler must be callable"):
        pipeline.add_error_handler("not_callable")  # type: ignore[arg-type]


def test_pipeline_case_44_type_error_combine_non_pipeline() -> None:
    """
    Test case 44: TypeError when combining with non-Pipeline.
    """
    pipeline = Pipeline()

    with pytest.raises(TypeError, match="other must be a Pipeline"):
        pipeline.combine("not_a_pipeline")  # type: ignore[arg-type]
