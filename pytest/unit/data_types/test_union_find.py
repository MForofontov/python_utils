from data_types.union_find import UnionFind


def test_find_initializes_new_element():
    """
    Test case 1: Find initializes new element.
    """
    uf: UnionFind[int] = UnionFind()

    assert uf.find(42) == 42
    # Calling find again should return the same representative without raising
    assert uf.find(42) == 42


def test_find_handles_multiple_new_elements():
    """
    Test case 2: Find handles multiple new elements.
    """
    uf: UnionFind[str] = UnionFind()

    assert uf.find("alpha") == "alpha"
    assert uf.find("beta") == "beta"
    assert not uf.connected("alpha", "beta")


def test_union_merges_sets_and_connected_reflects_union():
    """
    Test case 3: Union merges sets and connected reflects the union.
    """
    uf: UnionFind[int] = UnionFind()

    uf.union(1, 2)

    assert uf.connected(1, 2)
    assert uf.find(1) == uf.find(2)


def test_union_by_rank_prefers_higher_rank_root():
    """
    Test case 4: Union by rank attaches the lower ranked tree to the higher.
    """
    uf: UnionFind[int] = UnionFind()

    uf.union(1, 2)
    uf.union(3, 4)

    # Both sets should now have rank 1.
    assert uf.rank[uf.find(1)] == 1
    assert uf.rank[uf.find(3)] == 1

    uf.union(1, 3)

    root = uf.find(1)
    assert uf.find(2) == root
    assert uf.find(3) == root
    assert uf.find(4) == root
    assert uf.rank[root] == 2


def test_find_applies_path_compression():
    """
    Test case 5: Find applies path compression to flatten the structure.
    """
    uf: UnionFind[int] = UnionFind()

    uf.union(10, 20)
    uf.union(20, 30)

    root_before = uf.find(10)
    assert uf.find(30) == root_before
    # After calling find, parent of 30 should be the root due to path compression
    assert uf.parent[30] == root_before
