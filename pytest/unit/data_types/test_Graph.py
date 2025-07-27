from data_types.graph import Graph


def test_add_vertex() -> None:
    """
    Test adding vertices to the graph.
    """
    # Test case 1: Add vertices
    graph = Graph[int]()
    graph.add_vertex(1)
    graph.add_vertex(2)
    assert 1 in graph.adjacency_list
    assert 2 in graph.adjacency_list
    assert graph.adjacency_list[1] == []
    assert graph.adjacency_list[2] == []


def test_add_edge() -> None:
    """
    Test adding edges between vertices.
    """
    # Test case 2: Add edges
    graph = Graph[int]()
    graph.add_edge(1, 2)
    assert 1 in graph.adjacency_list
    assert 2 in graph.adjacency_list
    assert graph.adjacency_list[1] == [2]
    assert graph.adjacency_list[2] == [1]


def test_get_neighbors() -> None:
    """
    Test retrieving neighbors of a vertex.
    """
    # Test case 3: Get neighbors
    graph = Graph[int]()
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    assert graph.get_neighbors(1) == [2, 3]
    assert graph.get_neighbors(2) == [1]
    assert graph.get_neighbors(3) == [1]


def test_add_duplicate_vertex() -> None:
    """
    Test adding a duplicate vertex.
    """
    # Test case 4: Add duplicate vertex
    graph = Graph[int]()
    graph.add_vertex(1)
    graph.add_vertex(1)  # Adding the same vertex again
    assert len(graph.adjacency_list) == 1
    assert graph.adjacency_list[1] == []


def test_add_edge_between_existing_vertices() -> None:
    """
    Test adding an edge between existing vertices.
    """
    # Test case 5: Add edge between existing vertices
    graph = Graph[int]()
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_edge(1, 2)
    assert graph.adjacency_list[1] == [2]
    assert graph.adjacency_list[2] == [1]


def test_add_edge_creates_vertices() -> None:
    """
    Test that adding an edge creates vertices if they don't exist.
    """
    # Test case 6: Add edge creates vertices
    graph = Graph[int]()
    graph.add_edge(1, 2)
    assert 1 in graph.adjacency_list
    assert 2 in graph.adjacency_list
    assert graph.adjacency_list[1] == [2]
    assert graph.adjacency_list[2] == [1]


def test_get_neighbors_of_nonexistent_vertex() -> None:
    """
    Test getting neighbors of a vertex that doesn't exist.
    """
    # Test case 7: Get neighbors of nonexistent vertex
    graph = Graph[int]()
    assert graph.get_neighbors(1) == []


def test_graph_with_custom_objects() -> None:
    """
    Test the graph with custom object vertices.
    """

    # Test case 8: Graph with custom objects
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

    assert graph.get_neighbors(vertex1) == [vertex2, vertex3]
    assert graph.get_neighbors(vertex2) == [vertex1]
    assert graph.get_neighbors(vertex3) == [vertex1]


def test_empty_graph() -> None:
    """
    Test operations on an empty graph.
    """
    # Test case 9: Empty graph
    graph = Graph[int]()
    assert graph.adjacency_list == {}
    assert graph.get_neighbors(1) == []


def test_large_graph() -> None:
    """
    Test adding a large number of vertices and edges.
    """
    # Test case 10: Large graph
    graph = Graph[int]()
    for i in range(1000):
        graph.add_vertex(i)
    for i in range(999):
        graph.add_edge(i, i + 1)
    assert len(graph.adjacency_list) == 1000
    assert graph.get_neighbors(0) == [1]
    assert graph.get_neighbors(999) == [998]


def test_order_of_neighbors() -> None:
    """
    Test that the order of neighbors is preserved.
    """
    # Test case 11: Order of neighbors
    graph = Graph[int]()
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(1, 4)
    assert graph.get_neighbors(1) == [2, 3, 4]
