# Lab 3 - Program to Remove Left Recursion from the given_grammar
# Sabin Thapa
# Roll no. 54
# CE 4th Year

given_grammar = []

def print_output(grammar):
    for i in grammar:
        statement = ''
        statement+=i[0]+'=>'
        for j in range(len(i[1])):
            if j:
                statement+='|'
            statement+=i[1][j]
        print(statement)
    print()

def take_grammar_input():
    given_grammar = []
    print('Note: \n 1. e represents epsilon. \n', 
            '2. Represent in the form: A=>aB|cD|Aa \n',
            '3. Press enter after each production. \n')
    
    while(True):
        inp = input(f'Enter the Grammar: ')
        # Stop after user inputs nothing
        if inp == '':
            break
        given_grammar.append(inp)

    for i,grammar in enumerate(given_grammar):
        given_grammar[i]=grammar.split('=>')
        given_grammar[i][1]=given_grammar[i][1].split('|')
    i=0
    while i<len(given_grammar):
        j=0
        while j<len(given_grammar):
            if i!=j:
                if given_grammar[i][0] == given_grammar[j][0]:
                    given_grammar[i][1].extend(given_grammar[j][1])
                    given_grammar.pop(j)
            j+=1
        i+=1
    return given_grammar

def remove_left_recursion():
    i=0
    while i<len(given_grammar):
        r = []
        j = 0
        while j<len(given_grammar[i][1]):
            if len(given_grammar[i][0]) <= len(given_grammar[i][1][j]):
                if given_grammar[i][0] == given_grammar[i][1][j][:len(given_grammar[i][0])]:
                    if given_grammar[i][0] == given_grammar[i][1][j]:
                        given_grammar[i][1].pop(j)
                        j-=1
                    else:
                        r.append(given_grammar[i][1][j][len(given_grammar[i][0]):])
                        given_grammar[i][1].pop(j)
                        j-=1
            j+=1
        if r:
            for j in range(len(given_grammar[i][1])):
                given_grammar[i][1][j]+=given_grammar[i][0]+"'"
            if not given_grammar[i][1]:
                given_grammar[i][1].append(given_grammar[i][0]+"'")
            for j in range(len(r)):
                r[j]+=given_grammar[i][0]+"'"
            r.append('e')
            if (i+1)<len(given_grammar):
                given_grammar.insert(i+1,[given_grammar[i][0]+"'",r]) 
            else:
                given_grammar.append([given_grammar[i][0]+"'",r])
        i+=1

if __name__=='__main__':
    given_grammar = take_grammar_input()
    print('\nGiven Grammar:')
    
    print_output(given_grammar)

    
    remove_left_recursion()
    
    print('After removing Left Recursion:')
    print_output(given_grammar)


# S=>A 
# A=>aB|aC|Ad|Ae 
# B=>bBc|f 
# C=>g 