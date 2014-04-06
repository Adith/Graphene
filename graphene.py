import ply.yacc as yacc
import ply.lex as lex
from itertools import chain
import itertools
import sys
import types
import decimal

debug = 0

#print("Hello world!")
NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)

tokens = ('ID', 'LPAREN', 'RPAREN', 'STRING', 'NUMBER', 'WHITESPACE', 'COMMA', 'Node', 'Edge', 'Graph', 'new', 'NEWLINE')
literals = [';', '=', '+', '-', '*', '/']
ids={}

t_ID = r'[a-zA-Z\_][a-zA-Z\_0-9]+'
     
t_LPAREN = r'\('

t_RPAREN = r'\)'
    
t_STRING = r'\"[a-zA-Z\ 0-9]*\"'

t_WHITESPACE = r'\s+'

t_COMMA = r','

t_Node = r'Node'

t_Edge = r'Edge'

t_Graph = r'Graph'

t_new = r'new'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    if t.lexer.paren_count == 0:
        return t

def t_NUMBER(t):
    r"""(\d+(\.\d*)?|\.\d+)([eE][-+]? \d+)?"""
    t.value = decimal.Decimal(t.value)
    return t

def t_error(t):
    print "Syntax error:"
    print "Type: ",t.type
    print "Token: ",t.value
    print "Line: ",t.lineno
    print "Column: ",t.lexpos
    sys.exit()

def strlen(G):
    print "Count:", len(G)

def myprint(G):
    #print len(G)
    for x in G:
        print x,
        
    print ""
    
def goutput():
    print "Doing graph output. BRB"

def ginput():
    print "Doing graph input. BRB"
    
func_map = {'print' : myprint, 'strlen' : strlen, 'graphene.input' : ginput, 'graphene.output' : goutput}    
    
lexer = lex.lex();

def p_statementlist(p):
    '''statementlist : statement
                     | statement statementlist'''

def p_statement(p):
    '''statement : expressionstatement'''

def p_expressionstatement(p):
    '''expressionstatement : ';'
                           | completeexpression ';' '''

def p_expression(p):                       
    '''completeexpression : call
                  | assignmentexpression
                  '''

#removed this we are supporting dynamic typing (can introduce later if required)

##def p_assignmentexpression(p):
##    '''assignmentexpression : Type ID '=' Type '.' new '(' ')'
##                            | Type ID '=' assignmentexpression'''

def p_assignval(p):
    "assignmentexpression : ID '=' expression"
    ids[p[1]] = p[3]
    print 'assigned ',p[1]
    
##def p_Type(p):
##    "Type : primitivetype"
##
##def p_primitivetype(p):
##    '''primitivetype : Node
##                     | Edge
##                     | Graph '''


################ ARITHMETIC EXPRESSIONS #################

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    print p[1], p[3]
    if p[2] == '+' :
        if isinstance(p[1], decimal.Decimal) and isinstance(p[3], decimal.Decimal):
            p[0] = p[1] + p[3]
        else:
            p[0] = p[1][1:-1] + p[3][1:-1]
    if isinstance(p[1], NumberTypes) and isinstance(p[3], NumberTypes):
        if p[2] == '-' : p[0] = p[1] - p[3]
        elif p[2] == '*' : p[0] = p[1] * p[3]
        elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]
    
def p_expression_string(p):
    "expression : STRING"
    p[0] = p[1]

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]

def p_expression_name(p):
    "expression : ID"
    try:
        p[0] = ids[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

#################################



def p_call(p):
    "call : ID LPAREN arglist RPAREN"
    
    if(debug):
        print "call ",len(p)
        for x in p:
            print x,
        print ""
    
    if(p[1] in func_map):
        func_map[p[1]](p[3])
    else:
        print "Function not found. Please replace developer."

##def p_arglist(p):
##    '''arglist : idOrString
##               | idOrString COMMA arglist
##               | '''
##    if(debug):
##        print "arglist ", len(p), p[0],p[1]
##        for x in p:
##            print x,",",
##        print ""
##        
##    arglist = []
##    i=1
##    while i<len(p):
##        arglist.append(p[i])
##        i+=2
##    if(p[0] == None):
##        p[0] = arglist
##    else:
##        p[0].extend(arglist)
##        
##    p[0] = list(chain.from_iterable(itertools.repeat(x,1) if isinstance(x,str) or isinstance(x,decimal.Decimal) else x for x in p[0]))
##    #itertools.repeat(x,1) if isinstance(x,str) else x for x in items


def p_arg(p):
    '''arglist : idOrString COMMA arglist
               | idOrString'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]
    
def p_istring(p):
    ''' idOrString : STRING '''
                   
    if(debug):
        print "idorstr", len(p)
        for x in p:
            print x,",",
        print ""
    p[0] = p[1];

def p_iid(p):
    ''' idOrString : ID'''
    p[0] = ids[p[1]];
    
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
