"""
Module: preprocessor

This module defines the `PrePro` class, which is used as a preprocessor for input source code 
in a compiler.
The preprocessor is responsible for removing comments and
handling other preprocessing tasks before tokenization and parsing.
The filter method specifically removes comments from the source code.

Classes:
    PrePro: A class that provides static methods for preprocessing source code.

Functions:
    filter(source):
        Removes single-line comments from the source code.
"""

import re

class PrePro:
    """
    A class that provides preprocessing functionality for source code in a compiler.

    Methods:
        filter(source):
            Removes comments from the source code by filtering out any lines that start with '--'.
    """

    @staticmethod
    def filter(source):
        """
        Removes single-line comments from the source code.
        Comments are considered to start with '--'
        and continue to the end of the line.
        This method supports both inline and standalone comments.

        Args:
            source (str): The raw source code as a string.

        Returns:
            str: The source code with comments removed.

        Example:
            >>> PrePro.filter("1 + 1 -- This is a comment")
            '1 + 1'
        """
        comments = re.sub(r"(?<!\d|-)--.*$", "", source, flags=re.MULTILINE)
        return comments
    def __str__(self) -> str:
        pass


if __name__ == "__main__":
    print(PrePro.filter("1 + 1 -- 1 + 1 greer"))  # "1 + 1"
    print(PrePro.filter("1 - 1 - 1 + 1"))
    print(
        PrePro.filter(
            """3+6/3   *  2 -+-  +  2*4/2 + 0/1 -((6+ ((4)))/(2)) -- Teste
                         -- Teste 2"""
        )
    )
