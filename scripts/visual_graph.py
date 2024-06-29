import matplotlib.pyplot as plt
from typing import List

class VisualGraph:
    """
    A class to represent the visual graph.

        Attributes
        ----------

        title : str
            Title of the visual graph
        limit_x : int
            Limit of the x axis
        limit_y : int
            Limit of the y axis
        agents : List["Agent"]
            List with the agents (nodes)
        save_path : str
            Path for save the visual graph
        filename : str
            Name of the visual graph file

        Methods
        -------
        
        update_frame(frame: int, ) -> tuple: 
            Update the informatin of the next frame.
        show_visual_graph(self) -> None:
            Show the visual graph.
    """

    def __init__(self, title: str, limit_x: int, limit_y: int, agents: List["Agent"], save_path: str, filename: str) -> None:
        self.title = title 
        self.limit_x = limit_x
        self.limit_y = limit_y
        self.agents = agents
        self.save_path = save_path
        self.filename = filename

    def update_frame(frame: int, ) -> tuple: 
        """
        Update the informatin of the next frame.

            Parameters
                frame (int): Current frame

            Returns
                return Tuple with the text matplotlib object and None value
        """

        # Update text position
        for agent in self.agents:
            agent.col = frame*0.1
        text.set_position((agent_col, 5))
        return text,

    def show_visual_graph(self) -> None:
        """
        Show the visual graph.

            Parameters
                None

            Returns
                return None
        """

        # Create a figure and axis
        fig, ax = plt.subplots()

        ax.set_title(f"Network - {self.title}")

        # Set x and y axis
        ax.set_xlim(0, self.limit_x)
        ax.set_ylim(0, self.limit_y)

        ax.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray")

        # Add invisible points with labels
        plt.plot([], [], " ", label="asd")

        plt.legend()

        agents_text_nodes = []

        # Draw agents
        for agent in self.agents:
            x, y = agent.col+1, agent.row+1

            # Get the agent text node
            agent_text_node = ax.text(
                x=x, 
                y=y, 
                s=agent.tag, 
                ha="center", 
                va="center", 
                fontsize=12, 
                color="black", 
                bbox=dict(facecolor="none", edgecolor="black", boxstyle="circle")
            )

            agents_text_nodes.append(agent_text_node)

            circle = plt.Circle((x, y), agent.radius, color="red", fill=False, linestyle="--")
            ax.add_artist(circle)

            for neighbor in agent.neighbors:
                ax.annotate("", xy=(neighbor.col+1, neighbor.row+1), xytext=(x, y),
                    arrowprops=dict(arrowstyle="->"))

        plt.savefig(self.save_path + f"\\{self.filename}")
        
        plt.show()

