from symbol_table import SymbolTable
from func_table import FuncTable

class Node():

    def __init__(self,value = 0,children = []):
        self.value = value
        self.children = children 

    def evaluate(self,symbol_table):
        pass


class NoOp(Node):

    def evaluate(self,symbol_table):
        return None # ???
    

class BinOp (Node):

    def evaluate(self,symbol_table):
        if self.value == "+":
            return (self.children[0].evaluate(symbol_table)[0] + self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "-":
            return (self.children[0].evaluate(symbol_table)[0] - self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "*":
            return (self.children[0].evaluate(symbol_table)[0] * self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "/":
            return (self.children[0].evaluate(symbol_table)[0] // self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "==":
            if (self.children[0].evaluate(symbol_table)[1] == "STRING" and self.children[1].evaluate(symbol_table)[1] == "STRING") or (self.children[0].evaluate(symbol_table)[1] == "INT" and self.children[1].evaluate(symbol_table)[1] == "INT"):
                return (int(self.children[0].evaluate(symbol_table)[0] == self.children[1].evaluate(symbol_table)[0]),"INT")
            else:
                raise SyntaxError(f"Unexpected token BinOp == {self.children[0].evaluate(symbol_table)[1]} and {self.children[1].evaluate(symbol_table)[1]}")
        elif self.value == ">":
            return (int(self.children[0].evaluate(symbol_table)[0] > self.children[1].evaluate(symbol_table)[0]),"INT")
        elif self.value == "<":
            return (self.children[0].evaluate(symbol_table)[0] < self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "and":
            return (self.children[0].evaluate(symbol_table)[0] and self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "or":
            return (self.children[0].evaluate(symbol_table)[0] or self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "CONCAT":
            return (str(self.children[0].evaluate(symbol_table)[0]) + str(self.children[1].evaluate(symbol_table)[0]),"STRING")
        else:
            raise SyntaxError(f"Unexpected token BinOp {self.value}")
    
    def __str__(self) -> str:
        return f"BinOp({self.value}: {self.children[0]}, {self.children[1]})"
    
class IntVal(Node):

    def evaluate(self,symbol_table):
        return (int(self.value),"INT")
    
    def __str__(self):
        return f"IntVal({self.value})"
    
class UnOp(Node):

    def evaluate(self,symbol_table):
        if self.value == "+":
            return (self.children[0].evaluate(symbol_table)[0],"INT")
        elif self.value == "-":
            return (-self.children[0].evaluate(symbol_table)[0],"INT")
        elif self.value == "not":
            return (not self.children[0].evaluate(symbol_table)[0],"INT")
        else:
            raise SyntaxError(f"Unexpected token {self.value} UnOp")
        

    def __str__(self) -> str:
        return f"UnOp({self.value},{self.children})"
    
class Block(Node):

    def evaluate(self,symbol_table):
        for child in self.children:
            #print(child)
            if type(child) == ReturnNode:
                return child.evaluate(symbol_table)
            child.evaluate(symbol_table)
        
    def __str__(self) -> str:
        i=0
        for child in self.children:
            i+=1
            return f"Block:{i} ({child})"
            
class Identifier(Node):

    def evaluate(self,symbol_table):
        return symbol_table.get_value(self.value)
    
    def __str__(self):
        return f"Identifier({self.value})"
    
class Assignment(Node):

    def evaluate(self,symbol_table):
        val = self.children[1].evaluate(symbol_table)
        if symbol_table.has_value(self.children[0].value):
            type = symbol_table.get_value(self.children[0].value)[1]
            if type.lower() != (val[1]).lower():
                raise ValueError(f"Cannot assign {val[1]} to {type}")
        symbol_table.set_value(self.children[0].value,val)
        
        
    def __str__(self):
        return f"Assignment({self.children[0],self.children[1]})"
    
class printNode(Node):
    def evaluate(self,symbol_table):
        var = self.children[0].evaluate(symbol_table)
        if var[1] == "STRING":
            print(var[0])
        elif var[1] == "INT":
            print(int(var[0])) # cast do print para int
        else:
            raise ValueError(f"Unexpected print type {var}")
    def __str__(self):
        return f"printNode: ({self.children[0]})"
    
class readNode(Node):

    def evaluate(self,symbol_table):
        val = int(input())
        return (val,"INT")
        
    def __str__(self):
        return f"readNode: ({self.children[0]})"
    
class ifNode(Node):
    
        def evaluate(self,symbol_table):
            if self.children[0].evaluate(symbol_table)[0]:
                self.children[1].evaluate(symbol_table)
            elif len(self.children) == 3:
                self.children[2].evaluate(symbol_table)
            
        def __str__(self):
            return f"IfNode: ({self.children[0],self.children[1],self.children[2]})"
    
class whileNode(Node):
    
        def evaluate(self,symbol_table):
            while self.children[0].evaluate(symbol_table)[0]:
                self.children[1].evaluate(symbol_table)
            
        def __str__(self):
            return f"whileNode: ({self.children[0],self.children[1]})"
        
class StrVal(Node):
        def evaluate(self,symbol_table):
         return (str(self.value),"STRING")
        
        def __str__(self):
            return f"StrVal({self.value})"
        
class VarDec(Node):
    def evaluate(self,symbol_table):
        var_type = self.children[1].value
        symbol_table.create_var(self.children[0].value,var_type)
        if (len(self.children) == 3):
            var = self.children[2].evaluate(symbol_table) # (value, type)
            symbol_table.set_value(self.children[0].value,var) 
        
    def __str__(self):
        return f"VarDec({self.value})"
    
class FuncDec(Node):
    def evaluate(self,symbol_table):
        name = self.children[0].value
        if FuncTable.isInTable(name):
            raise KeyError(f"Function {name} already exists")
        FuncTable.setFunc(name,self)
        

class FuncCall(Node):
    def evaluate(self,symbol_table):
        func = FuncTable.getFunc(self.value)
        if func is None:
            raise KeyError(f"Function {self.value} does not exist")
        args = func.children[1:-1]
        # raise if len(args) != len(self.children)
        if len(args) != len(self.children):
            raise TypeError(f"Function {self.value} expected {len(args)} arguments, got {len(self.children)}")
        new_table = SymbolTable()
        for i in range(len(args)):
            new_table.create_var(args[i].value)
            new_table.set_value(args[i].value,self.children[i].evaluate(symbol_table))
        return func.children[-1].evaluate(new_table)



class ReturnNode(Node):
    def evaluate(self,symbol_table):
        return self.children[0].evaluate(symbol_table)


class SwitchNode(Node):
    def evaluate(self, symbol_table):
        switch_value = self.children[0].evaluate(symbol_table)[0]
        for i in range(1, len(self.children)):           
            if isinstance(self.children[i], DefaultNode):
                self.children[i].evaluate(symbol_table)
                return
            elif self.children[i].children[0].evaluate(symbol_table)[0] == switch_value:
                self.children[i].evaluate(symbol_table)
                return
        return

    def __str__(self):
        return f"SwitchNode: ({self.children})"


class CaseNode(Node):
    def evaluate(self, symbol_table):
        return self.children[1].evaluate(symbol_table)

    def __str__(self):
        return f"CaseNode: ({self.children})"


class DefaultNode(Node):
    def evaluate(self, symbol_table):
        self.children[0].evaluate(symbol_table)

    def __str__(self):
        return f"DefaultNode: ({self.children})"
    
class TypeNode(Node):
    def evaluate(self,symbol_table):
        return self.value

    def __str__(self):
        return f"TypeNode({self.value})"

        