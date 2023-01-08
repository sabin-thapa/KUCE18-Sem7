from copy import deepcopy
from prettytable import PrettyTable as table
from prettytable import ALL
import graphviz
from PyQt5.QtWidgets import *
from PIL import Image
from textwrap import fill
import sys

class ParseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Parsing the Input')
        self.setGeometry(810,50,640,700)
        self.initParseUI()

    def initParseUI(self):
        self.parse_win_layout = QGridLayout()
        self.table_row = QHBoxLayout()
        self.parse_process_table = QTableWidget()
        self.table_row.addWidget(self.parse_process_table)

        self.parse_win_layout.addLayout(self.table_row,0,0)
        self.setLayout(self.parse_win_layout)

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setWindowTitle('LR(1) Parser')
        self.setGeometry(100,50,700,700)
        self.initUI()
    
    def initUI(self):
        self.layout = QGridLayout()
        
        #ROW1
        self.row1 = QHBoxLayout()
        self.label = QLabel('Grammar:')
        self.G = QTextEdit()
        self.G.setMaximumHeight(100)
        self.button = QPushButton('Done!')
        self.button.clicked.connect(lambda: self.takeGrammar(self.G.toPlainText()))
        self.row1.addWidget(self.label)
        self.row1.addWidget(self.G)
        self.row1.addWidget(self.button)

        #ROW2
        self.row2 = QHBoxLayout()
        self.ActionGoto = QTableWidget()
        self.row2.addWidget(self.ActionGoto)

        #ROW3
        self.row3 = QHBoxLayout()
        self.Input = QTextEdit()
        self.Input.setMaximumHeight(40)
        self.check = QPushButton('Check')
        self.check.clicked.connect(lambda: self.CheckOnly(self.Input.toPlainText()))
        self.row3.addWidget(self.Input)
        self.row3.addWidget(self.check)

        #ROW4
        self.row4 = QHBoxLayout()

        self.i = QLabel('Valid? : Yet To Check!')
        self.i.setMaximumHeight(20)
        self.row4.addWidget(self.i)
        self.show_parse = QPushButton('Show Parsing Process')
        self.show_parse.clicked.connect(lambda: self.CheckInput(self.Input.toPlainText()))
        self.row4.addWidget(self.show_parse)

        self.layout.addLayout(self.row1,0,0)
        self.layout.addLayout(self.row2,1,0,3,0)
        self.layout.addLayout(self.row3,5,0)
        self.layout.addLayout(self.row4,6,0)

        self.setLayout(self.layout)

    def takeGrammar(self,G):
        G = G.split('\n')
        try:
            G.remove('')
        except:
            pass
        for i,g in enumerate(G):
            g=g.replace(' ','')
            G[i]=g.split('=>') if '=>' in g else g.split('->')
            G[i][1]=G[i][1].split('|')
        G.insert(0,['X',[G[0][0]+'$']])
        global grammar
        grammar = G

        StateTable = States()
        statePTABLE = table(['STATE','CLOSURE'])
        for i,state in enumerate(StateTable):
            statePTABLE.add_row([i, fill(stringifyState(state),width = 10)] )
        statePTABLE.hrules = ALL
        print(statePTABLE)
        CreateTable(StateTable)

        #Add to QT table:
        self.ActionGoto.setColumnCount(len(ActionGotoTable[0]))
        for i in range(len(ActionGotoTable[0])):    
            self.ActionGoto.setColumnWidth(i,80)
        self.ActionGoto.setRowCount(len(ActionGotoTable)-1)
        for i in range(len(ActionGotoTable)-1):    
            self.ActionGoto.setRowHeight(i,35)
        self.ActionGoto.setHorizontalHeaderLabels(ActionGotoTable[0])
        self.ActionGoto.setVerticalHeaderLabels([str(i) for i in range(len(ActionGotoTable)-1)])
        for i in range(len(ActionGotoTable[1:])):
            self.ActionGoto.setItem(i,0,QTableWidgetItem(str(i)))
        for i,x in enumerate(ActionGotoTable[1:]):
            for j,e in enumerate(x[1:]):
                self.ActionGoto.setItem(i,j+1,QTableWidgetItem(str(e)))
        
        VisualizeStates()     # COMMENT OUT REDUCTIONS FROM ACTION DICTIONARY
        GRAPH = Image.open('COMP409/Lab/graphviz/CLR-State-Diagram.gv.png')
        GRAPH.show()

    def FillTable(self):
        global ParseTable
        self.w.parse_process_table.setColumnCount(len(ParseTable[0]))
        for i in range(len(ParseTable[0])):
            self.w.parse_process_table.setColumnWidth(i,200)
        self.w.parse_process_table.setRowCount(len(ParseTable)-1)
        for i in range(len(ParseTable)-1):
            self.w.parse_process_table.setRowHeight(i,35)
        self.w.parse_process_table.setHorizontalHeaderLabels(ParseTable[0])
        self.w.parse_process_table.setVerticalHeaderLabels([str(i) for i in range(len(ParseTable)-1)])
        for i,x in enumerate(ParseTable[1:]):
            for j,e in enumerate(x):
                result = ''.join(str(item).strip("'") for item in e)
                self.w.parse_process_table.setItem(i,j,QTableWidgetItem(str(result)))
    
    def CheckOnly(self, inp):
        parseTree = graphviz.Digraph(f'CLR-Parse-Tree')
        parseTree.attr(layout='dot')
        created_nodes = []
        reduced_nodes = []
        inp +='$'
        inp = list(inp)

        stack = []
        stack.append(0)
        while(True):
            try:
                action = Action[stack[0]][inp[0]]
            except:
                break
            try:
                action = action.split('->')
                reduction = ''
                if action[1] != 'X':
                    if action[1] in created_nodes:
                        act = action[1]
                        while act in created_nodes:
                            act += ' '
                        parseTree.node(act, shape = 'circle', style='filled',color='lightblue',ordering='in')
                        created_nodes.insert(0,act)
                        reduction = act
                    else:
                        parseTree.node(action[1], shape = 'circle', style='filled',color='lightblue',ordering='in')
                        created_nodes.insert(0,action[1])
                        reduction = action[1]

                for char in action[0]:
                    for cn in created_nodes:
                        if char in cn:
                            if cn not in reduced_nodes:
                                if action[1]=='X':
                                    parseTree.node('acc', shape = 'circle', style='filled',color='lightgreen',ordering='in')
                                    parseTree.edge(cn,'acc')
                                    reduced_nodes.append(cn)
                                else:
                                    for cnn in created_nodes:
                                        if reduction in cnn:
                                            if cnn not in reduced_nodes:
                                                parseTree.edge(cn,cnn)
                                                reduced_nodes.append(cn)
                                break

                if action[1] == 'X':
                    self.i.setText('Valid? : Valid Input!')
                    parseTree.format = 'png'
                    parseTree.render(directory='COMP409/Lab/graphviz').replace('\\', '/')

                    ParseTree = Image.open('COMP409/Lab/graphviz/CLR-Parse-Tree.gv.png')
                    ParseTree.show()

                    return 'Accept'
                for i in range(2*len(action[0])):
                    stack.pop(0)
                try:
                    gt = GoTo[stack[0]][action[1]]
                except:
                    break
                stack.insert(0,action[1])
                stack.insert(0,gt)
            except:
                action = inp.pop(0)
                if action in created_nodes:
                    act = action
                    while act in created_nodes:
                        act += ' '
                    parseTree.node(act, shape = 'circle', style='filled',color='lightblue',ordering='in')
                    created_nodes.append(act)
                else:
                    parseTree.node(action, shape = 'circle', style='filled',color='lightblue',ordering='in')
                    created_nodes.append(action)
                try:
                    gt = Action[stack[0]][action]

                except:
                    break
                stack.insert(0,action)
                stack.insert(0,gt)
        self.i.setText('Valid? : Invalid Input!')
        parseTree.node('error', shape = 'circle', style='filled',color='pink')
        for i in inp[:-1]:
            if i in created_nodes:
                act = i
                while act in created_nodes:
                    act += ' '
                parseTree.node(act, shape = 'circle', style='filled',color='lightblue',ordering='in')
                created_nodes.append(act)
            else:
                parseTree.node(i, shape = 'circle', style='filled',color='lightblue',ordering='in')
                created_nodes.append(i)
        for cn in created_nodes:
            if cn not in reduced_nodes:
                parseTree.edge(cn,'error')
        parseTree.format = 'png'
        parseTree.render(directory='COMP409/Lab/graphviz').replace('\\', '/')

        ParseTree = Image.open('COMP409/Lab/graphviz/CLR--Tree.gv.png')
        ParseTree.show()

        return 'Error'

    def CheckInput(self,inp):
        global ParseTable
        ParseTable=[]
        self.w = ParseWindow()
        self.w.show()

        ParseTable.append(['STACK','INPUT','ACTION'])
        inp +='$'
        inp = inp.replace(' ','')
        inp = list(inp)

        stack = []
        stack.append(0)
        while(True):
            row = ['']*3    
            row[0] = deepcopy(stack)    
            row[0].reverse()
            row[1] = deepcopy(inp)
            try:
                action = Action[stack[0]][inp[0]]
            except:
                break
            try:
                action = action.split('->')
                row[2] = 'reduce '+str(action)
                if action[1] == 'X':
                    self.i.setText('Valid? : Valid Input!')
                    row[0] = deepcopy(stack)
                    row[0].reverse()
                    row[1] = deepcopy(inp)
                    row[2] = 'Accept'
                    ParseTable.append(deepcopy(row))
                    self.FillTable()
                    return 'Accept'

                for i in range(2*len(action[0])):
                    stack.pop(0)
                try:
                    gt = GoTo[stack[0]][action[1]]
                    row[2] += f",  Goto({stack[0]},{action[1]}) => "+str(gt)
                    ParseTable.append(deepcopy(row))
                except:
                    break
                stack.insert(0,action[1])
                stack.insert(0,gt)

            except:
                row[2] = 'shift '+str(action)
                row[1] = deepcopy(inp)
                action = inp.pop(0)
                try:
                    row[0] = deepcopy(stack)
                    row[0].reverse()
                    
                    gt = Action[stack[0]][action]
                    ParseTable.append(deepcopy(row))
                except:
                    break
                stack.insert(0,action)
                stack.insert(0,gt)

        row[2] = 'Error'
        ParseTable.append(row)
        self.i.setText('Valid? : Invalid Input!')

        self.FillTable()
        return 'Error'

grammar = []
StateTable = []
GoTo = {}
Action = {}
GraphAction = {}
Reduction = []

ActionGotoTable = []
ParseTable = []


def First(var):
    if var[0]==var[0].lower():
        return var[0]
    else:
        f = ''
        for i in range(len(var)):
            for g in grammar:
                if g[0]==var[i]:
                    for x in g[1]:
                        f+=First(x)
            if 'e' in f:
                continue
            else:
                break
        if f[-1] != 'e':
            f = f.replace('e','')
        return f

def Follow(var):
    if var[0] == 'X':
        return '$'
    else:
        f = ''
        for gram in grammar:
            for g in gram[1]:
                if var[0] in g:
                    if var[0] == g[-1]:
                        f += Follow(gram[0]) if gram[0] != var[0] else ''
                    else:
                        f += First(g[g.index(var[0])+1:])
                    if 'e' in f:
                        f.replace('e','')
                        f += Follow(gram[0])
        return f

def FFTable():
    table = []
    for g in grammar:
        table.append([g[0],First(g[0]),Follow(g[0])])        # {g[0] : First(g[0])}
    for i in range(len(table)):
        table[i][2] = table[i][2].replace('e','')
        table[i][2] = "".join(dict.fromkeys(table[i][2]))
    return table

def showStates(t):
    for i,x in enumerate(t):
        print('\nState',str(i)+':')
        s = '{\n'
        for st in x:
            s += st[0]+'=>'+st[1][0]+','+st[1][1]+'\n'
        s += '}'
        print(s)

def stringifyState(t):
    s=''
    for st in t:
        s += st[0]+'=>'+st[1][0]+','+st[1][1]+' '
    return s

def alphabet():
    alphabet = ''
    for gram in grammar:
        for g in gram[1]:
            for a in g:
                if a == a.lower():
                    alphabet += a
    alphabet = alphabet.replace('e','')
    alphabet = ''.join(dict.fromkeys(alphabet))
    return alphabet

def Variables():
    var = ''
    for gram in grammar:
        for g in gram[0]:
            var += g
    var = var.replace('X','')
    var = ''.join(dict.fromkeys(var))
    return var

def CreateTable(states):
    global ActionGotoTable
    ActionGotoTable = []
    ActionGotoTable.append(['States'])
    for i in range(len(states)):
        ActionGotoTable.append([i])
    for a in alphabet().replace('$',''):
        ActionGotoTable[0].append(a)
    ActionGotoTable[0].append('$')
    for v in Variables():
        ActionGotoTable[0].append(v)

    for i in range(len(ActionGotoTable)-1):
        for j in range(len(ActionGotoTable[0])-1):
            temp = ' '
            try:
                temp = str(Action[i][ActionGotoTable[0][j+1]])
                if not '->' in temp:
                    temp = 'S'+temp
                if 'X' in temp:
                    temp = 'ACCEPT'
            except:
                try:
                    temp = GoTo[i][ActionGotoTable[0][j+1]]
                except:
                    temp = ' '
            ActionGotoTable[i+1].append(temp)

def Closure(g):
    s = []
    s.append(g)
    i = 0
    # If dot is at the end return
    if s[i][1][0].index('.')==len(s[i][1][0])-1:
        return s
    #Until all the production rules of the states are checked
    while(i<len(s)):
        if s[i][1][0].index('.')==len(s[i][1][0])-1:
            return s
        else:
            # If terminal after dot, no need to expand
            if s[i][1][0][s[i][1][0].index('.')+1].lower() == s[i][1][0][s[i][1][0].index('.')+1]:
                i+=1
                continue
            else:
                if s[i][1][0].index('.')+2 == len(s[i][1][0]):
                    a = s[i][1][1]
                else:
                    a = First(s[i][1][0][s[i][1][0].index('.')+2])
                for gram in grammar:
                    if gram[0] == s[i][1][0][s[i][1][0].index('.')+1]:
                        for gr in gram[1]:
                            if [gram[0],['.'+gr,a]] in s:
                                i+=1
                                continue
                            else:
                                s.append([gram[0],['.'+gr,a]])
            i+=1
    return s

def States():
    states = []
    initialState = Closure([grammar[0][0],['.'+grammar[0][1][0][0],grammar[0][1][0][1]]])
    states.append(initialState)
    i = 0
    while(i<len(states)):
        GoTo[i] = {}
        Action[i] = {}
        GraphAction[i] = {}

        readMarker = ''

        for state in states[i]:
            if state[1][0].index('.')==len(state[1][0])-1:
                Action[i][state[1][1]]=state[1][0].replace('.','')+'->'+state[0]  ##COMMENT OUT FOR GRAPH VISUALIZATION
                if state[0] == 'X':
                    GraphAction[i][state[1][1]] = 'acc'
                continue
            else:
                index = state[1][0].index('.')
                action = state[1][0][index+1]
                if action in readMarker:
                    continue
                readMarker += action
                redState = []
                C = []
                for state1 in states[i]:
                    index = state1[1][0].index('.')
                    if len(state1[1][0])>index+1:
                        if state1[1][0][index+1] == action:
                            redState.append(deepcopy(state1))
                for rS in redState:
                    index = rS[1][0].index('.')
                    try:
                        rS[1][0] = rS[1][0][:index]+action+'.'+rS[1][0][index+2:]
                    except:
                        rS[1][0] = rS[1][0][:index]+action+'.'
                    C.extend(Closure(rS)) #append
                stateIndex = -1
                temp = []
                for t in C:
                    if t not in temp:
                        temp.append(t)
                C = temp
                if not C in states:
                    states.append(C) #append
                stateIndex = states.index(C)
                if action in alphabet():
                    Action[i][action] = stateIndex
                    GraphAction[i][action] = stateIndex
                else:
                    GoTo[i][action] = stateIndex
        i+=1
    return states

def VisualizeStates():
    graph = graphviz.Digraph(f'CLR-State-Diagram')
    graph.attr(layout='dot')

    for a in GraphAction:
        graph.node(str(a), shape = 'circle', style='filled',color='lightblue')
        for b in GraphAction[a]:
            if GraphAction[a][b] == 'acc':
                graph.node(str(GraphAction[a][b]), shape = 'circle', style='filled',color='lightgreen')
            else:
                graph.node(str(GraphAction[a][b]), shape = 'circle', style='filled',color='lightblue')
            graph.edge(str(a),str(GraphAction[a][b]),label = b)

    for a in GoTo:
        graph.node(str(a), shape = 'circle', style='filled',color='lightblue')
        for b in GoTo[a]:
            graph.node(str(GoTo[a][b]), shape = 'circle', style='filled',color='lightblue')
            graph.edge(str(a),str(GoTo[a][b]),label = b)

    graph.node('start', shape = 'circle', style='filled', color='white')
    graph.node(str(0), shape = 'circle', style='filled',color='lightblue')
    graph.edge('start',str(0))
    graph.format = 'png'
    graph.render(directory='COMP409/Lab/graphviz').replace('\\', '/')


if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MyWindow()

    window.show()
    sys.exit(app.exec_())