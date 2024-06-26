from typing import List
import random


class Generator:
    """
    A class to represent a generator.

        Attributes
        ----------

        n : int
            Number of numbers to generate

        Methods
        -------

        generate_unique_numbers(self, min_value: int, max_value: int) -> List[int]:
            Generate random unique numbers.
        generate_numbers(self, min_value: int, max_value: int) -> List[int]:
            Generate random numbers.
        generate_unique_pairs(self, min_value1: int, max_value1: int, min_value2: int, max_value2: int) -> List[int]:
            Generate random unique pairs of numbers.
    """

    def __init__(self, n: int) -> None:
        self.n = n

    def generate_unique_numbers(self, min_value: int, max_value: int) -> List[int]:
        """
        Generate random unique numbers.

            Parameters
                min_value (int): Minimal value
                max_value (int): Maximal value
    
            Returns
                return List with random unique numbers
        """

        unique_numbers = set()
        while len(unique_numbers) < self.n:
            unique_numbers.add(random.randint(min_value, max_value))
        return list(unique_numbers)

    def generate_numbers(self, min_value: int, max_value: int) -> List[int]:
        """
        Generate random numbers.

            Parameters
                min_value (int): Minimal value
                max_value (int): Maximal value
    
            Returns
                return List with random numbers
        """

        return [random.randint(min_value, max_value) for _ in range(self.n)]

    def generate_unique_pairs(self, min_value1: int, max_value1: int, min_value2: int, max_value2: int) -> List[int]:
        """
        Generate random unique pairs of numbers.

            Parameters
                min_value1 (int): First minimal value
                max_value1 (int): First maximal value
                min_value2 (int): Second minimal value
                max_value2 (int): Second maximal value

            Returns
                return List with random unique pairs of numbers
        """

        pairs = set()
        while len(pairs) < self.n:
            num1 = random.randint(min_value1, max_value1)
            num2 = random.randint(min_value2, max_value2)
            pairs.add((num1, num2))
        return list(pairs)


