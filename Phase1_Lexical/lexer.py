import re
import os
import sys

# Add parent directory to sys.path so we can import 'errors'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from errors import RoyalProtocolViolation

# Token specifications
TOKEN_SPEC = [
    ('COMMENT',     r'//.*'),                 # Single-line comment
    ('BISMILLAH',   r'\bBismillah\b'),        # Start of program
    ('ALLAH_HAFIZ', r'\bAllahHafiz\b'),       # End of program
    ('DAULAT',      r'\bdaulat\b'),           # Variable declaration
    ('HUKAM',       r'\bhukam\b'),            # Function
    ('WAAPSI',      r'\bwaapsi\b'),           # Return
    ('JAB_TAK',     r'\bjab_tak\b'),          # While
    ('DOHRAO',      r'\bdohrao\b'),           # Do / Repeat
    ('HAR',         r'\bhar\b'),              # For
    ('WARNA_AGAR',  r'\bwarna_agar\b'),       # Else if
    ('AGAR',        r'\bagar\b'),             # If
    ('PHIR',        r'\bphir\b'),             # Then
    ('VARNA',       r'\bvarna\b'),            # Else
    ('FARMAN',      r'\bfarman\b'),           # Print
    ('DARKHWAST',   r'\bdarkhwast\b'),        # Input
    ('KHATAM',      r'\bkhatam\b'),           # End of block
    ('SACH',        r'\bsach\b'),             # True
    ('GHALAT',      r'\bghalat\b'),           # False
    ('ADAD',        r'\badad\b'),             # Int type
    ('ASHARIYA',    r'\bashariya\b'),         # Float type
    ('JUMLA',       r'\bjumla\b'),            # String type
    ('HAQEEQAT',    r'\bhaqeeqat\b'),         # Bool type
    ('FEHRIST',     r'\bfehrist\b'),          # Array type
    ('IDENTIFIER',  r'[A-Za-z_][A-Za-z0-9_]*'), # Identifiers
    ('NUMBER',      r'\d+(\.\d*)?'),          # Integer or decimal number
    ('STRING',      r'"[^"]*"'),              # String literal
    ('EQEQ',        r'=='),                   # Equal to
    ('NOTEQ',       r'!='),                   # Not equal to
    ('EQUALS',      r'='),                    # Assignment
    ('PLUS',        r'\+'),                   # Addition
    ('MINUS',       r'-'),                    # Subtraction
    ('STAR',        r'\*'),                   # Multiplication
    ('SLASH',       r'/'),                    # Division
    ('GT',          r'>'),                    # Greater than
    ('LT',          r'<'),                    # Less than
    ('SEMI',        r';'),                    # Statement terminator
    ('LPAREN',      r'\('),                   # Left Parenthesis
    ('RPAREN',      r'\)'),                   # Right Parenthesis
    ('LBRACE',      r'\{'),                   # Left Brace
    ('RBRACE',      r'\}'),                   # Right Brace
    ('LBRACKET',    r'\['),                   # Left Bracket
    ('RBRACKET',    r'\]'),                   # Right Bracket
    ('COMMA',       r','),                    # Comma
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
        elif type in ('WS', 'COMMENT'):
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lexer.py <input_file.shahi>")
        sys.exit(1)
        
    try:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
        tokens = tokenize(code)
        print("--- Lexical Analysis: Tokens ---")
        for t in tokens:
            print(f"{t.type}: {t.value}")
    except Exception as e:
        print(f"Lexical Error: {e}")
