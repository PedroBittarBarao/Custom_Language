from tokenizer import tokenizer
from Nodes import *


class prsr():
    my_tokenizer:tokenizer
    
    def __init__(self):
        pass

    @staticmethod
    def parse_expression():
        result = prsr.parse_term() 
        while prsr.my_tokenizer.next.typ == "PLUS" or prsr.my_tokenizer.next.typ == "MINUS":
            if prsr.my_tokenizer.next.typ == "PLUS":
                prsr.my_tokenizer.select_next()
                result = BinOp("+",[result,prsr.parse_term()])
            elif prsr.my_tokenizer.next.typ == "MINUS":
                prsr.my_tokenizer.select_next()
                result = BinOp("-",[result,prsr.parse_term()])
            
            else:
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position} ")
        return result

    @staticmethod
    def parse_term():
        result = prsr.parse_factor()
        while prsr.my_tokenizer.next.typ == "MULT" or prsr.my_tokenizer.next.typ == "DIV":
            if prsr.my_tokenizer.next.typ == "MULT":
                prsr.my_tokenizer.select_next()
                result = BinOp("*",[result,prsr.parse_factor()])
            elif prsr.my_tokenizer.next.typ == "DIV":
                prsr.my_tokenizer.select_next()
                result = BinOp("/",[result,prsr.parse_factor()])
            
            else:
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position} ")

        return result
    
    @staticmethod
    def parse_factor():
        if prsr.my_tokenizer.next.typ == "NUMBER":
            result = IntVal(value=prsr.my_tokenizer.next.value,children=[])
            prsr.my_tokenizer.select_next()
            return result
        elif prsr.my_tokenizer.next.typ == "PLUS":
            prsr.my_tokenizer.select_next()
            return UnOp("+",[prsr.parse_factor()])
        elif prsr.my_tokenizer.next.typ == "MINUS":
            prsr.my_tokenizer.select_next()
            return UnOp("-",[prsr.parse_factor()])
        elif prsr.my_tokenizer.next.typ == "not":
            prsr.my_tokenizer.select_next()
            return UnOp("not",[prsr.parse_factor()])
        elif prsr.my_tokenizer.next.typ == "LPAREN":
            prsr.my_tokenizer.select_next()
            result = prsr.parse_bool_expression()
            if prsr.my_tokenizer.next.typ != "RPAREN":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position} ")
            prsr.my_tokenizer.select_next()
            return result
        elif prsr.my_tokenizer.next.typ == "ID":
            result = Identifier(value=prsr.my_tokenizer.next.value,children=[])
            name = prsr.my_tokenizer.next.value
            prsr.my_tokenizer.select_next()
            return result
        elif prsr.my_tokenizer.next.typ == "read":
            prsr.my_tokenizer.select_next()
            if prsr.my_tokenizer.next.typ != "LPAREN":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position} ")
            prsr.my_tokenizer.select_next()
            if prsr.my_tokenizer.next.typ != "RPAREN":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position} ")
            prsr.my_tokenizer.select_next()
            return readNode(value=0,children=[])
        elif prsr.my_tokenizer.next.typ == "STRING":
            result = StrVal(value=prsr.my_tokenizer.next.value,children=[])
            prsr.my_tokenizer.select_next()
            return result
        else:
            raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position} ")
        
    @staticmethod
    def parse_statement():
        if prsr.my_tokenizer.next.typ == "ENDL":
            prsr.my_tokenizer.select_next()
            return NoOp()

        elif prsr.my_tokenizer.next.typ == "ID":
            iden = Identifier(value=prsr.my_tokenizer.next.value, children=[])
            prsr.my_tokenizer.select_next()
            if prsr.my_tokenizer.next.typ == "=":
                prsr.my_tokenizer.select_next()
                return Assignment(value=0, children=[iden, prsr.parse_bool_expression()])
            elif prsr.my_tokenizer.next.typ == "LPAREN":
                prsr.my_tokenizer.select_next()
                children = []
                if prsr.my_tokenizer.next.typ != "RPAREN":
                    children.append(prsr.parse_bool_expression())
                    while prsr.my_tokenizer.next.typ == "COMMA":
                        prsr.my_tokenizer.select_next()
                        children.append(prsr.parse_bool_expression())
                if prsr.my_tokenizer.next.typ != "RPAREN":
                    raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
                prsr.my_tokenizer.select_next()
                return FuncCall(value=iden.value, children=children)
            else:
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position} with value {prsr.my_tokenizer.next.value}")

        elif prsr.my_tokenizer.next.typ == "int" or prsr.my_tokenizer.next.typ == "string":
            var_type = prsr.my_tokenizer.next.typ
            typeNode = TypeNode(value=var_type, children=[])
            prsr.my_tokenizer.select_next()
            if prsr.my_tokenizer.next.typ != "ID":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
            iden = Identifier(value=prsr.my_tokenizer.next.value, children=[])
            prsr.my_tokenizer.select_next()
            if prsr.my_tokenizer.next.typ == "=":
                prsr.my_tokenizer.select_next()
                value = prsr.parse_bool_expression()
                if var_type == "int" and type(value) != IntVal:
                    raise Exception(f"Cannot assign {value} to int")
                elif var_type == "string" and type(value) != StrVal:
                    raise Exception(f"Cannot assign {value} to string")
                return VarDec(value=0, children=[iden,typeNode, value])
            return VarDec(value=0, children=[iden,typeNode])

        elif prsr.my_tokenizer.next.typ == "print":
            prsr.my_tokenizer.select_next()
            if prsr.my_tokenizer.next.typ != "LPAREN":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
            prsr.my_tokenizer.select_next()
            result = prsr.parse_bool_expression()
            if prsr.my_tokenizer.next.typ != "RPAREN":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
            prsr.my_tokenizer.select_next()
            return printNode(value=0, children=[result])

        elif prsr.my_tokenizer.next.typ == "while":
            prsr.my_tokenizer.select_next()
            condition = prsr.parse_bool_expression()
            while prsr.my_tokenizer.next.typ == "ENDL":
                prsr.my_tokenizer.select_next()
            if prsr.my_tokenizer.next.typ != "LBRACE":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
            prsr.my_tokenizer.select_next()
            statements = []
            while prsr.my_tokenizer.next.typ != "RBRACE":
                statements.append(prsr.parse_statement())
            prsr.my_tokenizer.select_next()
            block = Block(value=0, children=statements)
            while_node = whileNode(children=[condition, block])
            return while_node

        elif prsr.my_tokenizer.next.typ == "if":
            prsr.my_tokenizer.select_next()
            condition = prsr.parse_bool_expression()
            while prsr.my_tokenizer.next.typ == "ENDL":
                prsr.my_tokenizer.select_next()
            if prsr.my_tokenizer.next.typ != "LBRACE":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
            prsr.my_tokenizer.select_next()
            statements = []
            while prsr.my_tokenizer.next.typ != "RBRACE":
                statements.append(prsr.parse_statement())
            prsr.my_tokenizer.select_next()
            if_block = Block(value=0, children=statements)
            if_node = ifNode(children=[condition, if_block])
            if prsr.my_tokenizer.next.typ == "else":
                prsr.my_tokenizer.select_next()
                if prsr.my_tokenizer.next.typ != "LBRACE":
                    raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
                prsr.my_tokenizer.select_next()
                else_statements = []
                while prsr.my_tokenizer.next.typ != "RBRACE":
                    else_statements.append(prsr.parse_statement())
                prsr.my_tokenizer.select_next()
                else_block = Block(value=0, children=else_statements)
                if_node = ifNode(children=[condition, if_block, else_block])
            return if_node

        elif prsr.my_tokenizer.next.typ == "switch":
            prsr.my_tokenizer.select_next()
            if prsr.my_tokenizer.next.typ != "ID":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
            switch_expr = Identifier(value=prsr.my_tokenizer.next.value, children=[])
            switch_children = [switch_expr]
            prsr.my_tokenizer.select_next()
            if prsr.my_tokenizer.next.typ != "LPAREN":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
            prsr.my_tokenizer.select_next()
            
            while prsr.my_tokenizer.next.typ != "RPAREN":
                while prsr.my_tokenizer.next.typ == "ENDL":
                    prsr.my_tokenizer.select_next()
                if prsr.my_tokenizer.next.typ == "case":
                    prsr.my_tokenizer.select_next()
                    if prsr.my_tokenizer.next.typ == "NUMBER":
                        case_expr = IntVal(value=prsr.my_tokenizer.next.value, children=[])
                        prsr.my_tokenizer.select_next()
                    elif prsr.my_tokenizer.next.typ == "STRING":
                        case_expr = StrVal(value=prsr.my_tokenizer.next.value, children=[])
                        prsr.my_tokenizer.select_next()
                    while prsr.my_tokenizer.next.typ == "ENDL":
                        prsr.my_tokenizer.select_next()
                    if prsr.my_tokenizer.next.typ != "LBRACE":
                        raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
                    prsr.my_tokenizer.select_next()
                    case_statements = []
                    while prsr.my_tokenizer.next.typ != "RBRACE":
                        case_statements.append(prsr.parse_statement())
                    prsr.my_tokenizer.select_next()
                    case_block = Block(value=0, children=case_statements)
                    case_node = CaseNode(children=[case_expr, case_block])
                    switch_children.append(case_node)
                elif prsr.my_tokenizer.next.typ == "default":
                    prsr.my_tokenizer.select_next()
                    while prsr.my_tokenizer.next.typ == "ENDL":
                        prsr.my_tokenizer.select_next()
                    if prsr.my_tokenizer.next.typ != "LBRACE":
                        raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
                    prsr.my_tokenizer.select_next()
                    default_statements = []
                    while prsr.my_tokenizer.next.typ != "RBRACE":
                        default_statements.append(prsr.parse_statement())
                    prsr.my_tokenizer.select_next()
                    default_block = Block(value=0, children=default_statements)
                    default_node = DefaultNode(children=[default_block])
                    switch_children.append(default_node)
                elif prsr.my_tokenizer.next.typ == "RPAREN":
                    break
                else:
                    raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")

            if prsr.my_tokenizer.next.typ != "RPAREN":
                raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position}")
            prsr.my_tokenizer.select_next()
            switch_node = SwitchNode(children=switch_children)
            return switch_node

        else:
            return prsr.parse_bool_expression()


    @staticmethod
    def parse_block():
        result = Block(value=0,children=[])
        while prsr.my_tokenizer.next.typ != "EOF":
            result.children.append(prsr.parse_statement())
        return result
    
    @staticmethod
    def parse_rel_expression():
        result = prsr.parse_expression()
        if prsr.my_tokenizer.next.typ == "==":
            prsr.my_tokenizer.select_next()
            result = BinOp("==",[result,prsr.parse_expression()])
        elif prsr.my_tokenizer.next.typ == ">":
            prsr.my_tokenizer.select_next()
            result = BinOp(">",[result,prsr.parse_expression()])
        elif prsr.my_tokenizer.next.typ == "<":
            prsr.my_tokenizer.select_next()
            result = BinOp("<",[result,prsr.parse_expression()])
        return result
    
    @staticmethod
    def parse_bool_term():
        result = prsr.parse_rel_expression()
        while prsr.my_tokenizer.next.typ == "and":
            prsr.my_tokenizer.select_next()
            result = BinOp("and",[result,prsr.parse_rel_expression()])
        return result

    @staticmethod
    def parse_bool_expression():
        result = prsr.parse_bool_term()
        while prsr.my_tokenizer.next.typ == "or":
            prsr.my_tokenizer.select_next()
            result = BinOp("or",[result,prsr.parse_bool_term()])
        return result
        


    @staticmethod
    def run(code):
        prsr.my_tokenizer = tokenizer(code,0)
        prsr.my_tokenizer.select_next()
        result = prsr.parse_block()
        if prsr.my_tokenizer.next.typ != "EOF":
            raise Exception(f"Unexpected token {prsr.my_tokenizer.next.typ} at {prsr.my_tokenizer.position} ")
        return result
    