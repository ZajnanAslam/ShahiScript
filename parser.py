from errors import RoyalProtocolViolation

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def match(self, expected_type):
        token = self.current_token()
        if token and token.type == expected_type:
            self.advance()
            return token
        else:
            line = token.line if token else "EOF"
            col = token.column if token else "EOF"
            val = token.value if token else "EOF"
            raise RoyalProtocolViolation(f"Expected {expected_type}, but found {val!r}", line, col)

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        self.match('BISMILLAH')
        statements = self.parse_statement_list()
        self.match('ALLAH_HAFIZ')
        return {"type": "Program", "body": statements}

    def parse_statement_list(self):
        statements = []
        while self.current_token() and self.current_token().type not in ('ALLAH_HAFIZ', 'KHATAM', 'RBRACE', 'VARNA', 'WARNA_AGAR'):
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.current_token()
        if not token:
            raise RoyalProtocolViolation("Unexpected EOF", "EOF", "EOF")

        if token.type in ('ADAD', 'ASHARIYA', 'JUMLA', 'HAQEEQAT', 'FEHRIST', 'DAULAT'):
            return self.parse_declaration()
        elif token.type == 'FARMAN':
            return self.parse_print()
        elif token.type == 'AGAR':
            return self.parse_if()
        elif token.type == 'JAB_TAK':
            return self.parse_while()
        elif token.type == 'DOHRAO':
            return self.parse_do_while()
        elif token.type == 'HAR':
            return self.parse_for()
        elif token.type == 'HUKAM':
            return self.parse_function_declaration()
        elif token.type == 'WAAPSI':
            return self.parse_return()
        else:
            expr = self.parse_expression()
            if expr['type'] == 'Identifier' and self.current_token() and self.current_token().type == 'EQUALS':
                self.match('EQUALS')
                val = self.parse_expression()
                self.match('SEMI')
                return {"type": "Assignment", "left": expr['value'], "right": val}
            self.match('SEMI')
            return {"type": "ExpressionStatement", "expression": expr}

    def parse_declaration(self):
        var_type = None
        if self.current_token().type in ('ADAD', 'ASHARIYA', 'JUMLA', 'HAQEEQAT', 'FEHRIST'):
            var_type = self.current_token().value
            self.advance()
            
        self.match('DAULAT')
        id_token = self.match('IDENTIFIER')
        self.match('EQUALS')
        expr = self.parse_expression()
        self.match('SEMI')
        return {"type": "Declaration", "var_type": var_type or "daulat", "id": id_token.value, "value": expr}

    def parse_print(self):
        self.match('FARMAN')
        expr = self.parse_expression()
        self.match('SEMI')
        return {"type": "Print", "expression": expr}

    def parse_if(self):
        self.match('AGAR')
        self.match('LPAREN')
        condition = self.parse_expression()
        self.match('RPAREN')
        self.match('PHIR')
        body = self.parse_statement_list()
        self.match('KHATAM')
        self.match('SEMI')
        
        elif_blocks = []
        while self.current_token() and self.current_token().type == 'WARNA_AGAR':
            self.match('WARNA_AGAR')
            self.match('LPAREN')
            elif_cond = self.parse_expression()
            self.match('RPAREN')
            self.match('PHIR')
            elif_body = self.parse_statement_list()
            self.match('KHATAM')
            self.match('SEMI')
            elif_blocks.append({"condition": elif_cond, "body": elif_body})
            
        else_body = None
        if self.current_token() and self.current_token().type == 'VARNA':
            self.match('VARNA')
            else_body = self.parse_statement_list()
            self.match('KHATAM')
            self.match('SEMI')

        return {"type": "If", "condition": condition, "body": body, "elif_blocks": elif_blocks, "else_body": else_body}

    def parse_while(self):
        self.match('JAB_TAK')
        self.match('LPAREN')
        condition = self.parse_expression()
        self.match('RPAREN')
        self.match('PHIR')
        body = self.parse_statement_list()
        self.match('KHATAM')
        self.match('SEMI')
        return {"type": "While", "condition": condition, "body": body}

    def parse_do_while(self):
        self.match('DOHRAO')
        self.match('LBRACE')
        body = self.parse_statement_list()
        self.match('RBRACE')
        self.match('JAB_TAK')
        self.match('LPAREN')
        condition = self.parse_expression()
        self.match('RPAREN')
        self.match('SEMI')
        return {"type": "DoWhile", "body": body, "condition": condition}

    def parse_for(self):
        self.match('HAR')
        self.match('LPAREN')
        init = self.parse_declaration() 
        cond = self.parse_expression()
        self.match('SEMI')
        id_token = self.match('IDENTIFIER')
        self.match('EQUALS')
        update_expr = self.parse_expression()
        self.match('RPAREN')
        self.match('PHIR')
        body = self.parse_statement_list()
        self.match('KHATAM')
        self.match('SEMI')
        return {"type": "For", "init": init, "condition": cond, "update": {"type": "Assignment", "left": id_token.value, "right": update_expr}, "body": body}

    def parse_function_declaration(self):
        self.match('HUKAM')
        id_token = self.match('IDENTIFIER')
        self.match('LPAREN')
        params = []
        if self.current_token() and self.current_token().type == 'IDENTIFIER':
            params.append(self.match('IDENTIFIER').value)
            while self.current_token() and self.current_token().type == 'COMMA':
                self.match('COMMA')
                params.append(self.match('IDENTIFIER').value)
        self.match('RPAREN')
        self.match('LBRACE')
        body = self.parse_statement_list()
        self.match('RBRACE')
        return {"type": "FunctionDeclaration", "id": id_token.value, "params": params, "body": body}

    def parse_return(self):
        self.match('WAAPSI')
        expr = self.parse_expression()
        self.match('SEMI')
        return {"type": "Return", "expression": expr}

    def parse_expression(self):
        return self.parse_boolean_expression()

    def parse_boolean_expression(self):
        left = self.parse_arithmetic_expression()
        token = self.current_token()
        if token and token.type in ('GT', 'LT', 'EQEQ', 'NOTEQ'):
            op = token.value
            self.advance()
            right = self.parse_arithmetic_expression()
            return {"type": "BinaryExpression", "operator": op, "left": left, "right": right}
        return left

    def parse_arithmetic_expression(self):
        left = self.parse_term()
        while self.current_token() and self.current_token().type in ('PLUS', 'MINUS'):
            op = self.current_token().value
            self.advance()
            right = self.parse_term()
            left = {"type": "BinaryExpression", "operator": op, "left": left, "right": right}
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token() and self.current_token().type in ('STAR', 'SLASH'):
            op = self.current_token().value
            self.advance()
            right = self.parse_factor()
            left = {"type": "BinaryExpression", "operator": op, "left": left, "right": right}
        return left

    def parse_factor(self):
        token = self.current_token()
        if not token:
            raise RoyalProtocolViolation("Unexpected EOF in factor", "EOF", "EOF")
            
        if token.type == 'IDENTIFIER':
            self.advance()
            if self.current_token() and self.current_token().type == 'LPAREN':
                self.match('LPAREN')
                args = []
                if self.current_token() and self.current_token().type != 'RPAREN':
                    args.append(self.parse_expression())
                    while self.current_token() and self.current_token().type == 'COMMA':
                        self.match('COMMA')
                        args.append(self.parse_expression())
                self.match('RPAREN')
                return {"type": "FunctionCall", "id": token.value, "arguments": args}
            return {"type": "Identifier", "value": token.value}
        elif token.type == 'NUMBER':
            self.advance()
            return {"type": "NumberLiteral", "value": token.value}
        elif token.type == 'STRING':
            self.advance()
            return {"type": "StringLiteral", "value": token.value}
        elif token.type in ('SACH', 'GHALAT'):
            self.advance()
            return {"type": "BooleanLiteral", "value": token.value}
        elif token.type == 'LBRACKET':
            self.advance()
            elements = []
            if self.current_token() and self.current_token().type != 'RBRACKET':
                elements.append(self.parse_expression())
                while self.current_token() and self.current_token().type == 'COMMA':
                    self.match('COMMA')
                    elements.append(self.parse_expression())
            self.match('RBRACKET')
            return {"type": "ArrayLiteral", "elements": elements}
        elif token.type == 'DARKHWAST':
            self.advance()
            self.match('LPAREN')
            prompt = self.match('STRING')
            self.match('RPAREN')
            return {"type": "InputCall", "prompt": prompt.value}
        elif token.type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.match('RPAREN')
            return expr
        else:
            raise RoyalProtocolViolation(f"Unexpected token in factor: {token.value}", token.line, token.column)

def parse(tokens):
    return Parser(tokens).parse()
