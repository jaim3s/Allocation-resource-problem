from scripts.grid import Grid
from scripts.graph import Graph
from scripts.generator import Generator
import matplotlib.pyplot as plt
import random, math, numpy as np


class AdHocNetwork:
    """
    A class to represent an Ad Hoc Network.

        Attributes
        ----------

        width : float
            Width of the grid
        height : float
            Height of the grid
        width_span : float
            Width of the each span
        height_span : float
            Height of the each span
        num_nodes : int
            Number of nodes in the network
        connection_probability : float
            Connection probability between nodes

        Methods
        -------

        validate_kwargs(self, kwargs: dict, valid_kwargs: dict) -> None:
            Validate the key word arguments.
        create_grid(self) -> "Grid":
            Create the grid of the network.
        create_nodes(self) -> "Graph":
            Create the nodes and graph of the network.
        create_edges(self, graph: "Graph") -> None:
            Create the edges of the network.
        create_graph(self) -> "Graph":
            Create the graph of the network.
        install_graph(self) -> None:
            Install the graph in the grid.
        show_network(self) -> None:
            Show the network.
    """

    valid_kwargs = {
        "width"                    : float,
        "height"                   : float,
        "width_span"               : float,
        "height_span"              : float,
        "num_nodes"                : int,
        "connection_probability"   : float,
    }

    def __init__(self, **kwargs: dict) -> None:
        # Validate the kwargs arguments
        self.validate_kwargs(kwargs, self.valid_kwargs) 
        self.rows, self.cols = math.floor(self.height/self.height_span), math.floor(self.width/self.width_span)
        self.grid = self.create_grid()
        self.graph = self.create_graph()
        self.install_graph()

    def validate_kwargs(self, kwargs: dict, valid_kwargs: dict) -> None:
        """
        Validate the key word arguments.

            Parameters
                kwargs (dict): Dictionary with the key word arguments
                valid_kwargs (dict) : Dictionary with the allowed key word arguments
    
            Returns
                return None
        """

        for key in kwargs:
            # Validate key & value
            if valid_kwargs.get(key, None):
                if isinstance(kwargs[key], valid_kwargs[key]):
                    setattr(self, key, kwargs[key])
                else:
                    raise Exception(f"The attributes values ({kwargs[key]}) are invalid.")
            else:
                raise Exception(f"The key ({key}) ins't a valid keyword argument.")

    def create_grid(self) -> "Grid":
        """
        Create the grid of the network.

            Parameters
                None    

            Returns
                return Grid of the network
        """

        return Grid(self.rows, self.cols)

    def create_nodes(self, graph: "Graph") -> None:
        """
        Create the nodes of the network.

            Parameters
                graph ("Graph"): Graph of the network 

            Returns
                return Graph of the network
        """

        generator = Generator(self.num_nodes)
        # Generate random tags and values
        tags = generator.generate_unique_numbers(0, self.num_nodes-1)
        values = generator.generate_numbers(1, self.num_nodes)
        for i in range(self.num_nodes):
            graph.add_node(str(tags[i]), values)
        return graph

    def create_edges(self, graph: "Graph") -> None:
        """
        Create the edges of the network.

            Parameters
                graph ("Graph"): Graph of the network 

            Returns
                return None
        """

        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                if random.random() < self.connection_probability:
                    graph.add_edge(str(i), str(j))

    def create_graph(self) -> "Graph":
        """
        Create the graph of the network.

            Parameters
                None    

            Returns
                return Graph of the network
        """

        graph = Graph()
        self.create_nodes(graph)
        self.create_edges(graph)
        return graph

    def install_graph(self) -> None:
        """
        Install the graph in the grid.

            Parameters
                None

            Returns
                return None
        """

        generator = Generator(self.num_nodes)
        # Generate unique pairs of numbers
        unique_pairs = generator.generate_unique_pairs(0, self.rows-1, 0, self.cols-1)
        for idx, node_tag in enumerate(self.graph.nodes):
            # Assign the position to the nodes and the grid 
            row, col = unique_pairs[idx]
            self.graph.nodes[node_tag].row = row
            self.graph.nodes[node_tag].col = col
            self.grid.values[row][col] = node_tag

    def show_network(self) -> None:
        """
        Show the network.

            Parameters
                None

            Returns
                return None
        """

        plt.figure()
        plt.title(f"Network - {id(self)}")

        plt.xlim(0, self.cols)
        plt.ylim(0, self.rows)

        # Draw nodes
        for node_tag in self.graph.nodes: 
            plt.text(
                x=self.graph.nodes[node_tag].col, 
                y=self.graph.nodes[node_tag].row, 
                s=self.graph.nodes[node_tag].tag, 
                ha='center', 
                va='center', 
                fontsize=20, 
                color='black', 
                bbox=dict(facecolor='none', edgecolor='black', boxstyle='circle')
            )

            for neighbor in self.graph.nodes[node_tag].neighbors:
                plt.plot([self.graph.nodes[node_tag].col, neighbor.col], [self.graph.nodes[node_tag].row, neighbor.row], 'gray', zorder=1)

        plt.show()
