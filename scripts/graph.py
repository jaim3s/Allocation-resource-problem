from scripts.node import Node


class Graph:
    """
    A class to represent a graph.

        Attributes
        ----------

        nodes : dict
            Dictionary with the graph nodes

        Methods
        -------

        __str__(self) -> str:
            Represents the graph in a string format.
        __repr__(self) -> str:
            Represents the graph in a string format for data structures.
        add_node(self, tag: str, value: object) -> None:
            Add a new node to the graph.
        add_edge(self, tag1: str, tag2: str) -> None:
            Add a new edge to the graph.
        remove_node(self, tag: str) -> None:
            Remove a node from the graph.
        remove_edge(self, tag1: str, tag2: str) -> None:
            Remove an edge from the graph.
        display(self) -> None:
            Display the graph nodes.
        bfs(self, start_value: str) -> None:
            BFS (Breadth first search).
        dfs(self, start_value: str) -> None:
            DFS (Depth first search).
    """

    def __init__(self):
        self.nodes = {}

    def __str__(self) -> str:
        """
        Represents the graph in a string format.

            Parameters
                None
    
            Returns
                return The string format of the graph
        """

        return str(self.nodes)

    def __repr__(self) -> str:
        """
        Represents the graph in a string format for data structures.

            Parameters
                None
    
            Returns
                return The string format of the graph
        """

        return str(self.nodes)

    def add_node(self, tag: str, value: object) -> None:
        """
        Add a new node to the graph.

            Parameters
                tag (str): Tag/id of the node
                value (object): Value of the node
    
            Returns
                return None
        """

        if tag not in self.nodes:
            self.nodes[tag] = Node(tag, value)

    def add_edge(self, tag1: str, tag2: str) -> None:
        """
        Add a new edge to the graph.

            Parameters
                tag1 (str): Tag/id of the first node
                tag1 (str): Tag/id of the second node
    
            Returns
                return None
        """

        if tag1 in self.nodes and tag2 in self.nodes:
            self.nodes[tag1].add_neighbor(self.nodes[tag2])
            self.nodes[tag2].add_neighbor(self.nodes[tag1])

    def remove_node(self, tag: str) -> None:
        """
        Remove a node from the graph.

            Parameters
                tag (str): Tag/id of the node
    
            Returns
                return None
        """

        if tag in self.nodes:
            node_to_remove = self.nodes[tag]
            for neighbor in node_to_remove.neighbors:
                neighbor.remove_neighbor(node_to_remove)
            del self.nodes[tag]

    def remove_edge(self, tag1: str, tag2: str) -> None:
        """
        Remove an edge from the graph.

            Parameters
                tag1 (str): Tag/id of the first node
                tag1 (str): Tag/id of the second node
    
            Returns
                return None
        """

        if tag1 in self.nodes and tag2 in self.nodes:
            self.nodes[tag1].remove_neighbor(self.nodes[tag2])
            self.nodes[tag2].remove_neighbor(self.nodes[tag1])

    def display(self) -> None:
        """
        Display the graph nodes.

            Parameters
                None    

            Returns
                return None
        """

        for node in self.nodes.values():
            neighbors = [neighbor.tag for neighbor in node.neighbors]
            print(f"{node.tag}: {neighbors}")

    def bfs(self, start_value: str) -> None:
        """
        BFS (Breadth first search).

            Parameters
                start_value (str): Initial node

            Returns
                return None
        """

        if start_value not in self.nodes:
            return

        visited = set()
        queue = [self.nodes[start_value]]

        while queue:
            node = queue.pop(0)
            if node not in visited:
                print(node, end=" ")
                visited.add(node)
                queue.extend(set(node.neighbors) - visited)
        print()

    def dfs(self, start_value: str) -> None:
        """
        DFS (Depth first search).

            Parameters
                start_value (str): Initial node

            Returns
                return None
        """

        if start_value not in self.nodes:
            return

        visited = set()
        stack = [self.nodes[start_value]]

        while stack:
            node = stack.pop()
            if node not in visited:
                print(node, end=" ")
                visited.add(node)
                stack.extend(set(node.neighbors) - visited)
        print()
