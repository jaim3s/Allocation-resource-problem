import os, shutil, scripts.constants


class Program:
    """
    A class to represent the entire program.

        Attributes
        ----------

        None

        Methods
        -------

        delete_folders(self) -> None:
            Delete the folders of the content directory.
        check_number_type(self, value: str) -> object:
            Check if the value is a number (int or float) of not.
        is_boolean(self, value: str) -> bool:
            Check if the value is a boolean.
        string_to_bool(self, value: str) -> bool:
            Convert string into boolean.
        read_parameters(self, filename: str) -> dict:
            Get the content of the parameters file.
    """

    def __init__(self) -> None:
        pass 

    def delete_folders(self) -> None:
        """
        Delete the folders of the content directory.


            Parameters
                None

            Returns
                return None
        """

        for item in os.listdir(scripts.constants.content_folder_path):
            item_path = os.path.join(scripts.constants.content_folder_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)

    def check_number_type(self, value: str) -> object:
        """
        Check if the value is a number (int or float) of not.

            Parameters
                value (str): Value to check if is a number
    
            Returns
                return int data type if the value is an integer
                return float data type if the value is a float
                return None data type if the value isn"t a integer or float
        """

        if value.isdigit():
            return int
        try:
            float_value = float(value)
            if "." in value:
                return float
        except ValueError:
            pass
        return None

    def is_boolean(self, value: str) -> bool:
        """
        Check if the value is a boolean.

            Parameters
                value (str): Value to check if is a number
    
            Returns
                return True if the value is a boolean otherwise False
        """

        return isinstance(value, bool)

    def string_to_bool(self, value: str) -> bool:
        """
        Convert string into boolean.

            Parameters
                value (str): Value to check if is a number
    
            Returns
                return True if the value is true otherwise False
        """
        
        if value.lower() in scripts.constants.TRUE_VALUES:
            return True
        elif value.lower() in scripts.constants.FALSE_VALUES:
            return False
        else:
            raise ValueError(f"Cannot convert {value} to a boolean value")

    def read_parameters(self, filename: str) -> dict:
        """
        Get the content of the parameters file.

            Parameters
                filename (str): Name of the paramaters file
    
            Returns
                return Dictionary with the parameters
        """

        with open(scripts.constants.parameters_folder_path + f"\\{filename}", "r") as file:
            parameters = {}
            for line in file:
                key, value = line.replace(" ", "").strip().split(scripts.constants.SEPARATION_CHAR)
                # Check value type
                value_is_number = self.check_number_type(value)
                if value_is_number == int:
                    value = int(value)
                elif value_is_number == float:
                    value = float(value)
                elif value_is_number == None:
                    if self.is_boolean(value) == True:
                        value == self.string_to_bool(value)
                parameters[key] = value
        return parameters
