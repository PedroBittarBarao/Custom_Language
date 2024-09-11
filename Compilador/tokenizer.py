"""
Module: tokenizer

This module defines the `Tokenizer` class which is responsible for converting a source code string
into tokens, the smallest units of meaning in a programming language. This tokenizer identifies
various token types such as operators, parentheses, keywords, and literals from the source code. 
It supports handling reserved words, operators, numbers, strings, and other common syntax elements.

Classes:
    Tokenizer: A class that processes source code and generates tokens for parsing.

Functions:
    __init__(self, source, position):
        Initializes the tokenizer with a source string and a starting position.

    select_next(self):
        Scans the source code starting from the current position to identify the next token. 
        Updates the `next` attribute with the identified token.

    __str__(self):
        Returns a string representation of the current token and its position.

Reserved Words:
    A predefined list of reserved keywords such as 'if', 'while', 'print', etc.
"""

from token import Token
from pre_pro import PrePro

reserved_words = [
    "print",
    "if",
    "else",
    "while",
    "and",
    "or",
    "int",
    "string",
    "switch",
    "case",
    "default",
]

class Tokenizer:
    """
    A class used to tokenize source code, converting a string into individual tokens.

    Attributes:
        source (str): The source code string to be tokenized, preprocessed by `PrePro`.
        position (int): The current position of the tokenizer in the source string.
        next (Token): The next token that has been identified by the tokenizer.

    Methods:
        __init__(source, position):
            Initializes the tokenizer with a source string and starting position.
        
        select_next():
            Identifies and updates the next token from the source code.

        __str__():
            Returns a string representation of the current token and its position.
    """

    source: str
    position: int
    next: Token
    next = None

    def __init__(self, source, position) -> None:
        """
        Initializes the Tokenizer object with a source string and starting position.

        Args:
            source (str): The source code to be tokenized.
            position (int): The initial position of the tokenizer in the source code.
        """
        self.source = PrePro.filter(source)  # Pre-process the source before tokenizing
        self.position = position

    def select_next(self) -> None:
        """
        Scans the source code starting from the current position to identify the next token.
        This method handles various token types including operators, parentheses, numbers, 
        reserved words, and strings. It updates the `next` attribute with the identified token.

        Raises:
            SyntaxError: If an unrecognized character or unexpected end of string is encountered.
        """
        if self.position < len(self.source):
            # Skip whitespace and tabs
            while self.source[self.position] == " " or self.source[self.position] == "\t":
                if self.position == len(self.source) - 1:
                    self.next = Token("EOF", 0)
                    return
                self.position += 1

            # Identify tokens based on the current character
            if self.source[self.position] == "+":
                self.position += 1
                self.next = Token("PLUS", 0)
            elif self.source[self.position] == "-":
                self.next = Token("MINUS", 0)
                self.position += 1
            elif self.source[self.position] == "*":
                self.next = Token("MULT", 0)
                self.position += 1
            elif self.source[self.position] == "/":
                self.next = Token("DIV", 0)
                self.position += 1
            elif self.source[self.position] == "(":
                self.next = Token("LPAREN", 0)
                self.position += 1
            elif self.source[self.position] == ")":
                self.next = Token("RPAREN", 0)
                self.position += 1
            elif self.source[self.position].isdigit():
                # Handle multi-digit numbers
                start = self.position
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    self.position += 1
                self.next = Token("NUMBER", int(self.source[start:self.position]))
            elif self.source[self.position] == "\n":
                self.next = Token("ENDL", 0)
                self.position += 1
            elif self.source[self.position] == "=":
                if self.source[self.position + 1] == "=":
                    self.next = Token("==", 0)
                    self.position += 2
                else:
                    self.next = Token("=", 0)
                    self.position += 1
            elif str.isalpha(self.source[self.position]):
                # Handle identifiers and reserved words
                start = self.position
                while self.position < len(self.source) and (
                    self.source[self.position].isalnum() or self.source[self.position] == "_"):
                    self.position += 1
                self.next = Token("ID", self.source[start:self.position])
                if self.next.value in reserved_words:
                    self.next = Token(self.next.value, 0)
            elif self.source[self.position] == ">":
                self.next = Token(">", 0)
                self.position += 1
            elif self.source[self.position] == "<":
                self.next = Token("<", 0)
                self.position += 1
            elif self.source[self.position] == "{":
                self.next = Token("LBRACE", 0)
                self.position += 1
            elif self.source[self.position] == "}":
                self.next = Token("RBRACE", 0)
                self.position += 1
            elif self.source[self.position] == ".":
                if self.source[self.position + 1] == ".":
                    self.next = Token("CONCAT", 0)
                    self.position += 2
                else:
                    raise SyntaxError(f"""Unexpected character {self.source[self.position]}
                                       at {self.position}""")
            elif self.source[self.position] == '"':
                # Handle string literals
                start = self.position + 1
                self.position += 1
                while self.source[self.position] != '"':
                    self.position += 1
                    if self.position == len(self.source):
                        raise SyntaxError("Expected '\"'")
                self.next = Token("STRING", self.source[start:self.position])
                self.position += 1
            elif self.source[self.position] == ",":
                self.next = Token("COMMA", 0)
                self.position += 1
            else:
                raise SyntaxError(f"""Unexpected character {self.source[self.position]}
                                   at {self.position}""")
        else:
            self.next = Token("EOF", 0)

    def __str__(self) -> str:
        """
        Returns a string representation of the tokenizer,
        showing the current token and its position.

        Returns:
            str: A string in the format "next: '<token>', position: <position>".
        """
        return f"next: '{self.next}', position: {self.position}"


if __name__ == "__main__":
    CODE = """int x = 21
string y 
y="fish"

if x == 21 
{
	print("yes")
} else {
	print("no")
	print(x)
}

while x<30 
{
	x=x+1
}

switch x (
	case 1
    {
        y=10
    }
	case 2

    {

        y=11

    }

	default 
	{
		print(y)
	}
)"""
    x = Tokenizer(CODE, 0)
    while x.next is None or x.next.typ != "EOF":
        print(x)
        x.select_next()
