class RoyalProtocolViolation(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"Royal Protocol Violation at line {line}, col {column}: {message}")
        self.line = line
        self.column = column
