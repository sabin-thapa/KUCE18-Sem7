from curses.ascii import isalpha, isdigit
from tabulate import tabulate

symbolTable= []

path = str(input("Input path of file: "))
datatypes = ["str","int","float","bool","dict","list"]
reserved  = ['print', 'if', 'elif', 'else','import', 'True','False','None',
        'as','from','try','except', 'for','return','and','break','class',
        'continue','def','global','lambda','pass','with', 'del','in',
        'range','while']
operators = ['+', "-" ,"*", "/", "%", "**", "=", "," , ">", "<",">=","<=","==","!="]
specialcharacters = ['"'," ' ", "#", '(', ")", "[", "]"]

operatorsMappings = {
    '+': "PLUS_OP",
    '-': "MINUS_OP",
    '*': "MULT_OP",
    '/': "DIV_OP",
    '%': "MOD_OP",
    '**': "POW_OP",
    '=': "EQ_OP",
    '>': "GREATER_THAN_OP",
    '<': "LESS_THAN_OP",
    '>=': "GREATER_THAN_OR_EQUAL_OP",
    '<=': "LESS_THAN_OR_EQUAL_OP",
    '==': "EQUALITY_OP",
    '!=': "NOT_Equality_OP"
}

specialCharMappings = {
    '"': "DOUBLE_QUOTE",
    "'": "SINGLE_QUOTE",
    '#': "HASH",
    '(': 'PARAM_OPEN',
    ')': 'PARAM_CLOSE',
    '[': 'BRACKET_OPEN',
    ']': 'BRACKET_CLOSE',
    ':': 'DELIMITER_COLON'
}

with open(str(path)) as f:
    content_list = f.readlines()

content_list = [x.strip() for x in content_list]
# print(content_list)

for i in content_list:
    if i.isalpha():
        if str(i) in reserved:
            
            t = ["RESERVED",i]
            symbolTable.append(t)
        elif str(i) in datatypes:
            t =["DATATYPE",i]
            symbolTable.append(t)
        else:
            t = ["IDENTIFIER",i]
            symbolTable.append(t)
            
    elif not i.isalpha() and i[0].isalpha():
        t = ["IDENTIFIER",i]
        symbolTable.append(t)
            
    elif i.isdigit():
        t = ["INTEGER",i]
        symbolTable.append(t)    
    
    else:
        if i in operators:
            temp= operatorsMappings[i]
            t = [temp,i]
            # t = ["Operator",i]
            symbolTable.append(t)
        
        elif i in specialcharacters:
            temp= specialCharMappings[i]
            t = [temp,i]
            symbolTable.append(t)
            
        elif not i.isalpha() and i[0]=="_":
            t = ["IDENTIFIER",i]
            symbolTable.append(t)
        elif not i.isdigit():
            try:
                a = i.split('.')
                if a[0].isdigit() and a[1].isdigit() and len(a)==2:
                    t = ["FLOAT",i]
                    symbolTable.append(t) 
                
            except:
                pass
            
        else:
            t = ["ERROR",i]
            symbolTable.append(t)
# print(tabulate(symbolTable))
print(tabulate(symbolTable,headers=['Type','Token'],tablefmt='fancy_grid'))