import ply.yacc as yacc
import ply.lex as lex
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


from vendors import guiInput

tokens = ('ID', 'LPAREN', 'RPAREN', 'STRING', 'WHITESPACE', 'DOT')

t_ID = r'[a-zA-Z\_][a-zA-Z\_0-9]+'
     
t_DOT = r'\.'
t_LPAREN = r'\('

t_RPAREN = r'\)'
    
t_STRING = r'\"[a-zA-Z\ 0-9]+\"'

t_WHITESPACE = r'\s+'

def t_error(t):
    print "Lex Error"

def strlen(G):
    print "Count:", len(G)

def myprint(G):
    print G
    
def goutput():
    print "Doing graph output. BRB"

def ginput():
    print guiInput.main()

func_map = {'print' : myprint, 'strlen' : strlen, 'graphene' : {'input' : ginput, 'output' : goutput} }    
    
lexer = lex.lex();


def p_call(p):
    '''call : ID LPAREN STRING RPAREN
            | ID DOT ID LPAREN RPAREN '''
    if(len(p) == 6):

        func_map[p[1]][p[3]]()
    else:
        if(p[1] in func_map):
            func_map[p[1]](p[3][1:-1])
        else:
            print "You sir, suck."

parser = yacc.yacc()

class Graph:
    ''' Internal representation of a graph object '''
    id = -1
    __globalGraphIDVal = 0
    
    class Node:
        __globalNodeIDVal = 0
        id = -1
        properties = dict()
        
        
        def __init(self):
            id = __globalNodeIDVal
            __globalNodeIDVal += 1
    
    adjList = []
    nodes = []
    edges = []
    
    def __init__(self):
        nodes = []
        edges = []
        id = __globalGraphIDVal
        __globalGraphIDVal += 1

#output format to internal representation
def outToInNodes(nodes):
    final =dict()
    for node in nodes:
        final[node['id']] = node['name']
    return final


def outToInLinks(links):
    final = dict()
    for link in links:
        try:
            final[link['source']].append({'target':link['target'], 'weight':link['weight']})
        except KeyError:
            final[link['source']] = [{'target':link['target'], 'weight':link['weight']}]
    return final


#internal representation to output

def inToOutLinks(sources):
    final = []
    for source in sources.keys():
        print source
        for target in sources[source]:
           final.append({'source': source, 'target' :target['target'], 'left':True, 'right':True, 'weight':target['weight']})

    return final


while True: 

    try:
        s = raw_input('graphene> ')
    except EOFError:
        break
    if not s: continue 
    result = parser.parse(s) 
