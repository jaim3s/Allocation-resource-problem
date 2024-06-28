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
        generate_integer_numbers(self, min_value: int, max_value: int) -> List[int]:
            Generate random integer numbers.
        generate_float_numbers(self, min_value: float, max_value: float, precision: int) -> List[int]:
            Generate random float numbers.
        generate_unique_pairs(self, min_value1: int, max_value1: int, min_value2: int, max_value2: int) -> List[int]:
            Generate random unique pairs of numbers.
    """

    def __init__(self, n: int, seed_id: int) -> None:
        self.n = n
        self.seed_id = seed_id
        random.seed(self.seed_id)

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

    def generate_integer_numbers(self, min_value: int, max_value: int) -> List[int]:
        """
        Generate random integer numbers.

            Parameters
                min_value (int): Minimal integer value
                max_value (int): Maximal integer value
    
            Returns
                return List with random integer numbers
        """

        return [random.randint(min_value, max_value) for _ in range(self.n)]

    def generate_float_numbers(self, min_value: float, max_value: float, precision: int) -> List[int]:
        """
        Generate random float numbers.

            Parameters
                min_value (float): Minimal float value
                max_value (float): Maximal float value
                precision (int): Precision of the random numbers
    
            Returns
                return List with random float numbers
        """

        random_float_numbers = []
    
        for _ in range(self.n):
            random_float = random.uniform(min_value, max_value)
            format_str = "{:." + str(precision) + "f}"
            formatted_float = float(format_str.format(random_float))
            random_float_numbers.append(formatted_float)
        
        return random_float_numbers

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


