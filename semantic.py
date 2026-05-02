from errors import RoyalProtocolViolation

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def define(self, name, type_info):
        if name in self.symbols:
            raise RoyalProtocolViolation(f"Variable '{name}' already declared in this scope", "Semantic", "Error")
        self.symbols[name] = type_info

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        raise RoyalProtocolViolation(f"Undeclared variable '{name}'", "Semantic", "Error")

class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope

    def analyze(self, ast):
        self.visit(ast)

    def visit(self, node):
        if not node:
            return
        if isinstance(node, list):
            for n in node:
                self.visit(n)
            return

        method_name = 'visit_' + node.get('type', '')
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)

    def generic_visit(self, node):
        for key, value in node.items():
            if isinstance(value, dict) or isinstance(value, list):
                self.visit(value)

    def visit_Program(self, node):
        self.visit(node.get('body', []))

    def visit_Declaration(self, node):
        var_name = node['id']
        var_type = node.get('var_type', 'daulat')
        self.visit(node.get('value'))
        self.current_scope.define(var_name, var_type)

    def visit_Identifier(self, node):
        self.current_scope.lookup(node['value'])

    def visit_Assignment(self, node):
        var_name = node['left']
        self.current_scope.lookup(var_name)
        self.visit(node.get('right'))

    def visit_FunctionDeclaration(self, node):
        func_name = node['id']
        self.current_scope.define(func_name, "hukam")
        
        previous_scope = self.current_scope
        self.current_scope = SymbolTable(parent=previous_scope)
        
        for param in node.get('params', []):
            self.current_scope.define(param, "daulat")
            
        self.visit(node.get('body', []))
        self.current_scope = previous_scope

    def visit_FunctionCall(self, node):
        # Allow calling before declaration or builtin functions
        self.visit(node.get('arguments', []))

    def visit_For(self, node):
        previous_scope = self.current_scope
        self.current_scope = SymbolTable(parent=previous_scope)
        self.visit(node.get('init'))
        self.visit(node.get('condition'))
        self.visit(node.get('update'))
        self.visit(node.get('body'))
        self.current_scope = previous_scope
        
    def visit_If(self, node):
        self.visit(node.get('condition'))
        
        previous_scope = self.current_scope
        self.current_scope = SymbolTable(parent=previous_scope)
        self.visit(node.get('body'))
        self.current_scope = previous_scope
        
        for elif_block in node.get('elif_blocks', []):
            self.visit(elif_block.get('condition'))
            previous_scope = self.current_scope
            self.current_scope = SymbolTable(parent=previous_scope)
            self.visit(elif_block.get('body'))
            self.current_scope = previous_scope
            
        if node.get('else_body'):
            previous_scope = self.current_scope
            self.current_scope = SymbolTable(parent=previous_scope)
            self.visit(node.get('else_body'))
            self.current_scope = previous_scope

def analyze_semantics(ast):
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    return analyzer
