import multiprocessing_functions.parallel_map as pm


def double(x: int) -> int:
    return x * 2


def test_parallel_map_cpu_count_minimum(monkeypatch) -> None:
    monkeypatch.setattr(pm, "cpu_count", lambda: 1)
    assert pm.parallel_map(double, [1, 2, 3]) == [2, 4, 6]

