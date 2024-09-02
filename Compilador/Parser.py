from Tokenizer import Tokenizer
from Nodes import *


class Parser():
    my_tokenizer: Tokenizer

    def __init__(self):
        pass

    @staticmethod
    def parse_expression():
        result = Parser.parse_term()
        while Parser.my_tokenizer.next.typ == "PLUS" or Parser.my_tokenizer.next.typ == "MINUS":
            if Parser.my_tokenizer.next.typ == "PLUS":
                Parser.my_tokenizer.select_next()
                result = BinOp("+", [result, Parser.parse_term()])
            elif Parser.my_tokenizer.next.typ == "MINUS":
                Parser.my_tokenizer.select_next()
                result = BinOp("-", [result, Parser.parse_term()])

            else:
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position} ")
        return result

    @staticmethod
    def parse_term():
        result = Parser.parse_factor()
        while Parser.my_tokenizer.next.typ == "MULT" or Parser.my_tokenizer.next.typ == "DIV":
            if Parser.my_tokenizer.next.typ == "MULT":
                Parser.my_tokenizer.select_next()
                result = BinOp("*", [result, Parser.parse_factor()])
            elif Parser.my_tokenizer.next.typ == "DIV":
                Parser.my_tokenizer.select_next()
                result = BinOp("/", [result, Parser.parse_factor()])

            else:
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position} ")

        return result

    @staticmethod
    def parse_factor():
        if Parser.my_tokenizer.next.typ == "NUMBER":
            result = IntVal(value=Parser.my_tokenizer.next.value, children=[])
            Parser.my_tokenizer.select_next()
            return result
        elif Parser.my_tokenizer.next.typ == "PLUS":
            Parser.my_tokenizer.select_next()
            return UnOp("+", [Parser.parse_factor()])
        elif Parser.my_tokenizer.next.typ == "MINUS":
            Parser.my_tokenizer.select_next()
            return UnOp("-", [Parser.parse_factor()])
        elif Parser.my_tokenizer.next.typ == "not":
            Parser.my_tokenizer.select_next()
            return UnOp("not", [Parser.parse_factor()])
        elif Parser.my_tokenizer.next.typ == "LPAREN":
            Parser.my_tokenizer.select_next()
            result = Parser.parse_bool_expression()
            if Parser.my_tokenizer.next.typ != "RPAREN":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position} ")
            Parser.my_tokenizer.select_next()
            return result
        elif Parser.my_tokenizer.next.typ == "ID":
            result = Identifier(
                value=Parser.my_tokenizer.next.value, children=[])
            name = Parser.my_tokenizer.next.value
            Parser.my_tokenizer.select_next()
            return result
        elif Parser.my_tokenizer.next.typ == "read":
            Parser.my_tokenizer.select_next()
            if Parser.my_tokenizer.next.typ != "LPAREN":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position} ")
            Parser.my_tokenizer.select_next()
            if Parser.my_tokenizer.next.typ != "RPAREN":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position} ")
            Parser.my_tokenizer.select_next()
            return ReadNode(value=0, children=[])
        elif Parser.my_tokenizer.next.typ == "STRING":
            result = StrVal(value=Parser.my_tokenizer.next.value, children=[])
            Parser.my_tokenizer.select_next()
            return result
        else:
            raise SyntaxError(
                f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position} ")

    @staticmethod
    def parse_statement():
        if Parser.my_tokenizer.next.typ == "ENDL":
            Parser.my_tokenizer.select_next()
            return NoOp()

        elif Parser.my_tokenizer.next.typ == "ID":
            iden = Identifier(
                value=Parser.my_tokenizer.next.value, children=[])
            Parser.my_tokenizer.select_next()
            if Parser.my_tokenizer.next.typ == "=":
                Parser.my_tokenizer.select_next()
                return Assignment(value=0, children=[iden, Parser.parse_bool_expression()])
            elif Parser.my_tokenizer.next.typ == "LPAREN":
                Parser.my_tokenizer.select_next()
                children = []
                if Parser.my_tokenizer.next.typ != "RPAREN":
                    children.append(Parser.parse_bool_expression())
                    while Parser.my_tokenizer.next.typ == "COMMA":
                        Parser.my_tokenizer.select_next()
                        children.append(Parser.parse_bool_expression())
                if Parser.my_tokenizer.next.typ != "RPAREN":
                    raise SyntaxError(
                        f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
                Parser.my_tokenizer.select_next()
                return FuncCall(value=iden.value, children=children)
            else:
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position} with value {Parser.my_tokenizer.next.value}")

        elif Parser.my_tokenizer.next.typ == "int" or Parser.my_tokenizer.next.typ == "string":
            var_type = Parser.my_tokenizer.next.typ
            typeNode = TypeNode(value=var_type, children=[])
            Parser.my_tokenizer.select_next()
            if Parser.my_tokenizer.next.typ != "ID":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
            iden = Identifier(
                value=Parser.my_tokenizer.next.value, children=[])
            Parser.my_tokenizer.select_next()
            if Parser.my_tokenizer.next.typ == "=":
                Parser.my_tokenizer.select_next()
                value = Parser.parse_bool_expression()
                if var_type == "int" and type(value) != IntVal:
                    raise SyntaxError(f"Cannot assign {value} to int")
                elif var_type == "string" and type(value) != StrVal:
                    raise SyntaxError(f"Cannot assign {value} to string")
                return VarDec(value=0, children=[iden, typeNode, value])
            return VarDec(value=0, children=[iden, typeNode])

        elif Parser.my_tokenizer.next.typ == "print":
            Parser.my_tokenizer.select_next()
            if Parser.my_tokenizer.next.typ != "LPAREN":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
            Parser.my_tokenizer.select_next()
            result = Parser.parse_bool_expression()
            if Parser.my_tokenizer.next.typ != "RPAREN":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
            Parser.my_tokenizer.select_next()
            return PrintNode(value=0, children=[result])

        elif Parser.my_tokenizer.next.typ == "while":
            Parser.my_tokenizer.select_next()
            condition = Parser.parse_bool_expression()
            while Parser.my_tokenizer.next.typ == "ENDL":
                Parser.my_tokenizer.select_next()
            if Parser.my_tokenizer.next.typ != "LBRACE":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
            Parser.my_tokenizer.select_next()
            statements = []
            while Parser.my_tokenizer.next.typ != "RBRACE":
                statements.append(Parser.parse_statement())
            Parser.my_tokenizer.select_next()
            block = Block(value=0, children=statements)
            while_node = WhileNode(children=[condition, block])
            return while_node

        elif Parser.my_tokenizer.next.typ == "if":
            Parser.my_tokenizer.select_next()
            condition = Parser.parse_bool_expression()
            while Parser.my_tokenizer.next.typ == "ENDL":
                Parser.my_tokenizer.select_next()
            if Parser.my_tokenizer.next.typ != "LBRACE":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
            Parser.my_tokenizer.select_next()
            statements = []
            while Parser.my_tokenizer.next.typ != "RBRACE":
                statements.append(Parser.parse_statement())
            Parser.my_tokenizer.select_next()
            if_block = Block(value=0, children=statements)
            if_node = IfNode(children=[condition, if_block])
            if Parser.my_tokenizer.next.typ == "else":
                Parser.my_tokenizer.select_next()
                if Parser.my_tokenizer.next.typ != "LBRACE":
                    raise SyntaxError(
                        f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
                Parser.my_tokenizer.select_next()
                else_statements = []
                while Parser.my_tokenizer.next.typ != "RBRACE":
                    else_statements.append(Parser.parse_statement())
                Parser.my_tokenizer.select_next()
                else_block = Block(value=0, children=else_statements)
                if_node = IfNode(children=[condition, if_block, else_block])
            return if_node

        elif Parser.my_tokenizer.next.typ == "switch":
            Parser.my_tokenizer.select_next()
            if Parser.my_tokenizer.next.typ != "ID":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
            switch_expr = Identifier(
                value=Parser.my_tokenizer.next.value, children=[])
            switch_children = [switch_expr]
            Parser.my_tokenizer.select_next()
            if Parser.my_tokenizer.next.typ != "LPAREN":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
            Parser.my_tokenizer.select_next()

            while Parser.my_tokenizer.next.typ != "RPAREN":
                while Parser.my_tokenizer.next.typ == "ENDL":
                    Parser.my_tokenizer.select_next()
                if Parser.my_tokenizer.next.typ == "case":
                    Parser.my_tokenizer.select_next()
                    if Parser.my_tokenizer.next.typ == "NUMBER":
                        case_expr = IntVal(
                            value=Parser.my_tokenizer.next.value, children=[])
                        Parser.my_tokenizer.select_next()
                    elif Parser.my_tokenizer.next.typ == "STRING":
                        case_expr = StrVal(
                            value=Parser.my_tokenizer.next.value, children=[])
                        Parser.my_tokenizer.select_next()
                    while Parser.my_tokenizer.next.typ == "ENDL":
                        Parser.my_tokenizer.select_next()
                    if Parser.my_tokenizer.next.typ != "LBRACE":
                        raise SyntaxError(
                            f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
                    Parser.my_tokenizer.select_next()
                    case_statements = []
                    while Parser.my_tokenizer.next.typ != "RBRACE":
                        case_statements.append(Parser.parse_statement())
                    Parser.my_tokenizer.select_next()
                    case_block = Block(value=0, children=case_statements)
                    case_node = CaseNode(children=[case_expr, case_block])
                    switch_children.append(case_node)
                elif Parser.my_tokenizer.next.typ == "default":
                    Parser.my_tokenizer.select_next()
                    while Parser.my_tokenizer.next.typ == "ENDL":
                        Parser.my_tokenizer.select_next()
                    if Parser.my_tokenizer.next.typ != "LBRACE":
                        raise SyntaxError(
                            f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
                    Parser.my_tokenizer.select_next()
                    default_statements = []
                    while Parser.my_tokenizer.next.typ != "RBRACE":
                        default_statements.append(Parser.parse_statement())
                    Parser.my_tokenizer.select_next()
                    default_block = Block(value=0, children=default_statements)
                    default_node = DefaultNode(children=[default_block])
                    switch_children.append(default_node)
                elif Parser.my_tokenizer.next.typ == "RPAREN":
                    break
                else:
                    raise SyntaxError(
                        f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")

            if Parser.my_tokenizer.next.typ != "RPAREN":
                raise SyntaxError(
                    f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position}")
            Parser.my_tokenizer.select_next()
            switch_node = SwitchNode(children=switch_children)
            return switch_node

        else:
            return Parser.parse_bool_expression()

    @staticmethod
    def parse_block():
        result = Block(value=0, children=[])
        while Parser.my_tokenizer.next.typ != "EOF":
            result.children.append(Parser.parse_statement())
        return result

    @staticmethod
    def parse_rel_expression():
        result = Parser.parse_expression()
        if Parser.my_tokenizer.next.typ == "==":
            Parser.my_tokenizer.select_next()
            result = BinOp("==", [result, Parser.parse_expression()])
        elif Parser.my_tokenizer.next.typ == ">":
            Parser.my_tokenizer.select_next()
            result = BinOp(">", [result, Parser.parse_expression()])
        elif Parser.my_tokenizer.next.typ == "<":
            Parser.my_tokenizer.select_next()
            result = BinOp("<", [result, Parser.parse_expression()])
        return result

    @staticmethod
    def parse_bool_term():
        result = Parser.parse_rel_expression()
        while Parser.my_tokenizer.next.typ == "and":
            Parser.my_tokenizer.select_next()
            result = BinOp("and", [result, Parser.parse_rel_expression()])
        return result

    @staticmethod
    def parse_bool_expression():
        result = Parser.parse_bool_term()
        while Parser.my_tokenizer.next.typ == "or":
            Parser.my_tokenizer.select_next()
            result = BinOp("or", [result, Parser.parse_bool_term()])
        return result

    @staticmethod
    def run(code):
        Parser.my_tokenizer = Tokenizer(code, 0)
        Parser.my_tokenizer.select_next()
        result = Parser.parse_block()
        if Parser.my_tokenizer.next.typ != "EOF":
            raise SyntaxError(
                f"Unexpected token {Parser.my_tokenizer.next.typ} at {Parser.my_tokenizer.position} ")
        return result
