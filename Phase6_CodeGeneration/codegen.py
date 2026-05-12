import os
import sys

class CodeGenerator:
    def __init__(self):
        self.code = []
        self.label_count = 0

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, instruction):
        self.code.append(instruction)

    def generate(self, ast):
        self.visit(ast)
        return self.code

    def visit(self, node):
        if not node: return
        if isinstance(node, list):
            for n in node:
                self.visit(n)
            return
        
        method_name = 'visit_' + node.get('type', '')
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)

    def generic_visit(self, node):
        pass

    def visit_Program(self, node):
        self.visit(node.get('body', []))
        self.emit("HALT")

    def visit_NumberLiteral(self, node):
        self.emit(f"PUSH {node['value']}")

    def visit_StringLiteral(self, node):
        self.emit(f"PUSH \"{node['value']}\"")

    def visit_BooleanLiteral(self, node):
        val = 1 if node['value'] == 'sach' else 0
        self.emit(f"PUSH {val}")

    def visit_Identifier(self, node):
        self.emit(f"LOAD {node['value']}")

    def visit_BinaryExpression(self, node):
        self.visit(node['left'])
        self.visit(node['right'])
        op = node['operator']
        if op == '+': self.emit("ADD")
        elif op == '-': self.emit("SUB")
        elif op == '*': self.emit("MUL")
        elif op == '/': self.emit("DIV")
        elif op == '==': self.emit("EQ")
        elif op == '!=': self.emit("NEQ")
        elif op == '>': self.emit("GT")
        elif op == '<': self.emit("LT")

    def visit_Declaration(self, node):
        self.visit(node.get('value'))
        self.emit(f"STORE {node['id']}")

    def visit_Assignment(self, node):
        self.visit(node.get('right'))
        self.emit(f"STORE {node['left']}")

    def visit_Print(self, node):
        self.visit(node.get('expression'))
        self.emit("PRINT")

    def visit_If(self, node):
        end_label = self.new_label()
        next_label = self.new_label()
        
        self.visit(node.get('condition'))
        self.emit(f"JMP_FALSE {next_label}")
        self.visit(node.get('body'))
        self.emit(f"JMP {end_label}")
        self.emit(f"{next_label}:")
        
        for elif_block in node.get('elif_blocks', []):
            next_elif = self.new_label()
            self.visit(elif_block.get('condition'))
            self.emit(f"JMP_FALSE {next_elif}")
            self.visit(elif_block.get('body'))
            self.emit(f"JMP {end_label}")
            self.emit(f"{next_elif}:")
            
        if node.get('else_body'):
            self.visit(node.get('else_body'))
            
        self.emit(f"{end_label}:")

    def visit_While(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.emit(f"{start_label}:")
        self.visit(node.get('condition'))
        self.emit(f"JMP_FALSE {end_label}")
        self.visit(node.get('body'))
        self.emit(f"JMP {start_label}")
        self.emit(f"{end_label}:")

    def visit_FunctionDeclaration(self, node):
        self.emit(f"FUNC {node['id']}:")
        for param in reversed(node.get('params', [])):
            self.emit(f"POP {param}")
        self.visit(node.get('body'))
        self.emit("RET")

    def visit_FunctionCall(self, node):
        for arg in node.get('arguments', []):
            self.visit(arg)
        self.emit(f"CALL {node['id']}")

    def visit_Return(self, node):
        self.visit(node.get('expression'))
        self.emit("RET")

    def visit_ExpressionStatement(self, node):
        self.visit(node.get('expression'))


def generate_target_code(ast):
    generator = CodeGenerator()
    return generator.generate(ast)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python codegen.py <input_file.shahi>")
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
        asm = generate_target_code(opt_ast)
        
        print("--- Target Code Generation (Stack Machine ASM) ---")
        for line in asm:
            print(line)
    except Exception as e:
        print(f"Code Generation Error: {e}")
