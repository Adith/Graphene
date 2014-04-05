import ply.yacc as yacc
import ply.lex as lex

#print("Hello world!")

tokens = ('ID', 'LPAREN', 'RPAREN', 'STRING', 'OPTIONALWHITESPACE', 'WHITESPACE')

t_ID = r'[a-zA-Z\_][a-zA-Z\_0-9]+'
     
t_LPAREN = r'\('

t_RPAREN = r'\)'
    
t_STRING = r'\"[a-zA-Z\ 0-9]+\"'

t_OPTIONALWHITESPACE = r'\s*'

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
    print "Doing graph input. BRB"
    
func_map = {'print' : myprint, 'strlen' : strlen, 'graphene.input' : ginput, 'graphene.output' : goutput}    
    
lexer = lex.lex();


def p_call(p):
    '''call : ID OPTIONALWHITESPACE LPAREN OPTIONALWHITESPACE STRING OPTIONAL WHITESPACE RPAREN'''
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


while True: 

    try:
        s = raw_input('graphene> ')
    except EOFError:
        break
    if not s: continue 
    result = parser.parse(s) 