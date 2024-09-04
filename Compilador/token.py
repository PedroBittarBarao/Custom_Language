"""
Module: tokenizer

This module defines a basic `Token` class used in the tokenizer component of a programming language. 
A tokenizer, also known as a lexical analyzer, breaks down source code into tokens which are the 
smallest units of meaning (e.g., keywords, operators, identifiers, etc.).

Classes:
    Token: Represents a token with a type and a value.
"""

class Token:
    """
    A class used to represent a token in a programming language.

    Attributes:
        typ (str): The type of the token (e.g., 'PLUS', 'NUMBER', etc.).
        value (int): The value associated with the token, usually an integer 
                     (e.g., 1 for the token '1', 42 for the token '42').

    Methods:
        __init__(typ, value):
            Initializes the token with a type and a value.

        __str__():
            Returns a string representation of the token.
    """

    typ: str
    value: int

    def __init__(self, typ, value) -> None:
        """
        Initializes the Token object with a type and a value.

        Args:
            typ (str): The type of the token (e.g., 'PLUS', 'NUMBER').
            value (int): The value of the token, typically an integer.
        """
        self.typ = typ
        self.value = value

    def __str__(self):
        """
        Returns a string representation of the Token.

        Returns:
            str: A string in the format "type: <typ> value: <value>".
        """
        return f"type: {self.typ} value: {self.value}"


if __name__ == "__main__":
    x = Token("PLUS", 1)
    print(x)
