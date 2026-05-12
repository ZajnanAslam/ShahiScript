from errors import RoyalProtocolViolation

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.globals = {}
        self.environment = [self.globals]
        self.functions = {}

    def define(self, name, value):
        self.environment[-1][name] = value

    def assign(self, name, value):
        for env in reversed(self.environment):
            if name in env:
                env[name] = value
                return
        self.environment[-1][name] = value

    def lookup(self, name):
        for env in reversed(self.environment):
            if name in env:
                return env[name]
        raise RoyalProtocolViolation(f"Undeclared variable '{name}' at runtime", "Runtime", "Error")

    def push_env(self):
        self.environment.append({})

    def pop_env(self):
        self.environment.pop()

    def evaluate(self, node):
        if not node: return None
        if isinstance(node, list):
            result = None
            for n in node:
                result = self.evaluate(n)
            return result
            
        method_name = 'eval_' + node.get('type', '')
        evaluator = getattr(self, method_name, self.generic_eval)
        return evaluator(node)

    def generic_eval(self, node):
        pass

    def eval_Program(self, node):
        return self.evaluate(node.get('body', []))

    def eval_NumberLiteral(self, node):
        val = node['value']
        return float(val) if '.' in val else int(val)

    def eval_StringLiteral(self, node):
        return node['value'].strip('"')

    def eval_BooleanLiteral(self, node):
        return True if node['value'] == 'sach' else False

    def eval_Identifier(self, node):
        return self.lookup(node['value'])

    def eval_ArrayLiteral(self, node):
        return [self.evaluate(el) for el in node.get('elements', [])]

    def eval_BinaryExpression(self, node):
        left = self.evaluate(node['left'])
        right = self.evaluate(node['right'])
        op = node['operator']

        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/': return left / right
        if op == '>': return left > right
        if op == '<': return left < right
        if op == '==': return left == right
        if op == '!=': return left != right

    def eval_Declaration(self, node):
        val = self.evaluate(node.get('value'))
        self.define(node['id'], val)
        return val

    def eval_Assignment(self, node):
        val = self.evaluate(node.get('right'))
        self.assign(node['left'], val)
        return val

    def eval_Print(self, node):
        val = self.evaluate(node.get('expression'))
        # Convert True/False to sach/ghalat for output
        if val is True: val = "sach"
        elif val is False: val = "ghalat"
        print(val)
        return val

    def eval_InputCall(self, node):
        prompt = node.get('prompt', '').strip('"')
        return input(prompt)

    def eval_If(self, node):
        cond = self.evaluate(node.get('condition'))
        if cond:
            self.push_env()
            self.evaluate(node.get('body'))
            self.pop_env()
            return

        for elif_block in node.get('elif_blocks', []):
            if self.evaluate(elif_block.get('condition')):
                self.push_env()
                self.evaluate(elif_block.get('body'))
                self.pop_env()
                return

        if node.get('else_body'):
            self.push_env()
            self.evaluate(node.get('else_body'))
            self.pop_env()

    def eval_While(self, node):
        while self.evaluate(node.get('condition')):
            self.push_env()
            self.evaluate(node.get('body'))
            self.pop_env()

    def eval_DoWhile(self, node):
        while True:
            self.push_env()
            self.evaluate(node.get('body'))
            self.pop_env()
            if not self.evaluate(node.get('condition')):
                break

    def eval_For(self, node):
        self.push_env()
        self.evaluate(node.get('init'))
        while self.evaluate(node.get('condition')):
            self.push_env()
            self.evaluate(node.get('body'))
            self.pop_env()
            self.evaluate(node.get('update'))
        self.pop_env()

    def eval_FunctionDeclaration(self, node):
        self.functions[node['id']] = node

    def eval_FunctionCall(self, node):
        func_id = node['id']
        if func_id not in self.functions:
            raise RoyalProtocolViolation(f"Undeclared hukam '{func_id}'", "Runtime", "Error")
            
        func_node = self.functions[func_id]
        args = [self.evaluate(arg) for arg in node.get('arguments', [])]
        
        self.push_env()
        for i, param in enumerate(func_node.get('params', [])):
            val = args[i] if i < len(args) else None
            self.define(param, val)
            
        result = None
        try:
            self.evaluate(func_node.get('body', []))
        except ReturnException as e:
            result = e.value
            
        self.pop_env()
        return result

    def eval_Return(self, node):
        val = self.evaluate(node.get('expression'))
        raise ReturnException(val)

    def eval_ExpressionStatement(self, node):
        return self.evaluate(node.get('expression'))

def interpret(ast):
    Interpreter().evaluate(ast)
