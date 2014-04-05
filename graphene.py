import ply.yacc as yacc
import ply.lex as lex
from itertools import chain
import itertools

debug = 0

#print("Hello world!")

tokens = ('ID', 'LPAREN', 'RPAREN', 'STRING', 'WHITESPACE', 'COMMA')

t_ID = r'[a-zA-Z\_][a-zA-Z\_0-9]+'
     
t_LPAREN = r'\('

t_RPAREN = r'\)'
    
t_STRING = r'\"[a-zA-Z\ 0-9]*\"'

t_WHITESPACE = r'\s+'

t_COMMA = r','

def t_error(t):
    print "Lex Error"

def strlen(G):
    print "Count:", len(G)

def myprint(G):
    #print len(G)
    for x in G:
        print x[1:-1],
        
    print ""
    
def goutput():
    print "Doing graph output. BRB"

def ginput():
    print "Doing graph input. BRB"
    
func_map = {'print' : myprint, 'strlen' : strlen, 'graphene.input' : ginput, 'graphene.output' : goutput}    
    
lexer = lex.lex();


def p_call(p):
    '''call : ID LPAREN arglist RPAREN'''
    
    if(debug):
        print "call ",len(p)
        for x in p:
            print x,
        print ""
    
    if(p[1] in func_map):
        func_map[p[1]](p[3])
    else:
        print "Function not found. Please replace developer."

def p_arglist(p):
    '''arglist : idOrString
               | idOrString COMMA arglist
               | '''
    if(debug):
        print "arglist ", len(p), p[0],p[1]
        for x in p:
            print x,",",
        print ""
        
    arglist = []
    i=1
    while i<len(p):
        arglist.append(p[i])
        i+=2
    if(p[0] == None):
        p[0] = arglist
    else:
        p[0].extend(arglist)
        
    p[0] = list(chain.from_iterable(itertools.repeat(x,1) if isinstance(x,str) else x for x in p[0]))
    #itertools.repeat(x,1) if isinstance(x,str) else x for x in items

def p_idOrString(p):
    ''' idOrString : ID
                   | STRING '''
                   
    if(debug):
        print "idorstr", len(p)
        for x in p:
            print x,",",
        print ""
    p[0] = p[1];
    
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

def inToOutNodes(nodeL):
    finalStr =[]
    for node in nodeL:
        print node
        finalStr.append({'id:': node, 'name': nodeL[node]})
    return finalStr

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
