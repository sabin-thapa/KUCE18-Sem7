data = []

node_dict = {}
# data stores: value , label, nullable, firstPos, lastpos
alphabet = []

DFA = {}

def firstPos():
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
            stack.append([0])
            d[3] = [0]
        elif d[0] == '*':
            val = stack.pop()
            stack.append(val)
            d[3] = val.copy()
        else:
            stack.append([d[1]])
            d[3] = [d[1]]

def postFix(str):
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
        if not(d[0] == '*' or d[0]=='.' or d[0]=='+' or d[0]=='|' or d[0]=='#'):
            if d[0] not in alphabet:
                alphabet.append(d[0]) 

def label():
    i = 1
    j = 1
    for d in data:
        if not(d[0] =='e' or d[0] =='|' or d[0] =='+' or d[0] =='.' or d[0] =='*'):
            d.append(i)
            i += 1
        else:
            d.append(100-j-i)
            j += 1

def nullable():
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

def lastpos():
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
            stack.append([0])
            d[4] = [0]
        elif d[0] == '*':
            val = stack.pop()
            stack.append(val)
            d[4] = val.copy()
        else:
            stack.append([d[1]])
            d[4] = [d[1]]

def mkdict():
    for d in data:
        d.append([])
        a = f'{d[1]}'
        node_dict.update({a:d})

def followPos():
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

def update():
    for d in data:
        d = node_dict[f'{d[1]}']


def dfa_Create():
    n = f'{data[-1][3]}'
    DFA[n] = {}
    for a in alphabet:
        DFA[n][a] = None
    DFA[n]['value'] = data[-1][3]
    if data[-2][1] in DFA[n]['value']:
        DFA[n]['valid'] = True
    else:
        DFA[n]['valid'] = False
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
                        DFA[f'{follow}']['valid'] = True
                    else:
                        DFA[f'{follow}']['valid'] = False


def validate(string):
    valid = False
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
        valid = DFA[n]['valid']
    except:
        return False
    return valid


if __name__=="__main__":
    re = input("Enter the Regular Expression:")
    re = '('+re+').#'
    postFix(re)
    alpha()
    label()
    nullable()
    firstPos()
    lastpos()
    mkdict()
    followPos()
    update()
    dfa_Create()

    while True:
        s = input("Input the string: ")

        if validate(s):
            print('The given input is Valid!')
        else:
            print('The given inpu is not valid!')
        


