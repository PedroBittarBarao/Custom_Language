from tkn import tkn
from PrePro import PrePro

reserved_words = ["print","if","else","while","and","or","int","string","switch","case","default"]

class tokenizer():
    source :str
    position: int
    next:tkn
    next = None

    def __init__(self,source,position) -> None:
        self.source = PrePro.filter(source)
        self.position = position

    def select_next(self) -> None:
        if self.position < len(self.source):
            while self.source[self.position] == " " or self.source[self.position] == "\t":
                if self.position == len(self.source) - 1:
                    self.next=tkn("EOF",0)
                    return
                self.position += 1
            if self.source[self.position] == "+":
                self.position += 1
                self.next = tkn("PLUS",0)
            elif self.source[self.position] == "-":
                self.next = tkn("MINUS",0)
                self.position += 1
            elif self.source[self.position] == "*":
                self.next = tkn("MULT",0)
                self.position += 1
            elif self.source[self.position] == "/":
                self.next = tkn("DIV",0)
                self.position += 1
            elif self.source[self.position] == "(":
                self.next = tkn("LPAREN",0)
                self.position += 1
            elif self.source[self.position] == ")":
                self.next = tkn("RPAREN",0)
                self.position += 1
            elif self.source[self.position].isdigit():
                start = self.position
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    self.position += 1
                self.next = tkn("NUMBER",int(self.source[start:self.position]))
            elif self.source[self.position] == "\n": # ??????
                self.next = tkn("ENDL",0)
                self.position += 1
            elif self.source[self.position] == "=":
                if self.source[self.position + 1] == "=":
                    self.next = tkn("==",0)
                    self.position += 2
                else:
                    self.next = tkn("=",0)
                    self.position += 1
            elif str.isalpha(self.source[self.position]):
                start = self.position
                while self.position < len(self.source) and (
                    self.source[self.position].isalnum() or self.source[self.position] == "_"):
                    self.position += 1
                self.next = tkn("ID",self.source[start:self.position])
                if self.next.value in reserved_words:
                    self.next = tkn(self.next.value,0)
            elif self.source[self.position] == ">":
                self.next = tkn(">",0)
                self.position += 1
            elif self.source[self.position] == "<":
                self.next = tkn("<",0)
                self.position += 1
            elif self.source[self.position] == "{":
                self.next = tkn("LBRACE",0)
                self.position += 1
            elif self.source[self.position] == "}":
                self.next = tkn("RBRACE",0)
                self.position += 1
            elif self.source[self.position] == ".":
                if self.source[self.position + 1] == ".":
                    self.next = tkn("CONCAT",0)
                    self.position += 2
                else:
                    raise SyntaxError(
                        f"Unexpected character {self.source[self.position]} at {self.position}")
            elif self.source[self.position] == '"':
                start = self.position + 1
                self.position += 1
                while self.source[self.position] != '"':
                    self.position += 1
                    if self.position == len(self.source):
                        raise SyntaxError("Expected '\"'")
                self.next = tkn("STRING",self.source[start:self.position])
                self.position += 1
            elif self.source[self.position] == ",":
                self.next = tkn("COMMA",0)
                self.position += 1
            else:
                raise SyntaxError(
                    f"Unexpected character {self.source[self.position]} at {self.position}")            
        else:
            self.next = tkn("EOF",0)
    def __str__(self) -> str:
        return f"next: '{self.next}', position: {self.position}"

if __name__ == "__main__":
    code = '''int x = 21
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
)'''
    x = tokenizer(code,0)
    while x.next == None or x.next.typ != "EOF":
        print(x)
        x.select_next()
        