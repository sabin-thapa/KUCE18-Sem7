'''graphviz can be installed using the command: pip install graphviz'''
import graphviz # for drawing the graph

DFA = {}
node_dict = {}
alphabet = []
data = []

def evaluate_postfix(str):
    stack = []
    for i in str:
        if i == ' ':
            continue
        elif i=='+' or i=='|':
            if stack:
                if stack[len(stack)-1] == '(':
                    stack.append(i)
                else:
                    data.append([stack.pop()])
                    stack.append(i)
            else:
                stack.append(i)
        elif i=='.':
            if stack:
                if stack[len(stack)-1] == '(' or stack[len(stack)-1] == '+' or stack[len(stack)-1] == '|':
                    stack.append(i)
                else:
                    data.append([stack.pop()])
                    stack.append(i)
            else:
                stack.append(i)
        elif i=='(':
            stack.append(i)
        elif i==')':
            j= stack.pop()
            while j != '(':
                data.append([j])
                j = stack.pop()
        else:
            data.append([i])
    while stack:
        data.append([stack.pop()])

def alpha():
    for d in data:
        if not(d[0] == '*' or d[0]=='.' or d[0]=='+' or d[0]=='|' or d[0]=='#' or d[0]=='e'):
            if d[0] not in alphabet:
                alphabet.append(d[0]) 

def label():
    i = 1
    j = 1
    for d in data:
        #e = epsilon
        if not(d[0] =='e' or d[0] =='|' or d[0] =='+' or d[0] =='.' or d[0] =='*'):
            d.append(i)
            i += 1
        else:
            d.append(100-j-i)
            j += 1

def evaluate_nullable():
    stack = []
    for d in data:
        if d[0] == '+' or d[0] == '|':
            val2 = stack.pop()
            val1 = stack.pop()
            val = val1 or val2
            stack.append(val)
            d.append(val)
            d.append(val1)
            d.append(val2)
        elif d[0] == '.':
            val2 = stack.pop()
            val1 = stack.pop()
            val = val1 and val2
            stack.append(val)
            d.append(val)
            d.append(val1)
            d.append(val2)
        elif d[0] == 'e':
            stack.append(True)
            d.append(True)
            d.append(False)
            d.append(False)
        elif d[0] == '*':
            stack.pop()
            stack.append(True)
            d.append(True)
            d.append(False)
            d.append(False)
        else:
            stack.append(False)
            d.append(False)
            d.append(False)
            d.append(False)

def evaluate_firstpos():
    stack = []
    for d in data:
        if d[0] == '+' or d[0] == '|':
            val2 = stack.pop()
            val1 = stack.pop()
            for e in val2:
                if e not in val1:
                    val1.append(e)
            stack.append(val1)
            d[3] = val1.copy()
        elif d[0] == '.':
            val2 = stack.pop()
            val1 = stack.pop()
            if d[3]:
                for e in val2:
                    if e not in val1:
                        val1.append(e)
            stack.append(val1)
            d[3] = val1.copy()
        elif d[0] == 'e':
            stack.append([])
            d[3] = []
        elif d[0] == '*':
            val = stack.pop()
            stack.append(val)
            d[3] = val.copy()
        else:
            stack.append([d[1]])
            d[3] = [d[1]]

def evaluate_lastpos():
    stack = []
    for d in data:
        if d[0] == '+' or d[0] == '|':
            val2 = stack.pop()
            val1 = stack.pop()
            for e in val2:
                if e not in val1:
                    val1.append(e)
            stack.append(val1)
            d[4] = val1.copy()
        elif d[0] == '.':
            val2 = stack.pop()
            val1 = stack.pop()
            if d[4]:
                for e in val1:
                    if e not in val2:
                        val2.append(e)
            stack.append(val2)
            d[4] = val2.copy()
        elif d[0] == 'e':
            stack.append([])
            d[4] = []
        elif d[0] == '*':
            val = stack.pop()
            stack.append(val)
            d[4] = val.copy()
        else:
            stack.append([d[1]])
            d[4] = [d[1]]

def make_dict():
    for d in data:
        d.append([])
        a = f'{d[1]}'
        node_dict.update({a:d})

def evaluate_followpos():
    stack = []
    for d in data:
        if d[0] == '+' or d[0] == '|':
            stack.pop()
            stack.pop()
            stack.append(d[1])
        elif d[0] == '.':
            val2 = stack.pop()
            val1 = stack.pop()
            for i in node_dict[f'{val1}'][4]:
                follow = node_dict[f'{i}'][5]
                first = node_dict[f'{val2}'][3]
                for k in first:
                    if k not in follow:
                        follow.append(k)
                node_dict[f'{i}'][5] = follow.copy()
            stack.append(d[1])
        elif d[0] == 'e':
            stack.append(d[1])
        elif d[0] == '*':
            val = stack.pop()
            for i in d[4]:
                follow = node_dict[f'{i}'][5]
                first = d[3]
                for k in first:
                    if k not in follow:
                        follow.append(k)
                node_dict[f'{i}'][5] = follow.copy()
            stack.append(d[1])
        else:
            stack.append(d[1])

def update_data():
    for d in data:
        d = node_dict[f'{d[1]}']

def create_DFA():
    n = f'{data[-1][3]}'
    DFA[n] = {}
    for a in alphabet:
        DFA[n][a] = None
    DFA[n]['value'] = data[-1][3]
    if data[-2][1] in DFA[n]['value']:
        DFA[n]['VALID'] = True
    else:
        DFA[n]['VALID'] = False
    nodes = [n]
    while nodes:
        node = nodes.pop()
        for a in alphabet:
            follow = []
            for d in DFA[node]['value']:
                if node_dict[f'{d}'][0] == a:
                    for i in node_dict[f'{d}'][5]:
                        if i not in follow:
                            follow.append(i)
            follow = sorted(follow)
            if follow:
                DFA[node][a] = f'{follow}'
                try:
                    a = DFA[f'{follow}']
                except:
                    nodes.append(f'{follow}')
                    DFA[f'{follow}'] = {}
                    for a in alphabet:
                        DFA[f'{follow}'][a] = None
                    DFA[f'{follow}']['value'] = follow
                    if data[-2][1] in DFA[f'{follow}']['value']:
                        DFA[f'{follow}']['VALID'] = True
                    else:
                        DFA[f'{follow}']['VALID'] = False

def validate_string(string):
    VALID = False
    n = next(iter(DFA))
    if string:
        for s in string:
            if s not in alphabet:
                return False
            try:
                n = DFA[n][s]
            except:
                return False
    try:
        VALID = DFA[n]['VALID']
    except:
        return False
    return VALID

def graph_printer(regular_expression):
    graph = graphviz.Digraph(f'DFA:{regular_expression}')
    graph.attr(layout='dot')
    keys = DFA.keys()
    current = 'START'
    graph.node(current, shape = 'circle', style='filled', color='white')
    graph.node(str(0), shape = 'circle', style='filled',color='yellow')
    graph.edge(current,str(0))
    for i,k in enumerate(keys):
        current = str(i)
        for a in alphabet:
            try:
                edge = DFA[k][a]
                VALID = DFA[edge]['VALID']
                for i,key in enumerate(keys):
                    if edge == key:
                        graph.node(str(i), shape = 'doublecircle' if VALID else 'circle', style='filled', color='green' if VALID else 'yellow')
                        graph.edge(current, str(i),label=a)
            except:
                graph.node('REJECT', shape='circle', style='filled',color='red')
                graph.edge(current,'REJECT', label = a)
    graph.format = 'png'
    graph.render(directory='graph/').replace('\\', '/')



def printer():
    for val in data:
        print(val)

if __name__=="__main__":
    regular_expression = input("Enter the Regular Expression: \n <INPUT FORM: (x+y)*.x+y.(y.y+x).x >\n<NOTE: 'e' is reserved for epsilon>\n")
    #Augmenting the given grammar
    regular_expression = '('+regular_expression+').#'
    evaluate_postfix(regular_expression)
    alpha()
    label()
    evaluate_nullable()
    evaluate_firstpos()
    evaluate_lastpos()
    make_dict()
    evaluate_followpos()
    update_data()
    create_DFA()
    print(DFA,'\n')
    printer()
    graph_printer(regular_expression)

    while True:
        inp = input("Input the string: ")
        if validate_string(inp):
            print('Input is VALID!')
        else:
            print('Input is INVALID!')

        if input("Test another string? <y/n>") == 'n':
            break
