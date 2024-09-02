class Token():
    typ: str
    value: int

    def __init__(self,typ,value) -> None:
        self.typ=typ
        self.value=value

    def __str__(self):
        return f"type: {self.typ} value: {self.value}"

if __name__ == "__main__":
    x = Token("PLUS",1)
    print(x)