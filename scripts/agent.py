from typing import List, Tuple
import math, random, scripts.constants, numpy as np


class Agent:
    """
    A class to represent a agent.

        Attributes
        ----------

        tag : str
            Tag/id of the agent
        value : float
            Value of the agent
        radius : float
            Radius of the agent
        neighbors : list
            List of neighbor agents
        row : int
            Row position of the agent
        col : int
            Column position of the agent
        old_rows : List[int]
            List of old row positions of the agent
        old_cols : List[int]
            List of old column positions of the agent
        tasks : list
            List of tasks
        selected_tasks : List["Task"]
            List of selected tasks
        state : int
            Define the state of the agent
                state (0) -> The agent is not working

        Methods
        -------

        __str__(self) -> str:
            Represents the agent in a string format.
        __repr__(self) -> str:
            Represents the agent in a string format for data structures.
        add_neighbor(self, neighbor: "agent") -> None:
            Add a new agent to the neighbors list.
        remove_neighbor(self, neighbor: "agent") -> None:
            Remove a agent from the neighbors list.
        is_bidirectional(self, neighbor: "agent") -> bool:
            Check if the agent is bidirectional.
        in_neighborhood(self, x_pos: int, y_pos: int) -> bool:
            Check if the other agent is inside the agent radius.
        check_in_limits(self, rows: int, cols: int, new_row: int, new_col: int) -> bool:
            Check if the new position is in the limits.
        check_physical_collisions(self, agents: List["Agent"], new_row: int, new_col: int) -> bool:
            Check if the agent collide with other agent.
        brownian_motion(self, rows: int, cols: int, agents: List["Agent"], step_size: int) -> Tuple[int, int]:
            Brownian motion for the agent.
        update_position(self, new_row: int, new_col: int) -> None:
            Update the position of the agent.
        assign_task(self, task: "Task") -> None:
            Assign the task to the agent.
        get_selected_tasks(self, selected_tasks: List[List[float]]) -> List[int]:
            Get the selected tasks of the agent.
        get_allocation_resources_score(self) -> Tuple[float, list]:
            Get the best allocation score and the list of selected tasks.
    """

    def __init__(self, tag: str, value: float, radius: float) -> None:
        self.tag = tag
        self.value = value
        self.radius = radius
        self.neighbors = []
        self.tasks = []
        self.selected_tasks = []
        self.state = 0
        self.row, self.col = None, None
        self.old_rows, self.old_cols = [], [] 

    def __str__(self) -> str:
        """
        Represents the agent in a string format.

            Parameters
                None
    
            Returns
                return The string format of the agent
        """

        return "(" + str(self.tag) + ", " + str(self.value) + ")"

    def __repr__(self) -> str:
        """
        Represents the agent in a string format for data structures.

            Parameters
                None
    
            Returns
                return The string format of the agent
        """

        return "(" + str(self.tag) + ", " + str(self.value) + ")"

    def add_neighbor(self, neighbor: "agent") -> None:
        """
        Add a new agent to the neighbors list.

            Parameters
                neighbor ("agent"): New agent in the the neighbors list
    
            Returns
                return None
        """

        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor: "agent") -> None:
        """
        Remove a agent from the neighbors list.

            Parameters
                neighbor ("agent"): agent for remove from the neighbors list
    
            Returns
                return None
        """

        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)

    def is_bidirectional(self, neighbor: "agent") -> bool:
        """
        Check if the agent is bidirectional.

            Parameters
                neighbor ("agent"): agent for remove from the neighbors list
    
            Returns
                return None
        """

        return self in neighbor.neighbors

    def in_neighborhood(self, x_pos: int, y_pos: int) -> bool:
        """
        Check if the other agent is inside the agent radius.

            Parameters
                x_pos (int): x position of the agent
                y_pos (int): y position of the agent
    
            Returns
                return True if the agent is in the neighborhood otherwise False
        """

        return math.sqrt((x_pos - self.col)**2 + (y_pos - self.row)**2) <= self.radius

    def check_in_limits(self, rows: int, cols: int, new_row: int, new_col: int) -> bool:
        """
        Check if the new position is in the limits.

            Parameters
                rows (int): Number of rows
                cols (int): Number of columns
                new_row (int): New row position
                new_col (int): New col position

            Returns
                return True if the new position is in the limits otherwise False
        """

        return (0 <= new_row < rows) and (0 <= new_col < cols)

    def check_physical_collisions(self, agents: List["Agent"], new_row: int, new_col: int) -> bool:
        """
        Check if the agent collide with other agent.

            Parameters
                agents (List["Agent"]): List of agents
                new_row (int): New row position
                new_col (int): New col position

            Returns
                return True if the agent collide with other agent otherwise False
        """

        for agent in agents:
            if new_row == agent.row and new_col == agent.col:
                return True
        return False

    def brownian_motion(self, rows: int, cols: int, agents: List["Agent"], step_size: int) -> Tuple[int, int]:
        """
        Brownian motion for the agent.

            Parameters
                rows (int): Number of rows
                cols (int): Number of columns
                agents (List["Agent"]): List of agents
                step_size (int): Size of each step

            Returns
                return The new agent position based on the brownian motion
        """

        # Perform Brownian motion simulation
        dx = random.choice(scripts.constants.MOBILITY_ACTIONS) * step_size
        dy = random.choice(scripts.constants.MOBILITY_ACTIONS) * step_size
        new_row, new_col = self.row+dx, self.col+dy
        while (self.check_in_limits(rows, cols, new_row, new_col) == False) or (self.check_physical_collisions(agents, new_row, new_col) == True):
            dx = random.choice(scripts.constants.MOBILITY_ACTIONS) * step_size
            dy = random.choice(scripts.constants.MOBILITY_ACTIONS) * step_size
            new_row, new_col = self.row+dx, self.col+dy
        return new_row, new_col

    def update_position(self, new_row: int, new_col: int) -> None:
        """
        Update the position of the agent.

            Parameters
                new_row (int): New row position of the agent
                new_col (int): New column position of the agent

            Returns
                return None
        """

        if self.row and self.col:
            self.old_rows.append(self.row+1)
            self.old_cols.append(self.col+1)
        self.row, self.col = new_row, new_col

    def assign_task(self, task: "Task") -> None:
        """
        Assign the task to the agent.

            Parameters
                task ("Task"): The task to assign

            Returns
                return None
        """

        self.selected_tasks.append(task)
        self.value -= task.size

    def get_selected_tasks(self, selected_tasks: List[List[float]]) -> List[int]:
        """
        Get the selected tasks of the agent.

            Parameters
                selected_tasks (List[List[float]]): List of selected tasks

            Returns
                return A list with the selected tasks
        """

        result_tasks, w = [], self.value
        for i in range(len(self.tasks)-1, -1, -1):
            if selected_tasks[i][w]:
                result_tasks.append(i)
                w -= self.tasks[i].size
        return result_tasks
        
    def get_allocation_resources_score(self) -> Tuple[float, list]:
        """
        Get the best allocation score and the list of selected tasks.

            Parameters
                None

            Returns
                return Tuple with the best allocation resources score and the list of selected tasks
        """

        dp = [0]*(self.value+1)
        selected_tasks = [[False]*(self.value+1) for _ in range(len(self.tasks))]
        for i in range(1, len(self.tasks)+1):
            for w in range(self.value, 0, -1):
                if self.tasks[i-1].size <= w and dp[w] < dp[w-self.tasks[i-1].size]+self.tasks[i-1].value:
                    dp[w] = dp[w-self.tasks[i-1].size]+self.tasks[i-1].value
                    selected_tasks[i-1][w] = True
        return dp[self.value], self.get_selected_tasks(selected_tasks)
