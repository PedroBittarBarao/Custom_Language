"""
Module: AST Nodes

This module defines various classes used to represent nodes in the Abstract Syntax Tree (AST) 
of a compiler. Each class corresponds to a specific type of node, such as binary operations, 
unary operations, literals, control structures, etc. Each node class contains an `evaluate` 
method that processes the node in the context of a symbol table.

Classes:
    Node: Base class for all AST nodes.
    NoOp: Represents a no-operation node.
    BinOp: Represents a binary operation node.
    IntVal: Represents an integer literal node.
    UnOp: Represents a unary operation node.
    Block: Represents a block of statements.
    Identifier: Represents a variable or identifier node.
    Assignment: Represents an assignment operation.
    PrintNode: Represents a print operation.
    ReadNode: Represents a read operation for input.
    IfNode: Represents an if-else control structure.
    WhileNode: Represents a while loop.
    StrVal: Represents a string literal node.
    VarDec: Represents a variable declaration node.
    FuncDec: Represents a function declaration node.
    FuncCall: Represents a function call node.
    ReturnNode: Represents a return statement in a function.
    SwitchNode: Represents a switch-case control structure.
    CaseNode: Represents a case within a switch statement.
    DefaultNode: Represents a default case in a switch statement.
    TypeNode: Represents a type node in declarations.
"""

from symbol_table import SymbolTable
from func_table import FuncTable


class Node:
    """
    Represents a node in a tree structure.
    Attributes:
        value (int): The value associated with the node.
        children (list): The list of child nodes.
    Methods:
        evaluate(symbol_table): Evaluates the node using the given symbol table.
    """

    def __init__(self, value=0, children=None):
        if children is None:
            children = []
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        """
        Evaluate the node using the given symbol table.

        Parameters:
        - symbol_table: The symbol table containing the variables and their values.

        Returns:
        - None

        """

class NoOp(Node):
    """
    Represents a NoOp node in the abstract syntax tree.

    This node does not perform any operation and is used as a placeholder.

    Attributes:
        None

    Methods:
        evaluate(symbol_table): Evaluates the NoOp node.

    Returns:
        None
    """

    def evaluate(self, symbol_table):
        return None  # ???


class BinOp(Node):
    """
    Represents a binary operation node in the abstract syntax tree.

    Attributes:
        value (str): The operator of the binary operation.
        children (list): The list of child nodes.

    Methods:
        evaluate(symbol_table):
            Evaluates the binary operation and returns the result.

    
        Evaluates the binary operation and returns the result.

        Args:
            symbol_table (dict): The symbol table containing variable values.

        Returns:
            tuple: A tuple containing the result of the binary operation and its type.

        Raises:
            SyntaxError: If an unexpected token is encountered during evaluation.


        Returns a string representation of the BinOp node.

        Returns:
            str: The string representation of the BinOp node.

        """

    def evaluate(self, symbol_table):
        if self.value == "+":
            return (
                self.children[0].evaluate(symbol_table)[0]
                + self.children[1].evaluate(symbol_table)[0],
                "INT",
            )
        if self.value == "-":
            return (
                self.children[0].evaluate(symbol_table)[0]
                - self.children[1].evaluate(symbol_table)[0],
                "INT",
            )
        if self.value == "*":
            return (
                self.children[0].evaluate(symbol_table)[0]
                * self.children[1].evaluate(symbol_table)[0],
                "INT",
            )
        if self.value == "/":
            return (
                self.children[0].evaluate(symbol_table)[0]
                // self.children[1].evaluate(symbol_table)[0],
                "INT",
            )
        if self.value == "==":
            if (
                self.children[0].evaluate(symbol_table)[1] == "STRING"
                and self.children[1].evaluate(symbol_table)[1] == "STRING"
            ) or (
                self.children[0].evaluate(symbol_table)[1] == "INT"
                and self.children[1].evaluate(symbol_table)[1] == "INT"
            ):
                return (
                    int(
                        self.children[0].evaluate(symbol_table)[0]
                        == self.children[1].evaluate(symbol_table)[0]
                    ),
                    "INT",
                )
            raise SyntaxError(
                    f"""Unexpected token BinOp ==
                    {self.children[0].evaluate(symbol_table)[1]}
                    and {self.children[1].evaluate(symbol_table)[1]}"""
                )
        if self.value == ">":
            return (
                int(
                    self.children[0].evaluate(symbol_table)[0]
                    > self.children[1].evaluate(symbol_table)[0]
                ),
                "INT",
            )
        if self.value == "<":
            return (
                self.children[0].evaluate(symbol_table)[0]
                < self.children[1].evaluate(symbol_table)[0],
                "INT",
            )
        if self.value == "and":
            return (
                self.children[0].evaluate(symbol_table)[0]
                and self.children[1].evaluate(symbol_table)[0],
                "INT",
            )
        if self.value == "or":
            return (
                self.children[0].evaluate(symbol_table)[0]
                or self.children[1].evaluate(symbol_table)[0],
                "INT",
            )
        if self.value == "CONCAT":
            return (
                str(self.children[0].evaluate(symbol_table)[0])
                + str(self.children[1].evaluate(symbol_table)[0]),
                "STRING",
            )
        raise SyntaxError(f"Unexpected token BinOp {self.value}")

    def __str__(self) -> str:
        return f"BinOp({self.value}: {self.children[0]}, {self.children[1]})"


class IntVal(Node):
    """
    IntVal class represents a node in the abstract syntax tree (AST)
    that represents an integer value.

    Attributes:
        value (int): The integer value represented by this node.

    Methods:
        evaluate(symbol_table):
            Evaluates the node and returns a tuple containing
             the integer value and its type.
            
        __str__():
            Returns a string representation of the IntVal node.
    """

    def evaluate(self, symbol_table):
        return (int(self.value), "INT")

    def __str__(self):
        return f"IntVal({self.value})"


class UnOp(Node):
    """
    Represents a unary operation node in the abstract syntax tree.

    Attributes:
        value (str): The unary operator.
        children (list): The child nodes of the unary operation.

    Methods:
        evaluate(symbol_table):
            Evaluates the unary operation and returns the result.
            Args:
                symbol_table (dict): The symbol table for variable lookup.
            Returns:
                tuple: A tuple containing the evaluated result and its type.
            Raises:
                SyntaxError: If an unexpected token is encountered.

        __str__():
            Returns a string representation of the unary operation node.
            Returns:
                str: The string representation of the unary operation node.
    """

    def evaluate(self, symbol_table):
        if self.value == "+":
            return (self.children[0].evaluate(symbol_table)[0], "INT")
        if self.value == "-":
            return (-self.children[0].evaluate(symbol_table)[0], "INT")
        if self.value == "not":
            return (not self.children[0].evaluate(symbol_table)[0], "INT")
        raise SyntaxError(f"Unexpected token {self.value} UnOp")

    def __str__(self) -> str:
        return f"UnOp({self.value},{self.children})"


class Block(Node):
    """
    Represents a block of code.

    Attributes:
        children (list): List of child nodes contained in the block.

    Methods:
        evaluate(symbol_table): Evaluates the block by iterating
        over its children and executing their evaluate methods.

        Evaluates the block by iterating over its children and executing their evaluate methods.

        Args:
            symbol_table (dict): The symbol table used for variable lookup and assignment.

        Returns:
            The result of the last evaluated child node, or None if there are no child nodes.

        Returns a string representation of the block.

        Returns:
            A string representation of the block.
        """

    def evaluate(self, symbol_table):
        for child in self.children:
            # print(child)
            if isinstance(child, ReturnNode):
                return child.evaluate(symbol_table)
            child.evaluate(symbol_table)

    def __str__(self) -> str:
        i = 0
        for child in self.children:
            i += 1
            return f"Block:{i} ({child})"


class Identifier(Node):
    """
    Represents an identifier node in the abstract syntax tree.

    Attributes:
        value (str): The value of the identifier.

    Methods:
        evaluate(symbol_table): Evaluates the identifier
        by retrieving its value from the symbol table.



    Evaluates the identifier by retrieving its value from the symbol table.

    Args:
        symbol_table (dict): The symbol table containing
        variable names and their corresponding values.

    Returns:
        The value of the identifier.

    Returns a string representation of the identifier.

    Returns:
        A string representation of the identifier.
    """

    def evaluate(self, symbol_table):
        return symbol_table.get_value(self.value)

    def __str__(self):
        return f"Identifier({self.value})"


class Assignment(Node):
    """
    Represents an assignment statement node in the abstract syntax tree.

    Attributes:
        children (list): A list of child nodes representing
        the left-hand side and right-hand side of the assignment.


        Evaluates the assignment statement by assigning the value of
        the right-hand side expression to the variable on the left-hand side.

        Args:
            symbol_table (SymbolTable): The symbol table containing variable values.

        Raises:
            ValueError: If the assigned value's type does not match the variable's type.

        Returns:
            None


        Returns a string representation of the Assignment node.

        Returns:
            str: The string representation of the node.
        """

    def evaluate(self, symbol_table):
        val = self.children[1].evaluate(symbol_table)
        if symbol_table.has_value(self.children[0].value):
            type_ = symbol_table.get_value(self.children[0].value)[1]
            if type_.lower() != (val[1]).lower():
                raise ValueError(f"Cannot assign {val[1]} to {type_}")
        symbol_table.set_value(self.children[0].value, val)

    def __str__(self):
        return f"Assignment({self.children[0],self.children[1]})"


class PrintNode(Node):
    """
    Evaluates the PrintNode and prints the value of the child node.

    Args:
        symbol_table (dict): The symbol table containing variable values.

    Raises:
        ValueError: If the type of the value to be printed is unexpected.

    Returns:
        None
    """


    def evaluate(self, symbol_table):
        var = self.children[0].evaluate(symbol_table)
        if var[1] == "STRING":
            print(var[0])
        elif var[1] == "INT":
            print(int(var[0]))  # cast do print para int
        else:
            raise ValueError(f"Unexpected print type {var}")

    def __str__(self):
        return f"printNode: ({self.children[0]})"


class ReadNode(Node):
    """
    A node representing the read operation in the custom language.

    This node reads an integer value from the user
    and returns it along with the data type "INT".

    Attributes:
        None

    Methods:
        evaluate(symbol_table):
            Reads an integer value from the user
            and returns it along with the data type "INT".

        __str__():
            Returns a string representation of the ReadNode.

    Example usage:
        read_node = ReadNode()
        result = read_node.evaluate(symbol_table)
        print(result)
    """

    def evaluate(self, symbol_table):
        val = int(input())
        return (val, "INT")

    def __str__(self):
        return f"readNode: ({self.children[0]})"


class IfNode(Node):
    """
    Represents an if statement node in the abstract syntax tree.

    Attributes:
        children (list): A list of child nodes representing the condition,
        the body of the if statement, and the else body (optional).

    Methods:
        evaluate(symbol_table):
            Evaluates the if statement by evaluating the condition
            and executing the appropriate body based on the result.

        __str__():
            Returns a string representation of the IfNode object.
    """


    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table)[0]:
            self.children[1].evaluate(symbol_table)
        elif len(self.children) == 3:
            self.children[2].evaluate(symbol_table)

    def __str__(self):
        return f"IfNode: ({self.children[0],self.children[1],self.children[2]})"


class WhileNode(Node):
    """
    Represents a while loop node in the abstract syntax tree.

    Attributes:
        children (list): A list containing two child nodes: the condition node and the body node.

    Methods:
        evaluate(symbol_table):
            Evaluates the while loop by repeatedly executing the body node
            while the condition node evaluates to True.

        __str__():
            Returns a string representation of the while loop node.
    """

    def evaluate(self, symbol_table):
        while self.children[0].evaluate(symbol_table)[0]:
            self.children[1].evaluate(symbol_table)

    def __str__(self):
        return f"whileNode: ({self.children[0],self.children[1]})"


class StrVal(Node):
    """
    Evaluates the StrVal node and returns a tuple containing the string value and its type.

    Args:
        symbol_table (dict): The symbol table containing variable values.

    Returns:
        tuple: A tuple containing the string value and its type.

    """
    def evaluate(self, symbol_table):
        return (str(self.value), "STRING")

    def __str__(self):
        return f"StrVal({self.value})"


class VarDec(Node):
    """
    Evaluates the VarDec node and creates a variable in the symbol table.

    Args:
        symbol_table (SymbolTable): The symbol table to store the variable.

    Returns:
        None
    """
    def evaluate(self, symbol_table):
        var_type = self.children[1].value
        symbol_table.create_var(self.children[0].value, var_type)
        if len(self.children) == 3:
            var = self.children[2].evaluate(symbol_table)  # (value, type)
            symbol_table.set_value(self.children[0].value, var)

    def __str__(self):
        return f"VarDec({self.value})"


class FuncDec(Node):
    """
    Evaluate the function declaration node.

    Args:
        symbol_table (dict): The symbol table containing variable and function information.

    Raises:
        KeyError: If the function name already exists in the function table.

    Returns:
        None
    """
    def evaluate(self, symbol_table):
        name = self.children[0].value
        if FuncTable.isInTable(name):
            raise KeyError(f"Function {name} already exists")
        FuncTable.setFunc(name, self)


class FuncCall(Node):
    """
    Evaluate a function call.

    Parameters:
    - symbol_table (SymbolTable): The symbol table containing variable values.

    Raises:
    - KeyError: If the function does not exist in the function table.
    - TypeError: If the number of arguments provided
    does not match the number of expected arguments.

    Returns:
    - The result of evaluating the function body using the provided arguments.
    """
    def evaluate(self, symbol_table):
        func = FuncTable.getFunc(self.value)
        if func is None:
            raise KeyError(f"Function {self.value} does not exist")
        args = func.children[1:-1]
        # raise if len(args) != len(self.children)
        if len(args) != len(self.children):
            raise TypeError(
                f"Function {self.value} expected {len(args)} arguments, got {len(self.children)}"
            )
        new_table = SymbolTable()
        for i, arg in enumerate(args):
            new_table.create_var(arg.value, var_type="None")
            new_table.set_value(arg.value, self.children[i].evaluate(symbol_table))
        return func.children[-1].evaluate(new_table)


class ReturnNode(Node):
    """
    Represents a ReturnNode in the abstract syntax tree.

    Attributes:
        children (list): A list of child nodes.

    Methods:
        evaluate(symbol_table): Evaluates the ReturnNode and returns the result.

    """
    def evaluate(self, symbol_table):
        return self.children[0].evaluate(symbol_table)


class SwitchNode(Node):
    """
    Evaluates the SwitchNode by iterating through its children
    and executing the appropriate case or default block.

    Args:
        symbol_table (dict): The symbol table containing the variables and their values.

    Returns:
        None
    """
    def evaluate(self, symbol_table):
        switch_value = self.children[0].evaluate(symbol_table)[0]
        for i in range(1, len(self.children)):
            if isinstance(self.children[i], DefaultNode):
                self.children[i].evaluate(symbol_table)
                return
            if self.children[i].children[0].evaluate(symbol_table)[0] == switch_value:
                self.children[i].evaluate(symbol_table)
                return
        return

    def __str__(self):
        return f"SwitchNode: ({self.children})"


class CaseNode(Node):
    """
    Evaluates the CaseNode and returns the evaluation of its second child node.

    Args:
        symbol_table (dict): The symbol table containing variable values.

    Returns:
        The evaluation of the second child node.
    """

    def evaluate(self, symbol_table):
        return self.children[1].evaluate(symbol_table)

    def __str__(self):
        return f"CaseNode: ({self.children})"


class DefaultNode(Node):
    """
    Evaluates the default node by calling the evaluate method of its first child node.

    Args:
        symbol_table (dict): The symbol table used for evaluation.

    Returns:
        None
    """

    def evaluate(self, symbol_table):
        self.children[0].evaluate(symbol_table)

    def __str__(self):
        return f"DefaultNode: ({self.children})"


class TypeNode(Node):
    """
    TypeNode class represents a node in
    the abstract syntax tree (AST) for the custom language compiler.

    Attributes:
        value (str): The value of the TypeNode.

    Methods:
        evaluate(symbol_table):
            Evaluates the TypeNode and returns its value.

        __str__():
            Returns a string representation of the TypeNode.
    """
    def evaluate(self, symbol_table):
        return self.value

    def __str__(self):
        return f"TypeNode({self.value})"
