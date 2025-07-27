import types
from multiprocessing_functions import (
    parallel_broadcast,
    parallel_reduce,
    parallel_apply_with_args,
    parallel_accumulate,
    parallel_unique,
    parallel_sum,
    parallel_sort,
    parallel_dynamic_distribute,
    parallel_pipeline,
    parallel_starmap,
    parallel_gather_errors,
)


def add(a: int, b: int) -> int:
    return a + b


def square(x: int) -> int:
    return x * x


def multiply_shared(x: int, shared: int) -> int:
    return x * shared


def add_offset(x: int, offset: int) -> int:
    return x + offset


def inc(x: int) -> int:
    return x + 1


def risky(x: int) -> int:
    if x == 2:
        raise ValueError("bad")
    return x * x


# Helper to patch cpu_count to 1 in a module

def patch_cpu_count(monkeypatch, module: types.ModuleType) -> None:
    monkeypatch.setattr(module, "cpu_count", lambda: 1)


def test_parallel_broadcast_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_broadcast)
    data = [1, 2, 3]
    result = parallel_broadcast.parallel_broadcast(multiply_shared, 2, data)
    assert result == [2, 4, 6]


def test_parallel_reduce_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_reduce)
    data = [1, 2, 3, 4]
    result = parallel_reduce.parallel_reduce(add, data)
    assert result == 10


def test_parallel_apply_with_args_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_apply_with_args)
    data = [1, 2, 3]
    result = parallel_apply_with_args.parallel_apply_with_args(
        add_offset, data, args=(5,)
    )
    assert result == [6, 7, 8]


def test_parallel_accumulate_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_accumulate)
    data = [1, 2, 3, 4]
    result = parallel_accumulate.parallel_accumulate(add, data)
    assert result == [1, 3, 6, 10]


def test_parallel_unique_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_unique)
    data = [1, 2, 2, 3]
    result = parallel_unique.parallel_unique(data)
    assert sorted(result) == [1, 2, 3]


def test_parallel_sum_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_sum)
    data = [1, 2, 3, 4]
    result = parallel_sum.parallel_sum(data)
    assert result == 10


def test_parallel_sort_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_sort)
    data = [4, 3, 2, 1]
    result = parallel_sort.parallel_sort(data)
    assert result == [1, 2, 3, 4]


def test_parallel_dynamic_distribute_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_dynamic_distribute)
    data = [1, 2, 3, 4]
    result = parallel_dynamic_distribute.parallel_dynamic_distribute(
        square, data, chunk_size=2
    )
    assert result == [1, 4, 9, 16]


def test_parallel_pipeline_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_pipeline)
    data = [1, 2, 3]
    result = parallel_pipeline.parallel_pipeline([square, inc], data)
    assert result == [2, 5, 10]


def test_parallel_starmap_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_starmap)
    data = [(1, 2), (3, 4)]
    result = parallel_starmap.parallel_starmap(add, data)
    assert result == [3, 7]


def test_parallel_gather_errors_single_cpu(monkeypatch) -> None:
    patch_cpu_count(monkeypatch, parallel_gather_errors)
    data = [1, 2, 3]
    results, errors = parallel_gather_errors.parallel_gather_errors(risky, data)
    assert results == [1, 9]
    assert len(errors) == 1 and isinstance(errors[0], ValueError)
