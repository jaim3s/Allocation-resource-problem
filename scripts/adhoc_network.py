from scripts.grid import Grid
from scripts.graph import Graph
from scripts.task import Task
from scripts.generator import Generator
from typing import List
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
        num_agents : int
            Number of agents in the network
        connection_probability : float
            Connection probability between agents

        Methods
        -------

        validate_kwargs(self, kwargs: dict, valid_kwargs: dict) -> None:
            Validate the key word arguments.
        create_grid(self) -> "Grid":
            Create the grid of the network.
        create_agents(self) -> "Graph":
            Create the agents and graph of the network.
        create_edges(self, graph: "Graph") -> None:
            Create the edges of the network.
        create_graph(self) -> "Graph":
            Create the graph of the network.
        install_graph(self) -> None:
            Install the graph in the grid.
        show_network(self) -> None:
            Show the network.
        create_tasks(self, m: int, min_size: int, max_size: int, min_value: int, max_value: int) -> List["Task"]:
            Create tasks.
        assign_tasks(self) -> None:
            Assign tasks to the agents.
        run(self) -> None:
            Run the Ad Hoc Network.
    """

    valid_kwargs = {
        "width"                    : float,
        "height"                   : float,
        "width_span"               : float,
        "height_span"              : float,
        "connection_probability"   : float,
        "num_agents"                : int,
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

    def create_agents(self, graph: "Graph") -> None:
        """
        Create the agents of the network.

            Parameters
                graph ("Graph"): Graph of the network 

            Returns
                return Graph of the network
        """

        generator = Generator(self.num_agents)
        # Generate random tags and values
        tags = generator.generate_unique_numbers(0, self.num_agents-1)
        values = generator.generate_numbers(1, self.num_agents)
        for i in range(self.num_agents):
            graph.add_agent(str(tags[i]), values[i])
        return graph

    def create_edges(self, graph: "Graph") -> None:
        """
        Create the edges of the network.

            Parameters
                graph ("Graph"): Graph of the network 

            Returns
                return None
        """

        for i in range(self.num_agents):
            for j in range(i+1, self.num_agents):
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
        self.create_agents(graph)
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

        generator = Generator(self.num_agents)
        # Generate unique pairs of numbers
        unique_pairs = generator.generate_unique_pairs(0, self.rows-1, 0, self.cols-1)
        for idx, agent_tag in enumerate(self.graph.agents):
            # Assign the position to the agents and the grid 
            row, col = unique_pairs[idx]
            self.graph.agents[agent_tag].row = row
            self.graph.agents[agent_tag].col = col
            self.grid.values[row][col] = agent_tag

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

        # Draw agents
        for agent_tag in self.graph.agents: 
            plt.text(
                x=self.graph.agents[agent_tag].col, 
                y=self.graph.agents[agent_tag].row, 
                s=self.graph.agents[agent_tag].tag, 
                ha='center', 
                va='center', 
                fontsize=20, 
                color='black', 
                bbox=dict(facecolor='none', edgecolor='black', boxstyle='circle')
            )

            for neighbor in self.graph.agents[agent_tag].neighbors:
                plt.plot([self.graph.agents[agent_tag].col, neighbor.col], [self.graph.agents[agent_tag].row, neighbor.row], 'gray', zorder=1)

        plt.show()

    def create_tasks(self, m: int, min_size: int, max_size: int, min_value: int, max_value: int) -> List["Task"]:
        """
        Create tasks.

            Parameters
                m (int): Number of tasks
                min_size (int): Minimal size of tasks
                max_size (int): Maximal size of tasks
                min_value (int): Minimal value of tasks
                max_value (int): Maximal value of tasks

            Returns
                return List of tasks
        """

        return [Task(random.randint(min_size, max_size), random.randint(min_value, max_value)) for i in range(m)]

    def assign_tasks(self) -> None:
        """
        Assign tasks to the agents.

            Parameters
                None

            Returns
                return None
        """

        max_value = self.graph.get_max_value()
        num_groups = 3
        tasks = self.create_tasks(self.num_agents*num_groups, 1, max_value, 1, 100)
        for agent in self.graph.agents:
            self.graph.agents[agent].tasks = tasks

    def check_collisions(self, agents_results: dict) -> None:
        """
        Check for collisions in task selections.

            Parameters
                agents_results (dict): Dictionary with the agents results

            Returns
                return None
        """

        tasks_counter = {}
        for agent in agents_results:
            for task_idx in agents_results[agent]["selected_tasks"]:
                # The task doesn't exist in the counter
                if tasks_counter.get(task_idx, None) == None:
                    tasks_counter[task_idx] = 1
                else:
                    tasks_counter[task_idx] += 1
        for task_idx in tasks_counter: 
            if tasks_counter[task_idx] > 1:
                print(task_idx, tasks_counter[task_idx])

    def run(self) -> None:
        """
        Run the Ad Hoc Network.


            Parameters
                None

            Returns
                return None
        """

        self.assign_tasks()
        agents_results = {}
        print(self.graph.agents["1"].tasks)
        for agent in self.graph.agents:
            best_allocation_score, selected_tasks = self.graph.agents[agent].get_allocation_resources_score()
            agents_results[agent] = dict()
            agents_results[agent]["score"] = best_allocation_score
            agents_results[agent]["selected_tasks"] = selected_tasks
            print(self.graph.agents[agent], agents_results[agent]["selected_tasks"])
        self.check_collisions(agents_results)