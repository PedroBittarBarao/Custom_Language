"""A module containing the FuncTable class for managing a function table.

        None

    Classes:
        FuncTable: A class representing a function table.

        None"""

class FuncTable:
    """
    A class representing a function table.

    Attributes:
        table (dict): A dictionary representing the function table.

    Methods:
        setFunc(name, Func): Adds a function to the table.
        getFunc(name): Retrieves a function from the table.
        isInTable(name): Checks if a function exists in the table.
    """
    table = {}

    def setFunc(self, name, func):
        """
        Adds a function to the function table.

        Parameters:
        - name (str): The name of the function.
        - func (function): The function to be added.

        Raises:
        - KeyError: If a function with the same name already exists in the table.
        """
        if name in FuncTable.table:
            raise KeyError(f"Function {name} already exists")
        FuncTable.table[name] = func

    def getFunc(self, name):
        """
        Retrieves a function from the function table based on its name.

        Parameters:
        name (str): The name of the function to retrieve.

        Returns:
        function: The function object associated with the given name.

        """
        return FuncTable.table[name]

    def isInTable(self, name):
        """
        Check if a given name is in the function table.

        Parameters:
        - name (str): The name to be checked.

        Returns:
        - bool: True if the name is in the function table, False otherwise.
        """
        return name in FuncTable.table


if __name__ == "__main__":
    pass
