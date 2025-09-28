from data_types.union_find import UnionFind


def test_find_initializes_new_element():
    uf: UnionFind[int] = UnionFind()

    assert uf.find(42) == 42
    # Calling find again should return the same representative without raising
    assert uf.find(42) == 42


def test_find_handles_multiple_new_elements():
    uf: UnionFind[str] = UnionFind()

    assert uf.find("alpha") == "alpha"
    assert uf.find("beta") == "beta"
    assert not uf.connected("alpha", "beta")
