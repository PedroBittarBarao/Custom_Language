class FuncTable():
    table = {}

    def setFunc(Name, Func):
        if Name in FuncTable.table:
            raise KeyError(f"Function {Name} already exists")
        FuncTable.table[Name] = Func

    def getFunc(Name):
        return FuncTable.table[Name]

    def isInTable(Name):
        return Name in FuncTable.table


if __name__ == "__main__":
    FuncTable.setFunc("funcao", "NODE")
    print(FuncTable.getFunc("funcao"))
