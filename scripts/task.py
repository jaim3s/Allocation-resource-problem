class Task:
    """
    A class to represent a task.

        Attributes
        ----------

        size : float
            Size of the task
        value : float
            Value of the task
        time : float
            Time for the task

        Methods
        -------

        __str__(self) -> str:
            Represents the task in a string format.
        __repr__(self) -> str:
            Represents the task in a string format for data structures.
    """

    def __init__(self, size: float, value: float, time: float) -> None:
        self.size = size
        self.value = value
        self.time = time

    def __str__(self) -> str:
        """
        Represents the task in a string format.

            Parameters
                None
    
            Returns
                return The string format of the task
        """

        return "(" + str(self.size) + ", " + str(self.value) + ", " + str(self.time) + ")"

    def __repr__(self) -> str:
        """
        Represents the task in a string format for data structures.

            Parameters
                None
    
            Returns
                return The string format of the task
        """

        return "(" + str(self.size) + ", " + str(self.value) + ", " + str(self.time) + ")"
