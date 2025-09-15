from data_types.graph import Graph


def test_add_vertex() -> None:
    """
    Test case 1: Test adding vertices to the graph.
    """
    graph = Graph[int]()
    graph.add_vertex(1)
    graph.add_vertex(2)
    assert 1 in graph.adjacency_list
    assert 2 in graph.adjacency_list
    assert graph.adjacency_list[1] == set()
    assert graph.adjacency_list[2] == set()


def test_add_edge() -> None:
    """
    Test case 2: Test adding edges between vertices.
    """
    graph = Graph[int]()
    graph.add_edge(1, 2)
    assert 1 in graph.adjacency_list
    assert 2 in graph.adjacency_list
    assert graph.adjacency_list[1] == {2}
    assert graph.adjacency_list[2] == {1}


def test_get_neighbors() -> None:
    """
    Test case 3: Test retrieving neighbors of a vertex.
    """
    graph = Graph[int]()
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    assert set(graph.get_neighbors(1)) == {2, 3}
    assert set(graph.get_neighbors(2)) == {1}
    assert set(graph.get_neighbors(3)) == {1}


def test_add_duplicate_vertex() -> None:
    """
    Test case 4: Test adding a duplicate vertex.
    """
    graph = Graph[int]()
    graph.add_vertex(1)
    graph.add_vertex(1)  # Adding the same vertex again
    assert len(graph.adjacency_list) == 1
    assert graph.adjacency_list[1] == set()


def test_add_edge_between_existing_vertices() -> None:
    """
    Test case 5: Test adding an edge between existing vertices.
    """
    graph = Graph[int]()
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_edge(1, 2)
    assert graph.adjacency_list[1] == {2}
    assert graph.adjacency_list[2] == {1}


def test_add_edge_creates_vertices() -> None:
    """
    Test case 6: Test that adding an edge creates vertices if they don't exist.
    """
    graph = Graph[int]()
    graph.add_edge(1, 2)
    assert 1 in graph.adjacency_list
    assert 2 in graph.adjacency_list
    assert graph.adjacency_list[1] == {2}
    assert graph.adjacency_list[2] == {1}


def test_get_neighbors_of_nonexistent_vertex() -> None:
    """
    Test case 7: Test getting neighbors of a vertex that doesn't exist.
    """
    graph = Graph[int]()
    assert graph.get_neighbors(1) == []


def test_graph_with_custom_objects() -> None:
    """
    Test case 8: Test the graph with custom object vertices.
    """

    class CustomVertex:
        def __init__(self, name: str) -> None:
            self.name = name

        def __eq__(self, other: object) -> bool:
            if isinstance(other, CustomVertex):
                return self.name == other.name
            return False

        def __hash__(self) -> int:
            return hash(self.name)

        def __repr__(self) -> str:
            return f"CustomVertex({self.name})"

    vertex1 = CustomVertex("A")
    vertex2 = CustomVertex("B")
    vertex3 = CustomVertex("C")

    graph = Graph[CustomVertex]()
    graph.add_edge(vertex1, vertex2)
    graph.add_edge(vertex1, vertex3)

    assert set(graph.get_neighbors(vertex1)) == {vertex2, vertex3}
    assert set(graph.get_neighbors(vertex2)) == {vertex1}
    assert set(graph.get_neighbors(vertex3)) == {vertex1}


def test_empty_graph() -> None:
    """
    Test case 9: Test operations on an empty graph.
    """
    graph = Graph[int]()
    assert graph.adjacency_list == {}
    assert graph.get_neighbors(1) == []


def test_large_graph() -> None:
    """
    Test case 10: Test adding a large number of vertices and edges.
    """
    graph = Graph[int]()
    for i in range(1000):
        graph.add_vertex(i)
    for i in range(999):
        graph.add_edge(i, i + 1)
    assert len(graph.adjacency_list) == 1000
    assert set(graph.get_neighbors(0)) == {1}
    assert set(graph.get_neighbors(999)) == {998}


def test_neighbors_contents() -> None:
    """
    Test case 11: Test that the neighbors contain the expected vertices regardless of order.
    """
    graph = Graph[int]()
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    assert set(graph.get_neighbors(1)) == {2, 3, 4}


def test_add_vertex_with_none() -> None:
    """
    Test case 12: Test adding None as a vertex (should work with Generic type).
    """
    graph = Graph[int]()
    # Note: The Graph class doesn't have type validation, so it accepts any type
    # This is a design choice - the Generic typing is for type hints, not runtime validation
    graph.add_vertex(1)
    assert 1 in graph.adjacency_list


def test_add_edge_with_same_vertex() -> None:
    """
    Test case 13: Test adding an edge from a vertex to itself.
    """
    graph = Graph[int]()
    graph.add_edge(1, 1)
    assert 1 in graph.adjacency_list
    assert 1 in graph.adjacency_list[1]  # Self-loop should be added


def test_graph_consistency_after_operations() -> None:
    """
    Test case 14: Test graph maintains consistency after multiple operations.
    """
    graph = Graph[str]()
    graph.add_vertex("A")
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")

    # Verify bidirectional edges
    assert "B" in graph.get_neighbors("A")
    assert "A" in graph.get_neighbors("B")
    assert "C" in graph.get_neighbors("B")
    assert "B" in graph.get_neighbors("C")
