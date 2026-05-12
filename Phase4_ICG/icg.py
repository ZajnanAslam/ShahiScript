import os
import sys

class ICGGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, ast):
        self.visit(ast)
        return self.code

    def emit(self, instruction):
        self.code.append(instruction)

    def visit(self, node):
        if not node: return ""
        if isinstance(node, list):
            for n in node:
                self.visit(n)
            return ""
        
        method_name = 'visit_' + node.get('type', '')
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass

    def visit_Program(self, node):
        self.visit(node.get('body', []))

    def visit_NumberLiteral(self, node):
        return node['value']

    def visit_StringLiteral(self, node):
        return f"\"{node['value']}\""

    def visit_BooleanLiteral(self, node):
        return node['value']

    def visit_Identifier(self, node):
        return node['value']

    def visit_BinaryExpression(self, node):
        left = self.visit(node['left'])
        right = self.visit(node['right'])
        t = self.new_temp()
        self.emit(f"{t} = {left} {node['operator']} {right}")
        return t

    def visit_Declaration(self, node):
        val = self.visit(node.get('value'))
        self.emit(f"{node['id']} = {val}")
        return node['id']

    def visit_Assignment(self, node):
        val = self.visit(node.get('right'))
        self.emit(f"{node['left']} = {val}")
        return node['left']

    def visit_Print(self, node):
        val = self.visit(node.get('expression'))
        self.emit(f"PRINT {val}")

    def visit_If(self, node):
        cond = self.visit(node.get('condition'))
        end_label = self.new_label()
        next_label = self.new_label()
        
        self.emit(f"IF_FALSE {cond} GOTO {next_label}")
        self.visit(node.get('body'))
        self.emit(f"GOTO {end_label}")
        self.emit(f"{next_label}:")
        
        for elif_block in node.get('elif_blocks', []):
            elif_cond = self.visit(elif_block.get('condition'))
            next_elif = self.new_label()
            self.emit(f"IF_FALSE {elif_cond} GOTO {next_elif}")
            self.visit(elif_block.get('body'))
            self.emit(f"GOTO {end_label}")
            self.emit(f"{next_elif}:")
            
        if node.get('else_body'):
            self.visit(node.get('else_body'))
            
        self.emit(f"{end_label}:")

    def visit_While(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.emit(f"{start_label}:")
        cond = self.visit(node.get('condition'))
        self.emit(f"IF_FALSE {cond} GOTO {end_label}")
        self.visit(node.get('body'))
        self.emit(f"GOTO {start_label}")
        self.emit(f"{end_label}:")

    def visit_FunctionDeclaration(self, node):
        self.emit(f"FUNC {node['id']}:")
        for param in node.get('params', []):
            self.emit(f"PARAM {param}")
        self.visit(node.get('body'))
        self.emit(f"END FUNC {node['id']}")

    def visit_FunctionCall(self, node):
        for arg in node.get('arguments', []):
            val = self.visit(arg)
            self.emit(f"PUSH_ARG {val}")
        t = self.new_temp()
        self.emit(f"{t} = CALL {node['id']}")
        return t

    def visit_Return(self, node):
        val = self.visit(node.get('expression'))
        self.emit(f"RETURN {val}")

    def visit_ExpressionStatement(self, node):
        self.visit(node.get('expression'))


def generate_icg(ast):
    generator = ICGGenerator()
    return generator.generate(ast)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python icg.py <input_file.shahi>")
        sys.exit(1)
        
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from Phase1_Lexical.lexer import tokenize
        from Phase2_Syntax.parser import parse
        from Phase5_Optimization.optimizer import optimize_ast
        
        with open(sys.argv[1], 'r') as f:
            code = f.read()
            
        tokens = tokenize(code)
        ast = parse(tokens)
        opt_ast = optimize_ast(ast)
        tac = generate_icg(opt_ast)
        
        print("--- Intermediate Code Generation (TAC) ---")
        for line in tac:
            print(line)
    except Exception as e:
        print(f"ICG Error: {e}")
