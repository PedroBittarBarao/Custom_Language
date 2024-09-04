"""
Module: symbol_table

This module defines the `SymbolTable` class, which is used to manage the symbol table for a parser.
A symbol table is a data structure that stores variable information (such as value and type) 
during the parsing of a programming language.
It supports variable declaration, lookup, and value assignment.

Classes:
    SymbolTable: A class that manages variable declarations, assignments, and lookups for a parser.

Functions:
    __init__(self):
        Initializes an empty symbol table.

    get_value(self, key):
        Retrieves the value of a variable from the symbol table.

    has_value(self, key):
        Checks if a variable is declared in the symbol table.

    set_value(self, key, var):
        Assigns a value to a declared variable in the symbol table.

    create_var(self, key, var_type):
        Declares a new variable in the symbol table with a specified type.
"""

class SymbolTable:
    """
    A class used to manage variables in a symbol table for a parser. 
    It handles variable declarations, assignments, and lookups.

    Attributes:
        table (dict): A dictionary that stores variables as keys,
        and their values and types as values.

    Methods:
        __init__():
            Initializes an empty symbol table.
        
        get_value(key):
            Retrieves the value of a variable from the symbol table.
        
        has_value(key):
            Checks if a variable is declared in the symbol table.
        
        set_value(key, var):
            Assigns a value to an already declared variable in the symbol table.
        
        create_var(key, var_type):
            Declares a new variable with a specified type in the symbol table.
    """

    def __init__(self):
        """
        Initializes an empty symbol table.
        The symbol table is implemented as a dictionary where the keys are variable names, 
        and the values are tuples containing the variable's value and type.
        """
        self.table = {}

    def get_value(self, key):
        """
        Retrieves the value of a variable from the symbol table.

        Args:
            key (str): The name of the variable to look up.
        
        Returns:
            The value associated with the variable.

        Raises:
            KeyError: If the variable is not found in the symbol table.
        """
        return self.table[key]

    def has_value(self, key):
        """
        Checks if a variable has been declared in the symbol table.

        Args:
            key (str): The name of the variable to check.
        
        Returns:
            bool: True if the variable exists in the symbol table, False otherwise.
        """
        return key in self.table

    def set_value(self, key, var):
        """
        Assigns a value to a variable in the symbol table.

        Args:
            key (str): The name of the variable to assign a value to.
            var: The value to assign to the variable.
        
        Raises:
            KeyError: If the variable has not been declared.
        """
        if key not in self.table:
            raise KeyError(f"Variable {key} not declared")
        self.table[key] = var  # (value, type)

    def create_var(self, key, var_type):
        """
        Declares a new variable in the symbol table with a specified type.

        Args:
            key (str): The name of the variable to declare.
            var_type (str): The type of the variable being declared.
        
        Raises:
            KeyError: If the variable is already declared.
        """
        if key in self.table:
            raise KeyError(f"Variable {key} already declared")
        self.table[key] = (None, var_type)
