# Lab 4 - Program to compute FIRST and FOLLOW from the given_grammar
# Sabin Thapa
# Roll no. 54
# CE 4th Year

from prettytable import PrettyTable as table
input_grammar = []

def evaluate_first(symbol):
    if symbol[0]==symbol[0].lower():
        return symbol[0]
    else:
        FIRST = ''
        for i in range(len(symbol)):
            for production in input_grammar:
                if production[0]==symbol[i]:
                    for x in production[1]:
                        if x[0]==symbol[0]:
                            FIRST+=evaluate_first(x[1:])
                        else:
                            FIRST+=evaluate_first(x)
            if 'e' in FIRST:
                continue
            else:
                break
        if FIRST[-1] != 'e':
            FIRST = FIRST.replace('e','')
        return FIRST

def evaluate_follow(symbol):
    # evaluate_follow of augmented input_grammar
    if symbol[0] == 'X':
        return '$'
    else:
        FOLLOW = ''
        for production in input_grammar:
            for prod in production[1]:
                if symbol[0] in prod:
                    if symbol[0] == prod[-1]:
                        FOLLOW += evaluate_follow(production[0]) if production[0] != symbol[0] else ''
                    else:
                        FOLLOW += evaluate_first(prod[prod.index(symbol[0])+1:])
                    if 'e' in FOLLOW:
                        FOLLOW.replace('e','')
                        if symbol[0] != production[0]:
                            FOLLOW += evaluate_follow(production[0])
        return FOLLOW

def tabulate_results():
    output_table = []
    for production in input_grammar:
        output_table.append([production[0],evaluate_first(production[0]),evaluate_follow(production[0])]) 
    
    for i in range(len(output_table)):
        output_table[i][1] = "".join(dict.fromkeys(output_table[i][1]))
        output_table[i][2] = output_table[i][2].replace('e','')
        output_table[i][2] = "".join(dict.fromkeys(output_table[i][2]))
    return output_table

def display_table(tbl):
    output_table = table(['----','FIRST','FOLLOW'])
    output_table.title = 'FIRST and FOLLOW table'
    for i in range(len(tbl)):
        row=[]
        row.append(tbl[i][0] if not tbl[i][0]=='X' else tbl[i+1][0]+"'")
        for j in tbl[i][1:]:
            temp = '{'
            for k in j[:-1]:
                temp +=k+','
            temp+=j[-1]+'}'
            row.append(temp)
        output_table.add_row(row)
    print(output_table)

def take_grammar_input():
    input_grammar = []

    print('Note: \n 1. e represents epsilon. \n', 
            '2. Represent in the form: A=>aB \n',
            '3. Press enter after each production. \n')

    while(True):
        inp = input(f'Production: ')
        if inp == '':
            break
        input_grammar.append(inp)

    for i,g in enumerate(input_grammar):
        input_grammar[i]=g.split('=>')
        input_grammar[i][1]=input_grammar[i][1].split('|')
    input_grammar.insert(0,['X',[input_grammar[0][0]+'$']])
    i=0
    while i<len(input_grammar):
        j=0
        while j<len(input_grammar):
            if i!=j:
                if input_grammar[i][0] == input_grammar[j][0]:
                    input_grammar[i][1].extend(input_grammar[j][1])
                    input_grammar.pop(j)
            j+=1
        i+=1
    return input_grammar
if __name__=='__main__':
    input_grammar = take_grammar_input()
    output_table = tabulate_results()
    display_table(output_table)


# S=>A 
# A=>aB|aC
# B=>bBc|f 
# C=>g 