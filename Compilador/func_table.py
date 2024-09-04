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
        setFunc(Name, Func): Adds a function to the table.
        getFunc(Name): Retrieves a function from the table.
        isInTable(Name): Checks if a function exists in the table.
    """
    table = {}

    def setFunc(Name, Func):
        """
        Adds a function to the function table.

        Parameters:
        - Name (str): The name of the function.
        - Func (function): The function to be added.

        Raises:
        - KeyError: If a function with the same name already exists in the table.
        """
        if Name in FuncTable.table:
            raise KeyError(f"Function {Name} already exists")
        FuncTable.table[Name] = Func

    def getFunc(Name):
        """
        Retrieves a function from the function table based on its name.

        Parameters:
        Name (str): The name of the function to retrieve.

        Returns:
        function: The function object associated with the given name.

        """
        return FuncTable.table[Name]

    def isInTable(Name):
        """
        Check if a given name is in the function table.

        Parameters:
        - Name (str): The name to be checked.

        Returns:
        - bool: True if the name is in the function table, False otherwise.
        """
        return Name in FuncTable.table


if __name__ == "__main__":
    FuncTable.setFunc("funcao", "NODE")
    print(FuncTable.getFunc("funcao"))
