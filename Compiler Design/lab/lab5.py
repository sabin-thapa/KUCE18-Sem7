# Lab 5 - Program to Remove Left Factoring from the given_grammar
# Sabin Thapa
# Roll no. 54

input_grammar = []
def take_grammar_input():
    input_grammar = []

    print('Note: \n 1. e represents epsilon. \n', 
            '2. Represent in the form: A=>aB \n',
            '3. Press enter after each production. \n')

    while(True):
        user_input = input(f'Production: ')
        if user_input == '':
            break
        input_grammar.append(user_input)

    for i,production in enumerate(input_grammar):
        input_grammar[i]=production.split('=>')
        input_grammar[i][1]=input_grammar[i][1].split('|')
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

def left_factoring():
    i=0
    while i<len(input_grammar):
        matched_strings = ''
        j = 0
        while j<len(input_grammar[i][1]):
            k=0
            while k<len(input_grammar[i][1]):
                if k!=j:
                    while True:
                        if len(input_grammar[i][1][k])>len(matched_strings):
                            if input_grammar[i][1][j][:len(matched_strings)+1] == input_grammar[i][1][k][:len(matched_strings)+1]:
                                matched_strings += input_grammar[i][1][j][len(matched_strings)]
                            else:
                                break
                        else:
                            break
                k+=1
            j+=1
        if len(matched_strings):
            factors = []
            j=0
            while j<len(input_grammar[i][1]):
                if len(matched_strings)<=len(input_grammar[i][1][j]):
                    if matched_strings == input_grammar[i][1][j]:
                        input_grammar[i][1].pop(j)
                        factors.append('e')
                    elif matched_strings == input_grammar[i][1][j][:len(matched_strings)]:
                        factors.append(input_grammar[i][1][j][len(matched_strings):])
                        input_grammar[i][1].pop(j)
                    else:
                        j+=1
                else:
                    j+=1
            if (i+1)<len(input_grammar):
                if input_grammar[i+1][0] == input_grammar[i][0]+"'":
                    input_grammar[i][1].insert(0,matched_strings+input_grammar[i][0]+"''")
                    input_grammar.insert(i+1,[input_grammar[i][0]+"''",factors]) 
                else:
                    input_grammar[i][1].insert(0,matched_strings+input_grammar[i][0]+"'")
                    input_grammar.insert(i+1,[input_grammar[i][0]+"'",factors]) 
            else:
                input_grammar[i][1].insert(0,matched_strings+input_grammar[i][0]+"'")
                input_grammar.append([input_grammar[i][0]+"'",factors])
        i+=1

def print_output(grammar):
    for production in grammar:
        output_statement = ''
        output_statement+=production[0]+'=>'
        for j in range(len(production[1])):
            if j:
                output_statement+='|'
            output_statement+=production[1][j]
        print(output_statement)
    print()

if __name__=='__main__':
    input_grammar = take_grammar_input()
    print('\nGiven Grammar ')
    print_output(input_grammar)
    left_factoring()
    left_factoring()
    print('Left Factor Removed Grammar')
    print_output(input_grammar)
