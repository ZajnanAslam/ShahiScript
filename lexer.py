import re
from errors import RoyalProtocolViolation

# Token specifications
TOKEN_SPEC = [
    ('BISMILLAH',   r'\bBismillah\b'),        # Start of program
    ('ALLAH_HAFIZ', r'\bAllahHafiz\b'),       # End of program
    ('DAULAT',      r'\bdaulat\b'),           # Variable declaration
    ('AGAR',        r'\bagar\b'),             # If
    ('PHIR',        r'\bphir\b'),             # Then
    ('VARNA',       r'\bvarna\b'),            # Else
    ('FARMAN',      r'\bfarman\b'),           # Print
    ('KHATAM',      r'\bkhatam\b'),           # End of block
    ('IDENTIFIER',  r'[A-Za-z_][A-Za-z0-9_]*'), # Identifiers
    ('NUMBER',      r'\d+(\.\d*)?'),          # Integer or decimal number
    ('STRING',      r'"[^"]*"'),              # String literal
    ('EQUALS',      r'='),                    # Assignment
    ('GT',          r'>'),                    # Greater than
    ('LT',          r'<'),                    # Less than
    ('SEMI',        r';'),                    # Statement terminator
    ('LPAREN',      r'\('),                   # Left Parenthesis
    ('RPAREN',      r'\)'),                   # Right Parenthesis
    ('LBRACE',      r'\{'),                   # Left Brace
    ('RBRACE',      r'\}'),                   # Right Brace
    ('WS',          r'[ \t]+'),               # Whitespace
    ('NEWLINE',     r'\n'),                   # Line endings
    ('MISMATCH',    r'.'),                    # Any other character
]

TOKEN_REGEX = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPEC)
get_token = re.compile(TOKEN_REGEX).match

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, Line: {self.line}, Col: {self.column})"

def tokenize(code):
    line_num = 1
    line_start = 0
    pos = 0
    tokens = []
    
    match = get_token(code, pos)
    while match is not None:
        type = match.lastgroup
        value = match.group(type)
        column = match.start() - line_start + 1
        
        if type == 'NEWLINE':
            line_start = match.end()
            line_num += 1
        elif type == 'WS':
            pass
        elif type == 'MISMATCH':
            raise RoyalProtocolViolation(f"Unexpected character {value!r}", line_num, column)
        else:
            # Check if an identifier is actually a keyword (handled nicely here because keywords are listed first in TOKEN_SPEC)
            # Actually, regex matching goes by group ordering or longest match depending on re module.
            # Python's re matches the first group that matches. Since keywords are first, they take precedence over IDENTIFIER!
            tokens.append(Token(type, value, line_num, column))
            
        pos = match.end()
        match = get_token(code, pos)
        
    return tokens
