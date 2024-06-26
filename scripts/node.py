class Node:
    """
    A class to represent a node.

        Attributes
        ----------

        tag : str
            Tag/id of the node
        value : object
            Value of the node
        neighbors : list
            List of neighbor nodes
        row : int
            Row position of the node
        col : int
            Column position of the node
        tasks : list
            List of tasks

        Methods
        -------

        __str__(self) -> str:
            Represents the node in a string format.
        __repr__(self) -> str:
            Represents the node in a string format for data structures.
        add_neighbor(self, neighbor: "Node") -> None:
            Add a new node to the neighbors list.
        remove_neighbor(self, neighbor: "Node") -> None:
            Remove a node from the neighbors list.
    """

    def __init__(self, tag: str, value: object) -> None:
        self.tag = tag
        self.value = value
        self.neighbors = []
        self.tasks = []
        self.row, self.col = None, None

    def __str__(self) -> str:
        """
        Represents the node in a string format.

            Parameters
                None
    
            Returns
                return The string format of the node
        """

        return "(" + str(self.tag) + ", " + str(self.value) + ")"

    def __repr__(self) -> str:
        """
        Represents the node in a string format for data structures.

            Parameters
                None
    
            Returns
                return The string format of the node
        """

        return "(" + str(self.tag) + ", " + str(self.value) + ")"

    def add_neighbor(self, neighbor: "Node") -> None:
        """
        Add a new node to the neighbors list.

            Parameters
                neighbor ("Node"): New node in the the neighbors list
    
            Returns
                return None
        """

        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor: "Node") -> None:
        """
        Remove a node from the neighbors list.

            Parameters
                neighbor ("Node"): Node for remove from the neighbors list
    
            Returns
                return None
        """

        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
