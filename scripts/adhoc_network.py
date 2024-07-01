from scripts.grid import Grid
from scripts.graph import Graph
from scripts.task import Task
from scripts.generator import Generator
from scripts.visual_graph import VisualGraph
from typing import List
import time, random, math, os, sys, scripts.constants, numpy as np, pandas as pd


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
        iterations : int
            Number of iterations of the simulation
        mobility_model : str
            Mobility model of the agents in the network
        generator : "Generator"
            Generator of random numbers
        visual_graph : "VisualGraph"
            Visual graph object

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
        remove_edges(self, graph: "Graph") -> None:
            Remove the edges of the network.
        brownian_motion(self, step_size: int) -> None:
            Apply the brownian motion mobility model.
        create_tasks(self, min_size: int, max_size: int, min_value: int, max_value: int) -> List["Task"]:
            Create tasks objects.
        create_initial_tasks(self) -> None:
            Assign tasks to the agents.
        save_tasks(self, tasks, filename: str) -> None:
            Save the tasks of the network.
        count_collisions(self, agents_results: dict) -> dict:
            Get the agents in the selected tasks.
        check_collisions(self, tasks_counter: dict) -> bool:
            Check the collisions in the selected tasks.
        join_tasks(self, group: List["Agent"]) -> List["Task"]:
            Join the tasks of the group
        assign_tasks(self, group: List["Agent"], tasks: List["Task"]) -> List["Task"]:
            Assign the tasks to the agents in the group.
        merge(self, tasks: List["Task"], all_selected_tasks: List[tuple], left: int, mid: int, right: int):
            Merge the lists of selected tasks under the conditions.
        merge_sort_tasks(self, tasks: List["Task"], all_selected_tasks: List[tuple], begin: int, end: int) -> None:
            Merge sort the selected tasks of the group of agents.
        initialization(self) -> None:
            Initialize the Ad Hoc Network.
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
        "iterations"               : int,
        "mobility_model"           : str,
    }

    def __init__(self, **kwargs: dict) -> None:
        # Validate the kwargs arguments
        self.validate_kwargs(kwargs, self.valid_kwargs)
        self.initialization()

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
        tags = self.generator.generate_unique_integer_numbers(0, self.num_agents-1)
        values = self.generator.generate_integer_numbers(1, self.num_agents)
        radius = self.generator.generate_float_numbers(3, 3, 0)
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
        for idx, agent in enumerate(graph.agents):
            # Assign the position to the agents and the grid 
            row, col = unique_pairs[idx]
            graph.agents[agent].update_position(row, col)
            self.grid.values[row][col] = agent

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
                    if self.generator.generate_random_number() < self.connection_probability:
                        graph.add_edge(agent1, agent2)

    def remove_edges(self, graph: "Graph") -> None:
        """
        Remove the edges of the network.

            Parameters
                graph ("Graph"): Graph of the network 

            Returns
                return None
        """

        for agent in graph.agents:
            graph.agents[agent].neighbors = []

    def brownian_motion(self, step_size: int) -> None:
        """
        Apply the brownian motion mobility model.

            Parameters
                step_size (int): Size of each step

            Returns
                return None
        """

        agents = list(self.graph.agents.values())
        for agent in self.graph.agents:
            new_row, new_col = self.graph.agents[agent].brownian_motion(self.rows, self.cols, agents, step_size)
            self.graph.agents[agent].update_position(new_row, new_col)

    def create_tasks(self, min_size: int, max_size: int, min_value: int, max_value: int, min_time: float, max_time: float) -> List["Task"]:
        """
        Create tasks objects.

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

    def create_initial_tasks(self) -> None:
        """
        Assign tasks to the agents.

            Parameters
                None

            Returns
                return None
        """

        max_value = self.graph.get_max_value()
        for agent in self.graph.agents:
            self.graph.agents[agent].tasks = self.create_tasks(1, max_value, 1, 100, 60, 120)

    def save_tasks(self, filename: str, tasks: List["Task"]) -> None:
        """
        Save the tasks of the network.

            Parameters
                filename (str): Name of the task file
                tasks (List["Task"]): List of tasks

            Returns
                return None
        """

        pd.DataFrame([
            (task.size, task.value, task.time) for task in tasks
        ]).to_csv(self.log_path + f"\\{filename}", index=False)

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

    def join_tasks(self, group: List["Agent"]) -> List["Task"]:
        """
        Join the tasks of the group

            Parameters
                group (List["Agent"]): Join the tasks of the group

            Returns
                return List with the tasks joinedj
        """

        joined_tasks = []
        for agent in group:
            joined_tasks.extend(agent.tasks)
            joined_tasks.extend(agent.selected_tasks)
        return joined_tasks

    def assign_tasks(self, group: List["Agent"], tasks: List["Task"]) -> List["Task"]:
        """
        Assign the tasks to the agents in the group.

            Parameters
                group (List["Agent"]): Join the tasks of the group
                tasks (List["Task"]): List of tasks

            Returns
                return List with the tasks joinedj
        """

        for agent in group:
            agent.tasks = tasks

    def merge(self, tasks: List["Task"], all_selected_tasks: List[tuple], left: int, mid: int, right: int):
        """
        Merge the lists of selected tasks under the conditions.

            Parameters
                tasks (List["Task"]): List of tasks
                all_selected_tasks (List[tuple]): The selected tasks
                left (int): Initial index
                mid (int): Mid index
                right (int): Last index

            Returns
                return None
        """

        sub_list_1 = mid-left+1
        sub_list_2 = right-mid

        # Create temporal lists
        left_list = [0]*sub_list_1
        right_list = [0]*sub_list_2

        # Copy data to temporal lists left_list[] and right_list[]
        for i in range(sub_list_1):
            left_list[i] = all_selected_tasks[left + i]
        for j in range(sub_list_2):
            right_list[j] = all_selected_tasks[mid + 1 + j]

        idx_sub_list_1 = 0  # Initial index of first sub-array
        idx_sub_list_2 = 0  # Initial index of second sub-array
        idx_merged_list = left  # Initial index of merged array

        # Merge the temporal lists back into all_selected_tasks[left..right]
        while idx_sub_list_1 < sub_list_1 and idx_sub_list_2 < sub_list_2:
            # Left task have more collisions than right task
            if len(left_list[idx_sub_list_1][1]) > len(right_list[idx_sub_list_2][1]):
                all_selected_tasks[idx_merged_list] = left_list[idx_sub_list_1]
                idx_sub_list_1 += 1
            # Same number of collisions
            elif len(left_list[idx_sub_list_1][1]) == len(right_list[idx_sub_list_2][1]):
                # Compare attributes
                size_comparison = tasks[left_list[idx_sub_list_1][0]].size > tasks[right_list[idx_sub_list_2][0]].size
                value_comparison = tasks[left_list[idx_sub_list_1][0]].value > tasks[right_list[idx_sub_list_2][0]].value
                # The left task is better than the right task
                if size_comparison == False and value_comparison == True:
                    all_selected_tasks[idx_merged_list] = left_list[idx_sub_list_1]
                    idx_sub_list_1 += 1
                # The right task is better than the left task
                elif size_comparison == True and value_comparison == False:
                    all_selected_tasks[idx_merged_list] = right_list[idx_sub_list_2]
                    idx_sub_list_2 += 1
                else:
                    all_selected_tasks[idx_merged_list] = left_list[idx_sub_list_1]
                    idx_sub_list_1 += 1
            else:
                all_selected_tasks[idx_merged_list] = right_list[idx_sub_list_2]
                idx_sub_list_2 += 1
            idx_merged_list += 1

        # Copy the remaining elements of left[], if any
        while idx_sub_list_1 < sub_list_1:
            all_selected_tasks[idx_merged_list] = left_list[idx_sub_list_1]
            idx_sub_list_1 += 1
            idx_merged_list += 1

        # Copy the remaining elements of right[], if any
        while idx_sub_list_2 < sub_list_2:
            all_selected_tasks[idx_merged_list] = right_list[idx_sub_list_2]
            idx_sub_list_2 += 1
            idx_merged_list += 1

    def merge_sort_tasks(self, tasks: List["Task"], all_selected_tasks: List[tuple], begin: int, end: int) -> None:
        """
        Merge sort the selected tasks of the group of agents.

            Parameters
                tasks (List["Task"]): List of tasks
                all_selected_tasks (List[tuple]): The selected tasks
                begin (int): Initial index
                end (int): Last index

            Returns
                return None
        """

        if begin >= end:
            return
        mid = begin+(end-begin)//2
        self.merge_sort_tasks(tasks, all_selected_tasks, begin, mid)
        self.merge_sort_tasks(tasks, all_selected_tasks, mid+1, end)
        self.merge(tasks, all_selected_tasks, begin, mid, end)

    def initialization(self) -> None:
        """
        Initialize the Ad Hoc Network.

            Parameters
                None

            Returns
                return None
        """

        # Create paths and folders for save the content
        self.create_paths()
        self.create_folders()

        # Generate and set random seed
        if self.seed_id == -1:
            self.seed_id = random.randrange(sys.maxsize)
        random.seed(self.seed_id)

        self.generator = Generator(self.num_agents, self.seed_id)
        self.rows, self.cols = math.floor(self.height/self.height_span), math.floor(self.width/self.width_span)

        # Create the grid, graph, and edges
        self.grid = self.create_grid()
        self.graph = self.create_graph()
        self.install_graph(self.graph)
        self.create_edges(self.graph)
        self.visual_graph = VisualGraph(str(self.seed_id), self.cols+1, self.rows+1, self.graphs_path)

        # Assign the initial tasks to each agent
        self.create_initial_tasks()

    def run(self) -> None:
        """
        Run the Ad Hoc Network.

            Parameters
                None

            Returns
                return None
        """

        log_text = f"Simulation stats\n\nRows: {self.rows}\nColumns: {self.cols}\nNumber of agents: {self.num_agents}\nNumber of tasks: {self.num_tasks}\nAgents:\n\n"

        # Save the initial agents stats
        for agent in self.graph.agents:
            log_text += self.graph.agents[agent].__str__() + "\n"

        start_time_simulation = time.time()

        # Create the list of groups of agents
        groups = self.graph.create_groups()

        # Show the initial configuration of agents in the network
        self.visual_graph.show_visual_graph("network_1.png", groups)

        for i in range(self.iterations):
            log_text += "\n"+"#"*50+f"\n\nIteration: {i}\n\nNumber of groups: {len(groups)}\n"
            groups_cnt = 0
            for group in groups:
                log_text += f"\nGroup: {groups_cnt}\n"  
                # Union each task of the group
                joined_tasks, iterations = self.join_tasks(group), 0
                for agent in group:
                    agent.value += sum([task.size for task in agent.selected_tasks])
                    agent.selected_tasks = []
                # Save the joined tasks as a CSV file
                # self.save_tasks(f"task_group_{groups_cnt}.csv", joined_tasks)
                while joined_tasks != []:
                    iterations += 1
                    # Assign the tasks to the agents of the same group
                    self.assign_tasks(group, joined_tasks)
                    agents_results = {}
                    for agent in group:
                        best_allocation_score, selected_tasks = agent.get_allocation_resources_score()
                        agents_results[agent] = {
                            "score" : best_allocation_score,
                            "selected_tasks" : selected_tasks
                        }
                    tasks_counter = self.count_collisions(agents_results)
                    if self.check_collisions(tasks_counter) == True:
                        # Sort the tasks_counter in function of the number of collisions and attributes
                        all_selected_tasks = list(tasks_counter.items())
                        self.merge_sort_tasks(joined_tasks, all_selected_tasks, 0, len(tasks_counter)-1)
                        sorted_selected_tasks = all_selected_tasks
                        # Select the task with more collisions
                        task_idx, task_agents = sorted_selected_tasks.pop(0)
                        # Sort tasks_agents in function of the value (size)
                        sorted_task_agents = sorted(task_agents, key=lambda agent: agent.value)
                        perfect_agent = False
                        # Check if exist the best agent for the task
                        for agent in sorted_task_agents:
                            # Perfect case
                            if agent.value == joined_tasks[task_idx].size:
                                agent.assign_task(joined_tasks[task_idx])
                                perfect_agent = True
                                break
                        if perfect_agent == False:
                            best_agent = sorted_task_agents.pop()
                            best_agent.assign_task(joined_tasks[task_idx])
                        # Remove the tasksk
                        joined_tasks.pop(task_idx)
                    else:
                        for agent in group:
                            if agents_results[agent]["score"] > 0:
                                for task_idx in agents_results[agent]["selected_tasks"]:
                                    agent.assign_task(joined_tasks[task_idx])
                        break
                total_num_selected_tasks, total_score = 0, 0
                for agent in group:
                    log_text += agent.__str__() + "->" + str(agent.selected_tasks) + "\n"
                    total_num_selected_tasks += len(agent.selected_tasks)
                    total_score += sum([task.value for task in agent.selected_tasks])
                log_text += f"\nGroup stats\nTotal score: {total_score}\nTotal number of tasks: {total_num_selected_tasks}\nIterations: {iterations}\n"
                groups_cnt += 1

            # Move the agents
            if self.mobility_model == "brownian_motion":
                self.brownian_motion(scripts.constants.STEP_SIZE)

            # Update the edges
            self.remove_edges(self.graph)
            self.create_edges(self.graph)

            # Create new possible groups
            groups = self.graph.create_groups()

        log_text += f"\nSimulation finished\nSeed ID: {str(self.seed_id)}\nTime: {str(time.time() - start_time_simulation)}"
        
        self.log(f"log.txt", log_text)

        self.visual_graph.show_visual_graph(f"network_{self.iterations}.png", groups)
        self.visual_graph.movement_graph(f"movement_{self.iterations}.png", groups)
