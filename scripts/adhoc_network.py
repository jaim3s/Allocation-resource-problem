from scripts.grid import Grid
from scripts.graph import Graph
from scripts.task import Task
from scripts.generator import Generator
from scripts.visual_graph import VisualGraph
from typing import List
import random, math, os, sys, scripts.constants, numpy as np, pandas as pd


class AdHocNetwork:
    """
    A class to represent an Ad Hoc Network.

        Attributes
        ----------

        seed_id : int
            Seed id of the simulation
        width : float
            Width of the grid
        height : float
            Height of the grid
        width_span : float
            Width of the each span
        height_span : float
            Height of the each span
        connection_probability : float
            Connection probability between agents
        num_agents : int
            Number of agents in the network
        num_tasks : int
            Number of tasks
        mobility_model : str
            Mobility model of the agents in the network
        generator : "Generator"
            Generator of random numbers

        Methods
        -------

        validate_kwargs(self, kwargs: dict, valid_kwargs: dict) -> None:
            Validate the key word arguments.
        create_paths(self) -> None:
            Create the paths of the Network.
        create_folders(self) -> None:
            Create the folders of the Network.
        log(self, filename: str, content: str) -> None:
            Create a file to write the given content.
        create_grid(self) -> "Grid":
            Create the grid of the network.
        create_agents(self) -> "Graph":
            Create the agents and graph of the network.
        create_graph(self) -> "Graph":
            Create the graph of the network.
        install_graph(self, graph: "Graph") -> None:
            Install the graph in the grid.
        create_edges(self, graph: "Graph") -> None:
            Create the edges of the network.
        brownian_motion(self, step_size: int) -> None:
            Apply the brownian motion mobility model.
        show_network(self) -> None:
            Show the network.
        create_tasks(self, min_size: int, max_size: int, min_value: int, max_value: int) -> List["Task"]:
            Create tasks.
        assign_tasks(self, tasks) -> None:
            Assign tasks to the agents.
        count_collisions(self, agents_results: dict) -> dict:
            Get the agents in the selected tasks.
        check_collisions(self, tasks_counter: dict) -> bool:
            Check the collisions in the selected tasks.
        run(self) -> None:
            Run the Ad Hoc Network.
    """

    valid_kwargs = {
        "seed_id"                  : int,
        "width"                    : float,
        "height"                   : float,
        "width_span"               : float,
        "height_span"              : float,
        "connection_probability"   : float,
        "num_agents"               : int,
        "num_tasks"                : int,
        "mobility_model"           : str,
    }

    def __init__(self, **kwargs: dict) -> None:
        # Validate the kwargs arguments
        self.validate_kwargs(kwargs, self.valid_kwargs)
        # Create paths and folders
        self.create_paths()
        self.create_folders()
        # Generate a random seed
        if self.seed_id == -1:
            self.seed_id = random.randrange(sys.maxsize)
        random.seed(self.seed_id)
        self.generator = Generator(self.num_agents, self.seed_id)
        self.rows, self.cols = math.floor(self.height/self.height_span), math.floor(self.width/self.width_span)
        self.grid = self.create_grid()
        self.graph = self.create_graph()
        self.install_graph(self.graph)
        self.create_edges(self.graph)
        self.tasks = self.create_tasks(1, self.graph.get_max_value(), 1, 100, 60, 120)
        self.visual_graph = VisualGraph(str(self.seed_id), self.cols+1, self.rows+1, list(self.graph.agents.values()), self.graphs_path, "network.png")

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

    def create_paths(self) -> None:
        """
        Create the paths of the Network.

            Parameters
                None
    
            Returns
                return None
        """

        # Define the parent path
        self.parent_path = scripts.constants.content_folder_path + "\\" + str(self.seed_id)
        self.log_path = self.parent_path + "\\logs"
        self.graphs_path = self.parent_path + "\\graphs"

    def create_folders(self) -> None:
        """
        Create the folders of the Network.

            Parameters
                None
    
            Returns
                return None
        """

        os.makedirs(self.parent_path, exist_ok=True)
        os.makedirs(self.log_path, exist_ok=True)
        os.makedirs(self.graphs_path, exist_ok=True)

    def log(self, filename: str, content: str) -> None:
        """
        Create a file to write the given content.

            Parameters
                filename (str): Name of the logs file
                content (str): Content to write in the log file
    
            Returns
                return None
        """

        with open(self.log_path + f"\\{filename}", "w") as file:
            file.write(content)

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

        # Generate random tags and values
        tags = self.generator.generate_unique_numbers(0, self.num_agents-1)
        values = self.generator.generate_integer_numbers(1, self.num_agents)
        radius = self.generator.generate_float_numbers(5, 5, 0)
        for i in range(self.num_agents):
            graph.add_agent(str(tags[i]), values[i], radius[i])
        return graph
                
    def create_graph(self) -> "Graph":
        """
        Create the graph of the network.

            Parameters
                None    

            Returns
                return Graph of the network
        """

        return self.create_agents(Graph())

    def install_graph(self, graph: "Graph") -> None:
        """
        Install the graph in the grid.

            Parameters
                graph ("Graph"): Graph of the network 

            Returns
                return None
        """

        # Generate unique pairs of numbers
        unique_pairs = self.generator.generate_unique_pairs(0, self.rows-1, 0, self.cols-1)
        for idx, agent_tag in enumerate(graph.agents):
            # Assign the position to the agents and the grid 
            row, col = unique_pairs[idx]
            graph.agents[agent_tag].row = row
            graph.agents[agent_tag].col = col
            self.grid.values[row][col] = agent_tag

    def create_edges(self, graph: "Graph") -> None:
        """
        Create the edges of the network.

            Parameters
                graph ("Graph"): Graph of the network 

            Returns
                return None
        """

        for agent1 in graph.agents:
            for agent2 in graph.agents:
                if agent1 != agent2 and graph.agents[agent1].in_neighborhood(graph.agents[agent2].col, graph.agents[agent2].row) == True:
                    if random.random() < self.connection_probability:
                        graph.add_edge(agent1, agent2)

    def brownian_motion(self, step_size: int) -> None:
        """
        Apply the brownian motion mobility model.

            Parameters
                step_size (int): Size of each step

            Returns
                return None
        """

        for agent in self.graph.agents:
            new_row, new_col = self.graph.agents[agent].brownian_motion(step_size)
            self.graph.agents[agent].update_position(new_row, new_col)

    def show_network(self) -> None:
        """
        Show the network.

            Parameters
                None

            Returns
                return None
        """

        # Create a figure and axis
        fig, ax = plt.subplots()

        ax.set_title(f"Network - {self.seed_id}")

        # Set x and y axis
        ax.set_xlim(0, self.cols+1)
        ax.set_ylim(0, self.rows+1)

        ax.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray")

        # Add invisible points with labels
        plt.plot([], [], " ", label="asd")

        plt.legend()

        # Draw agents
        for agent_tag in self.graph.agents:
            x, y = self.graph.agents[agent_tag].col+1, self.graph.agents[agent_tag].row+1

            # Get the agent node
            agent_node = ax.text(
                x=x, 
                y=y, 
                s=self.graph.agents[agent_tag].tag, 
                ha="center", 
                va="center", 
                fontsize=12, 
                color="black", 
                bbox=dict(facecolor="none", edgecolor="black", boxstyle="circle")
            )

            circle = plt.Circle((x, y), self.graph.agents[agent_tag].radius, color="red", fill=False, linestyle="--")
            ax.add_artist(circle)

            for neighbor in self.graph.agents[agent_tag].neighbors:
                ax.annotate("", xy=(neighbor.col+1, neighbor.row+1), xytext=(x, y),
                    arrowprops=dict(arrowstyle="->"))
        
        plt.savefig(self.graphs_path + "\\network.png")
        plt.show()

    def create_tasks(self, min_size: int, max_size: int, min_value: int, max_value: int, min_time: float, max_time: float) -> List["Task"]:
        """
        Create tasks.

            Parameters
                min_size (int): Minimal size of tasks
                max_size (int): Maximum size of tasks
                min_value (int): Minimal value of tasks
                max_value (int): Maximum value of tasks
                min_time (float): Minimal time of tasks
                max_time (float): Maximum time of tasks

            Returns
                return List of tasks
        """

        return [
            Task(
                random.randint(min_size, max_size),
                random.randint(min_value, max_value),
                random.randint(min_time, max_time)
                ) for i in range(self.num_tasks)
        ]

    def assign_tasks(self, tasks) -> None:
        """
        Assign tasks to the agents.

            Parameters
                tasks (List["Task"]): List of tasks

            Returns
                return None
        """

        for agent in self.graph.agents:
            self.graph.agents[agent].tasks = tasks

    def save_tasks(self, tasks) -> None:
        """
        Save the tasks of the network.

            Parameters
                tasks (List["Task"]): List of tasks

            Returns
                return None
        """

        pd.DataFrame([(task.size, task.value, task.time) for task in tasks]).to_csv(self.log_path + f"\\tasks.csv", index=False)

    def count_collisions(self, agents_results: dict) -> dict:
        """
        Get the agents in the selected tasks.

            Parameters
                agents_results (dict): Dictionary with the agents results

            Returns
                return Dictionary with the agents for each selected task
        """

        tasks_counter = {}
        for agent in agents_results:
            for task_idx in agents_results[agent]["selected_tasks"]:
                # The task doesn"t exist in the counter
                if tasks_counter.get(task_idx, None) == None:
                    tasks_counter[task_idx] = [agent]
                else:
                    tasks_counter[task_idx].append(agent)
        return tasks_counter

    def check_collisions(self, tasks_counter: dict) -> bool:
        """
        Check the collisions in the selected tasks.

            Parameters
                tasks_counter (dict): Dictionary with the agents of each selected task

            Returns
                return True if exist a collision otherwise False
        """

        for task_idx in tasks_counter: 
            if len(tasks_counter[task_idx]) > 1:
                return True
        return False

    def run(self) -> None:
        """
        Run the Ad Hoc Network.


            Parameters
                None

            Returns
                return None
        """

        # Save tasks as a CSV file
        self.save_tasks(self.tasks)

        log_text, iterations = "Simulation stats\nAgents:\n", 0

        for agent in self.graph.agents:
            log_text += self.graph.agents[agent].__str__() + "->" + str(self.graph.agents[agent].selected_tasks) + "\n"

        # Assign the task to each agent
        

        while self.tasks != []:
            iterations += 1
            self.assign_tasks(self.tasks)
            agents_results = {}
            for agent in self.graph.agents:
                best_allocation_score, selected_tasks = self.graph.agents[agent].get_allocation_resources_score()
                agents_results[agent] = dict()
                agents_results[agent]["score"] = best_allocation_score
                agents_results[agent]["selected_tasks"] = selected_tasks
            tasks_counter = self.count_collisions(agents_results)
            if self.check_collisions(tasks_counter) == True:
                # Sort the tasks_counter in function of the number of collisions
                sorted_selected_tasks = sorted(tasks_counter.items(), key=lambda selected_task: len(selected_task[1]), reverse=True)
                # Select the task with more collisions
                task_idx, task_agents = sorted_selected_tasks.pop(0)
                # Sort tasks_agents in function of the value (size)
                sorted_task_agents = sorted(task_agents, key=lambda agent: self.graph.agents[agent].value)
                perfect_agent = False
                # Check if exist the best agent for the task
                for agent in sorted_task_agents:
                    # Perfect case
                    if self.graph.agents[agent].value == self.tasks[task_idx].size:
                        self.graph.agents[agent].assign_task(self.tasks[task_idx])
                        perfect_agent = True
                        break
                if perfect_agent == False:
                    best_agent = sorted_task_agents.pop()
                    self.graph.agents[best_agent].assign_task(self.tasks[task_idx])
                # Remove the tasksk
                self.tasks.pop(task_idx)
            else:
                for agent in self.graph.agents:
                    if agents_results[agent]["score"] > 0:
                        for task_idx in agents_results[agent]["selected_tasks"]:
                            self.graph.agents[agent].assign_task(self.tasks[task_idx])
                break

        log_text += f"\nSimulation finished\nSeed ID: {str(self.seed_id)}\nIterations: {str(iterations)}\nAgents:\n"

        total_num_selected_tasks, total_score = 0, 0
        for agent in self.graph.agents:
            log_text += self.graph.agents[agent].__str__() + "->" + str(self.graph.agents[agent].selected_tasks) + "\n"
            total_num_selected_tasks += len(self.graph.agents[agent].selected_tasks)
            total_score += sum([task.value for task in self.graph.agents[agent].selected_tasks])

        log_text += f"\nGeneral stats\nTotal score: {total_score}\nTotal number of tasks: {total_num_selected_tasks}"

        self.log(f"log.txt", log_text)
