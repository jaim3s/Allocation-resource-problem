from typing import List, Tuple
from scripts.agent import Agent


class Graph:
    """
    A class to represent a graph.

        Attributes
        ----------

        agents : dict
            Dictionary with the graph agents

        Methods
        -------

        __str__(self) -> str:
            Represents the graph in a string format.
        __repr__(self) -> str:
            Represents the graph in a string format for data structures.
        add_agent(self, tag: str, value: float, radius: float) -> None:
            Add a new agent to the graph.
        add_edge(self, tag1: str, tag2: str) -> None:
            Add a new edge to the graph.
        remove_agent(self, tag: str) -> None:
            Remove a agent from the graph.
        remove_edge(self, tag1: str, tag2: str) -> None:
            Remove an edge from the graph.
        display(self) -> None:
            Display the graph agents.
        bfs(self, start_value: str) -> None:
            BFS (Breadth first search).
        dfs(self, start_value: str) -> None:
            DFS (Depth first search).
        get_max_value(self) -> float:
            Get the maximum value of the agents in the graph.
        get_min_value(self) -> float:
            Get the minimum value of the agents in the graph.
        create_group(self, start_value: str) -> List[list]:
            Create group of bidirectional neighbors using the BFS.
        create_groups(self) -> List[List["Agent"]]:
            Create groups of bidirectional neighbors using the BFS.
    """

    def __init__(self) -> None:
        self.agents = {}

    def __str__(self) -> str:
        """
        Represents the graph in a string format.

            Parameters
                None
    
            Returns
                return The string format of the graph
        """

        return str(self.agents)

    def __repr__(self) -> str:
        """
        Represents the graph in a string format for data structures.

            Parameters
                None
    
            Returns
                return The string format of the graph
        """

        return str(self.agents)

    def add_agent(self, tag: str, value: float, radius: float) -> None:
        """
        Add a new agent to the graph.

            Parameters
                tag (str): Tag/id of the agent
                value (float): Value of the agent
                radius (float): Radius of the agent
    
            Returns
                return None
        """

        if tag not in self.agents:
            self.agents[tag] = Agent(tag, value,radius)

    def add_edge(self, tag1: str, tag2: str) -> None:
        """
        Add a new edge to the graph.

            Parameters
                tag1 (str): Tag/id of the first agent
                tag1 (str): Tag/id of the second agent
    
            Returns
                return None
        """

        if tag1 in self.agents and tag2 in self.agents:
            self.agents[tag1].add_neighbor(self.agents[tag2])

    def remove_agent(self, tag: str) -> None:
        """
        Remove a agent from the graph.

            Parameters
                tag (str): Tag/id of the agent
    
            Returns
                return None
        """

        if tag in self.agents:
            agent_to_remove = self.agents[tag]
            for neighbor in agent_to_remove.neighbors:
                neighbor.remove_neighbor(agent_to_remove)
            del self.agents[tag]

    def remove_edge(self, tag1: str, tag2: str) -> None:
        """
        Remove an edge from the graph.

            Parameters
                tag1 (str): Tag/id of the first agent
                tag1 (str): Tag/id of the second agent
    
            Returns
                return None
        """

        if tag1 in self.agents and tag2 in self.agents:
            self.agents[tag1].remove_neighbor(self.agents[tag2])
            self.agents[tag2].remove_neighbor(self.agents[tag1])

    def display(self) -> None:
        """
        Display the graph agents.

            Parameters
                None    

            Returns
                return None
        """

        for agent in self.agents.values():
            neighbors = [neighbor.tag for neighbor in agent.neighbors]
            print(f"{agent.tag}: {neighbors}")

    def bfs(self, start_value: str) -> None:
        """
        BFS (Breadth first search).

            Parameters
                start_value (str): Initial agent

            Returns
                return None
        """

        if start_value not in self.agents:
            return

        visited = set()
        queue = [self.agents[start_value]]

        while queue:
            agent = queue.pop(0)
            if agent not in visited:
                print(agent, end=" ")
                visited.add(agent)
                queue.extend(set(agent.neighbors) - visited)
        print()

    def dfs(self, start_value: str) -> None:
        """
        DFS (Depth first search).

            Parameters
                start_value (str): Initial agent

            Returns
                return None
        """

        if start_value not in self.agents:
            return

        visited = set()
        stack = [self.agents[start_value]]

        while stack:
            agent = stack.pop()
            if agent not in visited:
                print(agent, end=" ")
                visited.add(agent)
                stack.extend(set(agent.neighbors) - visited)
        print()

    def get_max_value(self) -> float:
        """
        Get the maximum value of the agents in the graph.

            Parameters
                None

            Returns
                return Maximum size
        """

        max_value = float("-inf")
        for agent_tag in self.agents:
            max_value = max(max_value, self.agents[agent_tag].value)
        return max_value

    def get_min_value(self) -> float:
        """
        Get the minimum value of the agents in the graph.

            Parameters
                None

            Returns
                return Maximum size
        """

        min_value = float("inf")
        for agent_tag in self.agents:
            min_value = min(min_value, self.agents[agent_tag].value)
        return min_value

    def create_group(self, start_value: str) -> Tuple[List["Agent"], List["Agent"]]:
        """
        Create group of bidirectional neighbors using the BFS.

            Parameters
                start_value (str): Initial agent

            Returns
                return List of agents of the same group and the visited agents
                return None if the agent is not in the dict of agents
        """

        if start_value not in self.agents:
            return

        visited = set()
        group = [self.agents[start_value]]
        index = 0

        while index < len(group):
            agent = group[index]
            index += 1
            if agent not in visited:
                # Save the neighbors
                for neighbor in agent.neighbors:
                    # Check the neighbors who have not been visited and have a two-way connection
                    if (neighbor not in visited) and (neighbor not in group) and (agent.is_bidirectional(neighbor) == True):
                        group.append(neighbor)
                visited.add(agent)
        return group, visited

    def create_groups(self) -> List[List["Agent"]]:
        """
        Create groups of bidirectional neighbors using the BFS.

            Parameters
                None

            Returns
                return List of groups
        """

        groups, visited = [], set()
        for agent in self.agents:
            if self.agents[agent] not in visited:
                group, aux_visited = self.create_group(agent)
                groups.append(group)
                visited = visited.union(aux_visited)
        return groups
