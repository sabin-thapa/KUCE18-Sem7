from curses.ascii import isalpha, isdigit
from tabulate import tabulate


line_number = 0
current = ' '
file_path = ' '

reserved_words = set((
        'import',
        'global',
        'print',
        'while',
        'for',
        'if',
        'elif',
        'else',
        'True',
        'False',
        'None',
        'as',
        'from',
        'try',
        'except',
        'and',
        'break',
        'class',
        'continue',
        'def',
        'lambda',
        'pass',
        'with',
        'del',
        'in',
        'range',
        'return',
    ))

operators_mappings = {
    '/': "DIV_OP",
    '*': "MULT_OP",
    '+': "PLUS_OP",
    '-': "MINUS_OP",
    '%': "MOD_OP",
    '**': "POW_OP",
    '^':'POW_OP',
    '=': "ASSIGN_OP",
    ',': "COMMA_OP"
}

special_characters = [ 
    '"',
    "'",
    '#',
    '(',
    ')',
    '[',
    ']',
    ':',]

special_char_mappings = {
    '#': "HASH",
    "'": "SINGLE_QUOTE",
    '"': "DOUBLE_QUOTE",
    '(': 'PARAM_OPEN',
    ')': 'PARAM_CLOSE',
    '[': 'BRACKET_OPEN',
    ']': 'BRACKET_CLOSE',
    ':': 'DELIMITER_COLON'
}

data_type = {
    'int': 'INTEGER',
    'float': 'FLOATING_POINT',
    'bool': 'BOOLEAN',
    'str': 'STRING',
    'dict': 'DICTIONARY',
    'list': 'LIST',
}

def scan_input(input):
    global current
    if current.isdigit():
        val = 0
        while True:
            val = 10*val + int(current)
            current = input.read(1)
            if not current.isdigit():
                if current == '.':
                    i = 1
                    while True:
                        current = input.read(1)
                        if not current.isdigit():
                            break
                        val = val+float(int(current))/10**i
                        i += 1
                break
        return data_type[str(type(val))[8:-2]],val

    if current in special_characters:
        if current == '"' or current == "'":
            quotation = current
            buffer = []
            while True:
                buffer.append(current)
                current = input.read(1)
                if current == quotation: 
                    current = input.read(1)
                    break
            w = ''.join(buffer)
            return data_type['str'],w
        temp = current
        current = input.read(1)
        return special_char_mappings[temp],temp

    
    if current.isalpha():
        buffer = []
        while True:
            buffer.append(current)
            current = input.read(1)
            if not current.isalnum(): break
        word = ''.join(buffer)

        if word in reserved_words:
            return 'reserved_words',word
        return 'IDENTIFIER',word
    
    t = (operators_mappings[current],current)
    current = ' '
    return t

def generate_tokens(input):
    global current,line_number
    tokens = []
    current = input.read(1)
    while True:
        if (current == ' ' or current == '\t'): 
            current = input.read(1)
            continue
        if (current == '\n' or current == ';'): 
            current = input.read(1)
            line_number += 1
            continue
        if current:
            tokens.append(scan_input(input))
        else: 
            break
    print('Symbol Table:')

    print(tabulate(tokens,headers=['Type','Token'],tablefmt='fancy_grid'))


if __name__=='__main__':
    file_path = input("Enter the path of the file (eg: input.txt): ")
    inputs = open(repr(file_path)[1:-1],'r')
    generate_tokens(inputs)
    inputs.close()