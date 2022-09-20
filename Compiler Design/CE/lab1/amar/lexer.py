'''
Name: Amar Kumar Mandal
Group: CE (4th Year/ 1st Sem)
Question number#1
'''

from amar.tokens import Token, operatorsMappings,\
    TokenTypes, specialCharMappings, reserved, relationsMappings


class Lexer:
    def __init__(self, filePath: str):
        self.line: int = 1
        self.peek: str = ' '
        self.code = open(filePath, 'r')

    def scan(self):

        # Check if digit or not
        if self.peek.isdigit():
            v = 0
            while True:
                v = 10*v + int(self.peek)
                self.peek = self.code.read(1)
                if not self.peek.isdigit():
                    break
            return Token(TokenTypes.INT, v)

        if self.peek in specialCharMappings.keys():
            # Check if string or not
            if self.peek == '"' or self.peek == "'":
                quotation = self.peek
                buffer = []
                # Loop until matching quotation not found
                while True:
                    buffer.append(self.peek)
                    self.peek = self.code.read(1)
                    if self.peek == quotation:
                        break
                w = ''.join(buffer)
                return Token(TokenTypes.STR, w)

            # check for the special character
            return Token(specialCharMappings[self.peek])

        # if given input is alphabet or not
        if self.peek.isalpha():
            buffer = []
            while True:
                buffer.append(self.peek)
                self.peek = self.code.read(1)
                if not self.peek.isalnum():
                    break
            w = ''.join(buffer)

            if w in reserved:
                return Token(TokenTypes.RESERVED, w)

            return Token(TokenTypes.IDENT, w)

        # check if input is relational operator or not
        # if yes make the symbol table entry
        if self.peek in relationsMappings.keys():
            return Token(TokenTypes.RELATION, relationsMappings[self.peek])

        # Operator
        t = Token(TokenTypes.OPERATOR, operatorsMappings[self.peek])
        self.peek = ' '
        return t

    def make_tokens(self):
        tokens = []
        while True:
            self.peek = self.code.read(1)

            if (self.peek == ' ' or self.peek == '\t'):
                continue

            if (self.peek == '\n' or self.peek == ';'):
                self.line += 1
                continue

            if self.peek:
                tokens.append(self.scan())
            else:
                break

        for t in tokens:
            print(t)


# read the input file
Lexer('./input.txt').make_tokens()
