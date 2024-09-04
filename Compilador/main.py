"""
This module contains the main script for the Custom Language-1 compiler.

The main script reads a source file,
parses the code using the Parser class,
and evaluates the parsed code using a SymbolTable object.

Usage:
    python main.py <source_file>

Args:
    source_file (str): The path to the source file to be compiled.

Example:
    python main.py /path/to/source_file.bar
"""


from parser import Parser
import sys
from symbol_table import SymbolTable
from func_table import FuncTable

source = sys.argv[1]

with open(source, "r") as file:
    code = file.read()

my_symbol_table = SymbolTable()
Parser.run(code).evaluate(my_symbol_table)
