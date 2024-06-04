from prsr import prsr
import sys
from symbol_table import SymbolTable
from func_table import FuncTable

source = sys.argv[1]

with open(source, "r") as file:
    code = file.read()

my_symbol_table = SymbolTable()
prsr.run(code).evaluate(my_symbol_table)