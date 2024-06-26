import numpy as np


class Grid:
    """
    A class to represent a grid.

        Attributes
        ----------

        rows : int
            Rows of the grid
        cols : int
            Columns of the grid

        Methods
        -------

        __str__(self) -> str:
            Represents the grid in a string format.
        __repr__(self) -> str:
            Represents the grid in a string format for data structures.
        create_grid(self) -> np.ndarray:
            Create an empty numpy array for save the agents.
    """

    def __init__(self, rows: int, cols: int) -> None:
        self.rows, self.cols = rows, cols
        self.values = self.create_grid()

    def __str__(self) -> str:
        """
        Represents the grid in a string format.

            Parameters
                None
    
            Returns
                return The string format of the grid
        """

        return str(self.values)
        
    def __repr__(self) -> str:
        """
        Represents the grid in a string format for data structures.

            Parameters
                None
    
            Returns
                return The string format of the grid
        """

        return str(self.values)

    def create_grid(self) -> np.ndarray:
        """
        Create an empty numpy array for save the agents.

            Parameters
                None
    
            Returns
                return Numpy array for save agents
        """

        return np.zeros(shape=(self.rows, self.cols), dtype=str)

