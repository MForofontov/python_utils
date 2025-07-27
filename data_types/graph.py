from typing import TypeVar, Generic

# Define a generic type variable
T = TypeVar("T")


class Graph(Generic[T]):
    """
    A Graph data structure using an adjacency list.

    Attributes
    ----------
    adjacency_list : Dict[T, List[T]]
        The dictionary representing the graph, where keys are vertices and values are lists of adjacent vertices.

    Methods
    -------
    add_vertex(vertex: T) -> None
        Adds a vertex to the graph.
    add_edge(vertex1: T, vertex2: T) -> None
        Adds an edge between two vertices.
    get_neighbors(vertex: T) -> List[T]
        Returns a list of neighbors for a given vertex.
    """

    def __init__(self) -> None:
        """
        Initializes an empty graph.
        """
        self.adjacency_list: dict[T, list[T]] = {}

    def add_vertex(self, vertex: T) -> None:
        """
        Adds a vertex to the graph.

        Parameters
        ----------
        vertex : T
            The vertex to add.
        """
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1: T, vertex2: T) -> None:
        """
        Adds an edge between two vertices.

        Parameters
        ----------
        vertex1 : T
            The first vertex.
        vertex2 : T
            The second vertex.
        """
        if vertex1 not in self.adjacency_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adjacency_list:
            self.add_vertex(vertex2)
        self.adjacency_list[vertex1].append(vertex2)
        self.adjacency_list[vertex2].append(vertex1)

    def get_neighbors(self, vertex: T) -> list[T]:
        """
        Returns a list of neighbors for a given vertex.

        Parameters
        ----------
        vertex : T
            The vertex whose neighbors are to be returned.

        Returns
        -------
        List[T]
            A list of neighbors for the given vertex.
        """
        return self.adjacency_list.get(vertex, [])
