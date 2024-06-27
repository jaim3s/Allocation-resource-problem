from typing import List, Tuple
import math

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
        tasks : list
            List of tasks
        selected_tasks : list
            List of selected tasks

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
        in_neighborhood(self, x_pos: int, y_pos: int) -> bool:
            Check if the other agent is inside the agent radius.
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
        self.row, self.col = None, None

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

        dp = [0 for i in range(self.value+1)]
        selected_tasks = [[False for _ in range(self.value+1)] for _ in range(len(self.tasks))]
        for i in range(1, len(self.tasks)+1):
            for w in range(self.value, 0, -1):
                if self.tasks[i-1].size <= w and dp[w] < dp[w-self.tasks[i-1].size]+self.tasks[i-1].value:
                    dp[w] = dp[w-self.tasks[i-1].size]+self.tasks[i-1].value
                    selected_tasks[i-1][w] = True
        return dp[self.value], self.get_selected_tasks(selected_tasks)
