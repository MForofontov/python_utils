from typing import Dict, List, Any

class Graph:
    """
    A Graph data structure using an adjacency list.

    Attributes
    ----------
    adjacency_list : Dict[Any, List[Any]]
        The dictionary representing the graph, where keys are vertices and values are lists of adjacent vertices.

    Methods
    -------
    add_vertex(vertex)
        Adds a vertex to the graph.
    add_edge(vertex1, vertex2)
        Adds an edge between two vertices.
    get_neighbors(vertex)
        Returns a list of neighbors for a given vertex.
    """

    def __init__(self) -> None:
        """
        Initializes an empty graph.
        """
        self.adjacency_list: Dict[Any, List[Any]] = {}

    def add_vertex(self, vertex: Any) -> None:
        """
        Adds a vertex to the graph.

        Parameters
        ----------
        vertex : Any
            The vertex to add.
        """
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1: Any, vertex2: Any) -> None:
        """
        Adds an edge between two vertices.

        Parameters
        ----------
        vertex1 : Any
            The first vertex.
        vertex2 : Any
            The second vertex.
        """
        if vertex1 not in self.adjacency_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adjacency_list:
            self.add_vertex(vertex2)
        self.adjacency_list[vertex1].append(vertex2)
        self.adjacency_list[vertex2].append(vertex1)

    def get_neighbors(self, vertex: Any) -> List[Any]:
        """
        Returns a list of neighbors for a given vertex.

        Parameters
        ----------
        vertex : Any
            The vertex whose neighbors are to be returned.

        Returns
        -------
        List[Any]
            A list of neighbors for the given vertex.
        """
        return self.adjacency_list.get(vertex, [])
