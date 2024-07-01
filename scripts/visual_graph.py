import random, matplotlib.pyplot as plt
from typing import List
import matplotlib.lines as mlines

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
        save_path : str
            Path for save the visual graph
        colors : List[tuple]
            List of colors (RGB%)

        Methods
        -------
        
        generate_palette(self, n: int) -> List[tuple]:
            Generate a palette of colors.
        update_frame(frame: int, ) -> tuple: 
            Update the informatin of the next frame.
        show_visual_graph(self) -> None:
            Show and save the visual graph.
    """

    def __init__(self, title: str, limit_x: int, limit_y: int, save_path: str) -> None:
        self.title = title 
        self.limit_x = limit_x
        self.limit_y = limit_y
        self.save_path = save_path

    def generate_palette(self, n: int) -> List[tuple]:
        """
        Generate a palette of colors.

            Parameters
                n (int): Number of colors to generate

            Returns
                return Tuple with the text matplotlib object and None value
        """    
        colors = []
        for _ in range(n):
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            colors.append(color)
        return colors

    def update_frame(frame: int) -> tuple: 
        """
        Update the informatin of the next frame.

            Parameters
                frame (int): Current frame

            Returns
                return Tuple with the text matplotlib object and None value
        """

        # Update text position
        for agent in self.groups:
            agent.col = frame*0.1
        text.set_position((agent_col, 5))
        return text,

    def movement_graph(self, filename: str, groups: List[List["Agent"]]) -> None:
        """
        Create and save the movement graph.

            Parameters
                filename (str): Name of the visual graph file
                groups (List[List["Agent"]]): List of groups of agents

            Returns
                return None
        """

        colors = self.generate_palette(len(groups))

        # Create a figure and axis
        fig, ax = plt.subplots()

        ax.set_title(f"{filename[:filename.find('.')].capitalize()} - {self.title}")

        # Set x and y axis
        ax.set_xlim(0, self.limit_x)
        ax.set_ylim(0, self.limit_y)

        ax.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray")

        agents_text_nodes = []

        # Draw groups
        for i in range(len(groups)):
            color = colors[i]
            for agent in groups[i]:
                plt.plot(agent.old_cols, agent.old_rows, label=f"Group {i}", color=color)

        plt.legend()

        plt.savefig(self.save_path + f"\\{filename}")
        
        plt.show()

    def show_visual_graph(self, filename: str, groups: List[List["Agent"]]) -> None:
        """
        Show and save the visual graph.

            Parameters
                filename (str): Name of the visual graph file
                groups (List[List["Agent"]]): List of groups of agents

            Returns
                return None
        """

        colors = self.generate_palette(len(groups))

        # Create a figure and axis
        fig, ax = plt.subplots()

        ax.set_title(f"{filename[:filename.find('.')].capitalize()} - {self.title}")

        # Set x and y axis
        ax.set_xlim(0, self.limit_x)
        ax.set_ylim(0, self.limit_y)

        ax.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray")

        agents_text_nodes = []

        # Draw groups
        for i in range(len(groups)):
            color = colors[i]
            for agent in groups[i]:
                # Add invisible points with labels

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
                    bbox=dict(facecolor=color, edgecolor="black", boxstyle="circle", alpha=0.3)
                )

                agents_text_nodes.append(agent_text_node)

                circle = plt.Circle((x, y), agent.radius, color="red", fill=False, linestyle="--", alpha=0.3)
                ax.add_artist(circle)

                for neighbor in agent.neighbors:
                    ax.annotate("", xy=(neighbor.col+1, neighbor.row+1), xytext=(x, y),
                        arrowprops=dict(arrowstyle="->"))

            plt.plot([], [], color=color, label=f"Group {i}")

        plt.legend()

        plt.savefig(self.save_path + f"\\{filename}")
        
        plt.show()

