class SymbolTable():
    def __init__(self):
        self.table = {}

    def get_value(self, key):
        return self.table[key]
    
    def has_value(self, key):
        return key in self.table
    
    def set_value(self, key, var):
        if key not in self.table:
            raise KeyError(f"Variable {key} not declared")
        self.table[key] = var # (value, type)

    def create_var(self, key, var_type):
        if key in self.table:
            raise KeyError(f"Variable {key} already declared")
        self.table[key] = (None,var_type)