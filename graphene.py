#! /usr/bin/env python
# -*- coding: UTF-8 -*-

# ████████╗ ██████╗     ██████╗  ██████╗
# ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔═══██╗
#    ██║   ██║   ██║    ██║  ██║██║   ██║
#    ██║   ██║   ██║    ██║  ██║██║   ██║
#    ██║   ╚██████╔╝    ██████╔╝╚██████╔╝
#    ╚═╝    ╚═════╝     ╚═════╝  ╚═════╝
# Error handling - exit table


import ply.yacc as yacc
import ply.lex as lex
import os, sys
if os.name == "posix":
    import readline
import inspect
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from itertools import chain
import itertools
import sys
import types
import decimal
from lib import grapheneLib as lib
from lib import grapheneHelper as helper
from lib import ast
from collections import namedtuple
import logging

# import symboltable

fread = False
logger = logging.getLogger()
lineNo = 0;

if len(sys.argv) > 1:
    if "-d" in sys.argv:
        logger.setLevel(logging.DEBUG)
    elif "-i" in sys.argv:
        logger.setLevel(logging.INFO)
    if "-f" in sys.argv:
        fread = True


NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)

errorDict = {'ID':'id', 
    'LPAREN':'\'(\'', 
    'DEF':'\'def\'', 
    'IMPLY': '\'=>\'', 
    'LAMDA':'\'lambda\'', 
    'RPAREN':'\')\'', 
    'STRING': 'string',
    'SQRBEGIN':'\'[\'', 
    'SQREND':'\']\'', 
    'CURLBEGIN':'\'{\'', 
    'CURLEND':'\'}\'', 
    'NUMBER': 'number',
    'IF':'\'if\'', 
    'ELSE':'\'else\'', 
    'COMMA':'\',\'',  
    'GR':'\'>\'', 
    'LS':'\'<\'', 
    'NODE':'\'NodeType\'', 
    'GRAPH':'\'Graph\'',
    'GRAPHTYPE':'\'d\', \'u\'', 
    'CONNECTOR':'\'->\', \'<->\'', 
    'NEW':'\'new\'', 
    'NEWLINE':'\'\\n\'', 
    'DOT':'\'.\'', 
    'WHILE':'\'while\'', 
    'FOR':'\'for\'', 
    'FOREACH':'\'foreach\'', 
    'IN':'\'in\'', 
    'HAS':'\'has\'', 
    'ON':'\'on\'', 
    'COLON':'\':\'', 
    'GRTEQ':'\'>=\'',
    'LESSEQ':'\'<=\'',
    'EQUAL':'\'=\'',
    'NEQUAL':'\'!=\'',
    'LOGAND':'\'&&\'',
    'LOGOR':'\'||\'', 
    'ADD_STORE':'\'+=\'', 
    'REMOVE_STORE':'\'-=\'',
    '=':'\'=\'',
    ';':'\';\'',
    '+': '\'+\'',
    '*': '\'+\'',
    '-': '\'-\'',
    '/': '\'/\''}

tokens = ('ID', 'LPAREN', 'DEF', 'IMPLY', 'LAMDA', 'RPAREN', 'STRING', 'SQRBEGIN', 'SQREND', 'CURLBEGIN', 'CURLEND', 'NUMBER', 'IF', 'ELSE', 'COMMA', 'GR', 'LS', 'NODE', 'GRAPH','GRAPHTYPE', 'CONNECTOR', 'NEW', 'NEWLINE', 'DOT', 'WHILE', 'FOR', 'FOREACH', 'IN', 'HAS', 'ON', 'COLON', 'GRTEQ','LESSEQ','EQUAL','NEQUAL','LOGAND','LOGOR', 'ADD_STORE', 'REMOVE_STORE','TRUE','FALSE')
literals = [';', '=', '+', '-', '*', '/']
t_GR = r'\>'
t_LS = r'\<'

RESERVED = {
  "def": "DEF",
  "if": "IF",
  "else": "ELSE",
  "return": "RETURN",
  "while": "WHILE",
  "for": "FOR",
  "foreach": "FOREACH",
  "in":"IN",
  "has": "HAS",
  "on": "ON",
  "NodeType": "NODE",
  "Graph": "GRAPH",
  "Edge": "EDGE",
  "d{": "GRAPHTYPE",
  "u{": "GRAPHTYPE",
  "->": "CONNECTOR",
  "<->": "CONNECTOR",
  "lambda": "LAMDA",
  "True":"TRUE",
  "False":"FALSE"
  }

t_IMPLY = r'=>'

t_CURLBEGIN = r'{'

t_CURLEND = r'}'

t_SQRBEGIN = r'\['

t_SQREND = r'\]'

t_DOT = r'\.'

t_COLON = r':'

t_GRTEQ = r'\>='

t_LESSEQ = r'\<='

t_EQUAL = r'\=='

t_NEQUAL = r'\!='

t_LOGAND = r'\&&'

t_ADD_STORE = r'\+='

t_REMOVE_STORE = r'-='

#TODO - this symbol is giving lexer error -NEHA
# add parsing for logical OR.
t_LOGOR = r'\|\|'

t_LPAREN = r'\('

t_RPAREN = r'\)'

t_STRING = r'[\"\'][a-zA-Z\ /.:0-9(){}]*[\"\']'

t_COMMA = r','

t_NODE = r'Node'

t_GRAPH = r'Graph'

t_NEW = r'new'

t_CONNECTOR = r'<?->'

t_GRAPHTYPE = r'(d|u){1}'

precedence = (
	('left','LOGAND','LOGOR'),
	('left', 'EQUAL', 'NEQUAL'),
	('left','LS','GR','GRTEQ', 'LESSEQ'),
	('left', '+', '-'),
	('left', '*', '/'),
)

def t_TRUE(t):
    r'True'
    t.type = RESERVED.get(t.value, "TRUE")
    logging.debug("----- BOOL: "+t.type+" ------")
    return t

def t_FALSE(t):
    r'False'
    t.type = RESERVED.get(t.value, "FALSE")
    logging.debug("----- BOOL: "+t.type+" ------")
    return t

def t_ID(t):
    r'[a-zA-Z\_][a-zA-Z\_0-9]*'
    t.type = RESERVED.get(t.value, "ID")
    logging.debug("----- TOKEN: ID - "+t.type+" ------")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexpos += len(t.value)
    t.type = "NEWLINE"
    if t.lexer.paren_count == 0:
        return t

def t_WHITESPACE(t):
    r'\s+'
    t.lexpos += len(t.value)

def t_NUMBER(t):
    r"""(\-?\d+(\.\d*)?|\.\d+)([eE][-+]? \d+)?"""
    #t.value = decimal.Decimal(t.value)
    return t

def t_error(t):
    print "Syntax error:"
    print "Type: ",t.type
    print "Token: ",t.value
    print "Line: ",t.lineno
    print "Column: ",t.lexpos
    sys.exit()

def p_error(p):
    if p is None:
        print "Syntax error: unexpected EOF"
    else:
        print "Syntax error at line {}: unexpected token '{}'".format(p.lineno, p.value)

    #Ugly hack since Ply doesn't provide any useful error information
    import inspect
    frame = inspect.currentframe()

    cvars = frame.f_back.f_locals
    errorOutput = []

    for k in cvars['actions'][cvars['state']].keys():
        errorOutput.append(errorDict[k])
        # print errorDict[k]

    print 'Expected one of: ',', '.join(errorOutput) 
    print '\n'
    # print 'Found:', cvars['ltype']
    # print 'Current stack:', cvars['symstack']
    sys.exit()

def cluster(graph,lamda):
    clusters = []
    lamda = lambda x,y:x.get_data()['age']==y.get_data()['age']
    nodes = graph.getNodes()
    for n in nodes:
        print n.get_data()
    if lamda(nodes[0],nodes[1]):
        clusters.append([nodes[0],nodes[1]])
    else:
        clusters.append([nodes[0]])
        clusters.append([nodes[1]])
    print clusters
    nodes = nodes[2:]
    for node in nodes:
        cluster_ids = []
        index = 0 
        for cluster in clusters:
            if lamda(node,cluster[0]):
                cluster.append(node)
                cluster_ids.append(index)
            index+=1
        if len(cluster_ids)==0:
            clusters.append([node])

        # Merge all clusters a node belongs to
        if len(cluster_ids)>1:
            clusters[cluster_ids[0]] = list(set(clusters[cluster_ids]))
            for ind in range(1,len(cluster_ids)):
                clusters[ind]=None
        clusters = filter(lambda a: a != None, clusters)
    print len(clusters)
    index=0
    for cluster in clusters:
        for node in cluster: 
            #print lib.nodeList[node.get_data()['id']].get_data()
            node.__cluster__=index
        index+=1
    #print nodeList
    return clusters


lexer = lex.lex();

####################### TO BE MODIFIED ##############################

def p_program(p):
    '''program : declarationlist'''
    logging.debug("----- program ------")
    p[0]=p[1]

def p_declarations(p):
    '''declarationlist : declaration declarationlist
                       | declaration'''
    logging.debug("----- declaration list ------")
    p[0]=p[1]

def p_declaration(p):
    '''declaration : funcdec
                   | vardec'''
    logging.debug("----- declaration ------")
    p[0]= p[1]
    ast.evaluateAST(p[0], lineNo)

def p_vardec(p):
    '''vardec : node-dec ';'
              | graph-dec ';' '''
    logging.debug("----- variable declaration ------")

    p[0] = p[1]

def p_node(p):
    '''node-dec : ID HAS keylist'''
    #Note - keylist implies parameters

    logging.debug("----- Node declaration -----")

    node = ast.ASTNode()
    node.type = 'node-dec'

    child1 = ast.ASTNode()
    child1.value = p[1]
    child2 = ast.ASTNode()
    child2.value = p[3]

    node.children.append(child1)
    node.children.append(child2)
    p[0] = node

def p_keylist(p):
    '''keylist : idOrAlphanum
               | idOrAlphanum COMMA keylist'''

    logging.debug("----- Node declaration keylist -----")

    p[0] = []
    if p[1].type == "id":
        p[0].append(p[1].children[0])
    else:
        p[0].append(p[1].value)
    if len(p) == 4:
        if p[1] in p[3]:
            logging.critical("Same property name for node.")
            system.exit(-1)

        p[0] += p[3]

def p_graph(p):
    '''graph-dec : GRAPH ID HAS GRAPHTYPE edgelist CURLEND
                 | GRAPH ID HAS GRAPHTYPE edgelist CURLEND ON idOrAlphanum '''

    logging.debug("----- Graph declaration -----")

    node = ast.ASTNode()
    node.type = 'graph-dec'

    gid = ast.ASTNode()
    gid.type = "id"
    gid.value = p[2]
    gtype = ast.ASTNode()
    gtype.type = "terminal"
    gtype.value = p[4]
    edges = p[6]

    key = ast.ASTNode()
    key.type = "terminal"
    key.value = "id"

    if(len(p) == 10):
        key.value = p[9]

    node.children.append(gid)
    node.children.append(gtype)
    node.children.append(key)
    node.children.append(p[6])

    p[0] = node

#
#  ████████╗ ██████╗     ██████╗  ██████╗
#  ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔═══██╗
#     ██║   ██║   ██║    ██║  ██║██║   ██║
#     ██║   ██║   ██║    ██║  ██║██║   ██║
#     ██║   ╚██████╔╝    ██████╔╝╚██████╔╝
#     ╚═╝    ╚═════╝     ╚═════╝  ╚═════╝
#
#   Parse node ids to check if node exists
#

def p_edgelist(p):
    '''edgelist : idOrAlphanum CONNECTOR idOrAlphanum
                | idOrAlphanum CONNECTOR idOrAlphanum COMMA edgelist
                | idOrAlphanum CONNECTOR idOrAlphanum LPAREN arglist RPAREN
                | idOrAlphanum CONNECTOR idOrAlphanum LPAREN arglist RPAREN COMMA edgelist'''

    logging.debug("----- Graph declaration keylist -----")

    edgelist = ast.ASTNode()
    edgelist.type = "edgelist"

    edgelist.children.append(p[1])
    edgelist.children.append(p[2])
    edgelist.children.append(p[3])

    if len(p) == 6:
        edgelist.children.append(None)
    if len(p) > 4:
        edgelist.children.append(p[5])
    if len(p) > 7:
        edgelist.children.append(p[8])

    p[0] = edgelist

def p_decstatement(p):
    '''declaration : statement'''
    logging.debug("---- declaration ---")
    p[0]=p[1]
    ast.evaluateAST(p[0], lineNo)

def p_compoundstatement(p):
    '''statement : compoundstatement'''
    p[0]=p[1]

def p_compoundstatementdef(p):
    '''compoundstatement : CURLBEGIN statementlist CURLEND
                         | CURLBEGIN CURLEND '''
    p[0] = ast.ASTNode()
    p[0].type = 'compoundstatement'
    if len(p)==4:    
        p[0].children.append(p[2])
    else:
        p[0].children.append(None)

def p_funccompoundstatementdef(p):
    '''funccompoundstatement : CURLBEGIN statementlist CURLEND
                         | CURLBEGIN CURLEND '''
    p[0] = ast.ASTNode()
    p[0].type = 'funccompoundstatement'
    if len(p)==4:    
        p[0].children.append(p[2])
    else:
        p[0].children.append(None)

######### function def #########################

def p_funcdec(p):
    '''funcdec : func ';' '''
    p[0] = p[1]

def p_func(p):
    '''func : DEF parameters IMPLY ID funccompoundstatement IMPLY returnarguments'''
    #funcdef : DEF parameters IMPLY ID CURLBEGIN statementlist CURLEND IMPLY returnlist
    #p[0] = ast.Function(None, p[2], tuple(p[3]), (), 0, None, p[5])
    Node = ast.ASTNode()
    Node.type = 'function-dec'
    Node.children.append(p[4])  #ID

    compoundChild = ast.ASTNode()
    compoundChild.type = 'function-signature'
    compoundChild.children.append(p[5])  #statements
    compoundChild.children.append(p[2])  #arguments
    compoundChild.children.append(p[7])  #returnargs

    Node.children.append(compoundChild)

    p[0]=Node

def p_lambda(p):
    ''' lamda : LAMDA parameters COLON funccompoundstatement IMPLY returnarguments'''
    logging.debug("In lambda")
    termNode = ast.ASTNode()
    termNode.type = "lambda"
    termNode.children.append(p[2])
    termNode.children.append(p[4])
    termNode.children.append(p[6])
    p[0] = termNode

def p_assignlambda(p):
    '''assignmentexpression : ID '=' lamda'''
    logging.debug("-------In assignLambda-------")

    node = ast.ASTNode()
    node.type = "lamdaassign"
    #node.children.append(p[1])
    #node.children.append(p[3])

    ####### Return Arg. None ####
    Node = ast.ASTNode()
    Node.type = 'return-args'
    if len(p) == 3:
        Node.children.append(None)
    
    node.children.append(p[1])  #ID

    compoundChild = ast.ASTNode()
    compoundChild.type = 'lamda-signature'
    compoundChild.children.append(p[3].children[1])  #statements
    compoundChild.children.append(p[3].children[0])  #arguments
    compoundChild.children.append(p[3].children[2])  #return
    print '++++++++++++++++++++++++'
    print Node.children
    print '++++++++++++++++++++++++'
    node.children.append(compoundChild)

    p[0]=node 


def p_parameters(p):
    """parameters : LPAREN RPAREN
                  | LPAREN varargslist RPAREN"""
    Node = ast.ASTNode()
    Node.type = 'function-pars'
    if len(p) == 3:
        Node.children.append(None)
    else:
        for n in p[2]:
            Node.children.append(n)
    p[0] = Node

def p_varargslist(p):
    """varargslist : varargslist COMMA ID
                   | ID"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_returnarguments(p):
    """returnarguments : LPAREN RPAREN
                  | LPAREN returnset RPAREN"""
    Node = ast.ASTNode()
    Node.type = 'return-args'
    if len(p) == 3:
        Node.children.append(None)
    else:
        for n in p[2].children:
            Node.children.append(n)
    p[0] = Node

def p_returnset(p):
    '''returnset : expression
                | expression COMMA returnset'''

    logging.debug("returnset")

    arglistNode = ast.ASTNode()
    arglistNode.type = "returnset"

    arglistNode.children.append(p[1])

    if len(p) > 2:
        arglistNode.children.extend(p[3].children)
    p[0] = arglistNode


def p_statementlist(p):
    '''statementlist : statement
                     | statement statementlist'''

    node = ast.ASTNode();
    node.type = "statementlist";
    node.children.append(p[1]);
    if len(p)==3:
        logging.debug('Statement list... appending children of statementlist to current statementlist')
        node.children.extend(p[2].children);
    p[0]=node

    logging.debug(p[0].type)


def p_statement(p):
    '''statement : expressionstatement
                 | iterationstatement
				 | selectionstatement'''

    logging.debug("statement")

    p[0]=p[1]

def p_edgeexpression(p):
    '''edgeaddition : ID ADD_STORE idOrAlphanum CONNECTOR idOrAlphanum'''
    logging.debug("-------In edgeaddition-------")
    node = ast.ASTNode()
    node.type = "addedge"
    node.children.append(p[1])
    node.children.append(p[3])
    node.children.append(p[4])
    node.children.append(p[5])

    p[0] = node

def p_node_removal_expression(p):
    '''noderemoval : ID REMOVE_STORE nodeLookup'''
    logging.debug("-------In noderemoval-------")
    node = ast.ASTNode()
    node.type = "removenode"
    node.children.append(p[1])
    node.children.append(p[3])
    p[0] = node

def p_node_lookup(p):
    '''nodeLookup : idOrAlphanum COLON idOrAlphanum
                  | COLON idOrAlphanum'''
    logging.debug("nodeLookup")
    node = ast.ASTNode()
    node.type = "lookupnode"
    if len(p) == 3:
        node.children.append("id")
        node.children.append(p[2])
    elif len(p) == 4:
        node.children.append(p[1])
        node.children.append(p[3])
    else:
        node.children.append(p[1])
    p[0] = node


def p_iterationstatement(p):
    '''iterationstatement : WHILE LPAREN expression RPAREN statement
                          | FOR LPAREN statement expression ';' statement RPAREN CURLBEGIN statement CURLEND
                          | FOREACH LPAREN ID IN ID RPAREN CURLBEGIN statementlist CURLEND
                          | FOREACH LPAREN ID IN expression RPAREN CURLBEGIN statementlist CURLEND'''

    if ( p[1] == 'while' ):
        Node = ast.ASTNode()
        Node.type = 'while'
        Node.children.append(p[3]) #Condition
        Node.children.append(p[5]) #Statement
        p[0]=Node
        logging.debug("-------In iterationstatement (while loop)-------")

    if( p[1] == 'for' ):
        Node = ast.ASTNode()
        Node.type = 'for'
        Node.children.append(p[3]) #Initialization
        Node.children.append(p[4]) #Condition
        Node.children.append(p[6]) #Update
        Node.children.append(p[9]) #Statement
        p[0] = Node

        logging.debug("-------In iterationstatement (for loop)-------")
    
    if( p[1] == 'foreach' ):
        Node = ast.ASTNode()
        Node.type = 'foreach'
        Node.children.append(p[3]) #Iter variable
        Node.children.append(p[5]) #Iter list
        Node.children.append(p[8]) #Statement
        logging.debug("THIS: ")
        logging.debug(p[3])
        logging.debug(p[5])
        logging.debug(p[8].type)
        
        p[0] = Node
        logging.debug("-------In iterationstatement (foreach loop)-------")
        
    
def p_selStatement(p):
    '''selectionstatement : IF LPAREN expression RPAREN compoundstatement
                            | IF LPAREN expression RPAREN compoundstatement ELSE compoundstatement'''
    node = ast.ASTNode()
    node.type="if"
    node.children.append(p[3])
    node.children.append(p[5])
    if(len(p)>6):
        node.children.append(p[7])
    p[0] = node
    logging.debug("-------In selectionstatement (if-else)-------")

def p_expressionstatement(p):
    '''expressionstatement : ';'
                           | completeexpression ';'  '''

    logging.debug("expStatement")

    if(not (len(p) == 2)):
        logging.debug("non empty statement")
        p[0] = p[1]
        logging.debug(p[0].type)

def p_expression(p):
    '''completeexpression : callchain
                  | assignmentexpression
                  | edgeaddition
                  | noderemoval'''

    logging.debug("expr")
    p[0] = p[1]
    logging.debug(p[0].type)

#removed this we are supporting dynamic typing (can introduce later if required)

##def p_assignmentexpression(p):
##    '''assignmentexpression : Type ID '=' Type '.' new '(' ')'
##                            | Type ID '=' assignmentexpression'''

def p_assignval(p):
    '''assignmentexpression : ID '=' expression
                            | arglist '=' expression
                            | ID '=' nodeLookup
                            | ID '=' SQRBEGIN values SQREND
                            | ID '=' SQRBEGIN SQREND
                            | ID '=' ID SQRBEGIN SQREND
                            | ID SQRBEGIN idOrAlphanum SQREND '=' idOrAlphanum
                            | ID SQRBEGIN idOrAlphanum SQREND '=' SQRBEGIN values SQREND'''


    #helper.ids[p[1]] = p[3]
    logging.debug("-------In assignExpr-------")

    node = ast.ASTNode()
    if len(p) == 6:
        node.type = "listassignment"
        node.children.append(p[1])
        node.children.append(p[4])

    elif len(p) == 5:
        n = ast.ASTNode()
        n.type = "terminal"
        n.children.append(None)
        node.type = "listassignment"
        node.children.append(p[1])
        node.children.append(n)

    elif len(p) == 7 and p[2] == "=":
        node.type = "indexassignment"
        node.children.append(p[1])
        termNode = ast.ASTNode()
        termNode.type = "terminal"
        termNode.value = p[3]
        node.children.append(termNode)
        node.children.append(p[5])

    elif len(p) == 7:
        node.type = "rindexassignment"
        node.children.append(p[1])
        node.children.append(p[3])
        node.children.append(p[6])

    elif len(p) == 9:
        node.type = "rindexassignment"
        node.children.append(p[1])
        node.children.append(p[3])
        node.children.append(p[7])

    else:
        node.type="assignment"
        node.children.append(p[1])
        node.children.append(p[3])
        logging.info('assigned '+str(p[1]))

    p[0] = node

# def p_expression_string(p):
#     '''expression : STRING'''
#     logging.debug("p_expressionString")
#     termNode = ast.ASTNode()
#     termNode.type = "terminal"
#     termNode.value = p[1][1:-1]
#     p[0] = termNode
#     logging.debug(p[0].type)

def p_values(p):
    '''values : valuelist'''
    node = ast.ASTNode()
    node.type = "terminal"
    values = []
    for i in range(0,len(p[1].children)):
        values.append(p[1].children[i])
    node.value = values
    p[0] = node
    logging.debug(p[0].type)
    

def p_valueList(p):
    '''valuelist : idOrAlphanum COMMA valuelist
                | idOrAlphanum'''

    logging.debug("valuelist")

    vallistNode = ast.ASTNode()
    vallistNode.type = "valuelist"

    vallistNode.children.append(p[1])

    if len(p) > 2:
        for i in range (0,len(p[3].children)):
            vallistNode.children.append(p[3].children[i])

    p[0] = vallistNode
    logging.debug(p[0].type)


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

    logging.debug(str(p[1])+str(p[3]))

    if p[2] == '+' :
        logging.debug('---sum---')
        node = ast.ASTNode()
        node.type = "plus"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

    # if isinstance(p[1], NumberTypes) and isinstance(p[3], NumberTypes):
    if p[2] == '-' :
        logging.debug('---minus---')
        node = ast.ASTNode()
        node.type = "minus"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

    elif p[2] == '*' :
        logging.debug('---multiply---')
        node = ast.ASTNode()
        node.type = "multiply"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

    elif p[2] == '/':
        logging.debug('---divide---')
        node = ast.ASTNode()
        node.type = "divide"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

def p_expression_relop(p):
    '''expression : expression LS expression
                    | expression GR expression
                    | expression GRTEQ expression
                    | expression LESSEQ expression
                    '''
    logging.debug(str(p[1])+str(p[3]))

    if p[2] == '<' :
        logging.debug('---less-than---')
        node = ast.ASTNode()
        node.type = "less"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

    elif p[2] == '>' :
        logging.debug('---greater-than---')
        node = ast.ASTNode()
        node.type = "greater"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

    elif p[2] == '<=' :
        logging.debug('---less-than-equal---')
        node = ast.ASTNode()
        node.type = "lessequal"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

    elif p[2] == '>=' :
        logging.debug('---greater-than-equal---')
        node = ast.ASTNode()
        node.type = "greaterequal"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node
##        if isinstance(p[1], decimal.Decimal) and isinstance(p[3], decimal.Decimal):
##            p[0] = p[1] < p[3]
##    if isinstance(p[1], decimal.Decimal) and isinstance(p[3], decimal.Decimal):
##        if p[2] == '>' : p[0] = p[1] > p[3]
##        elif p[2] == '>=' : p[0] = p[1] >= p[3]
##        elif p[2] == '<=' : p[0] = p[1] <= p[3]

def p_expression_logicalop(p):
    '''expression : expression LOGAND expression
                  | expression LOGOR expression'''
    logging.debug(str(p[1])+str(p[3]))

    if p[2] == '&&' :
        logging.debug('---log-and---')
        node = ast.ASTNode()
        node.type = "land"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

    elif p[2] == '||' :
        logging.debug('---log-or---')
        node = ast.ASTNode()
        node.type = "lor"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node
##    print p[1],p[3]
##    if(p[2] == '&&'):
##        p[0] = p[1] and p[3]
##    elif(p[2] == '||'):
##        p[0] = p[1] or p[3]


def p_expression_eqop(p):
    '''expression : expression EQUAL expression
                    | expression NEQUAL expression'''

    logging.debug(str(p[1])+str(p[3]))

    if p[2] == '==' :
        logging.debug('---equal---')
        node = ast.ASTNode()
        node.type = "equal"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

    elif p[2] == '!=' :
        logging.debug('---not-equal---')
        node = ast.ASTNode()
        node.type = "nequal"
        node.children.append(p[1])
        node.children.append(p[3])
        p[0] = node

##    print p[1], p[3]
##    if p[2] == '==' :
##        if isinstance(p[1], decimal.Decimal) and isinstance(p[3], decimal.Decimal):
##            p[0] = p[1] == p[3]
##    if isinstance(p[1], decimal.Decimal) and isinstance(p[3], decimal.Decimal):
##        if p[2] == '!=' : p[0] = p[1] != p[3]

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN '''
    p[0] = p[2]

# def p_expression_string(p):
#     '''expression : STRING'''
#     logging.debug("p_expressionString")
#     termNode = ast.ASTNode()
#     termNode.type = "terminal"
#     termNode.value = str(p[1][1:-1])
#     p[0] = termNode
#     logging.debug(p[0].type)

def p_expression_idOrAlphaNum(p):
    '''expression : idOrAlphanum'''
    logging.debug("p_expressionNumber")
    # termNode = ast.ASTNode()
    # termNode.type = "terminal"
    # if '.' in p[1]:
    #     termNode.value = float(p[1])
    # else:
    #     termNode.value = int(p[1])
    # p[0] = termNode
    # logging.debug(p[0].type)
    p[0] = p[1]

# def p_expression_name(p):
#     '''expression : ID'''
#     try:
#         logging.debug("p_expressionId")
#         node = ast.ASTNode()
#         node.type = "id"
#         node.children.append(p[1])
#         p[0]=node
#     except LookupError:
#         logging.error(str("Undefined name '%s'" % p[1]))
#         p[0] = 0

# def p_expression_booleanExp(p):
#     '''expression : TRUE
#                   | FALSE '''
#     logging.debug("p_expressionBoolean")
#     termNode = ast.ASTNode()
#     termNode.type = "terminal"
#     termNode.value = p[1]
#     p[0] = termNode
#     logging.debug(p[0].type)

def p_expression_listIndex(p):
    '''expression : ID SQRBEGIN idOrAlphanum SQREND '''
    logging.debug("p_expressionListIndex")
    termNode = ast.ASTNode()
    termNode.type = "listIndex"
    # termNode.value = p[1]
    termNode.children.append(p[1])
    termNode.children.append(p[3])
    p[0] = termNode
    logging.debug(p[0].type)

def p_exp_call(p):
    '''expression : callchain'''
    p[0] = p[1]

#################################

def p_callchain(p):
    '''callchain : call 
                 | call DOT callchain'''
        
    node = ast.ASTNode()
    node.type = "callchain"
    node.children.append(p[1])
    node.chain_next = None
    if len(p)>2:
        node.chain_next = p[3].children[0]
    p[0] = node

def p_call(p):
    '''call : ID LPAREN callarglist RPAREN
            | ID DOT ID LPAREN callarglist RPAREN
            | ID DOT ID LPAREN RPAREN
            | ID LPAREN RPAREN'''

    logging.debug("call")
    for x in p:
        logging.debug(x)

    logging.debug("p_call")
    node = ast.ASTNode()
    node.type = "funccall"
    if(len(p) >= 6):
        node.type = "member_funccall"
        logging.debug("****member_funccall****")
        node.children.append(p[1])      #object
        node.children.append(p[3])      #member function
        if len(p) ==7:
            # child = ast.ASTNode()
            # child.type = 'arglist'
            # child.value = p[5]
            node.children.append(p[5])
    else:
        node.children.append(p[1])
        if len(p) == 5:
            logging.debug("****func_arg****")
            # child = ast.ASTNode()
            # child.type = 'arglist'
            # child.value = p[3]
            node.children.append(p[3])  #actual arguments passed to function
        else:
            node.children.append(None)  #No arguments passed
    p[0] = node

def p_callarglist(p):
    '''callarglist : expression COMMA arglist
               | expression'''

    logging.debug("callarglist")

    arglistNode = ast.ASTNode()
    arglistNode.type = "arglist"

    arglistNode.children.append(p[1])

    if len(p) > 2:
        arglistNode.children.append(p[3].children[0])

    p[0] = arglistNode
    logging.debug(p[0].type)

def p_arg(p):
    '''arglist : idOrAlphanum COMMA arglist
               | idOrAlphanum'''

    logging.debug("arglist")

    arglistNode = ast.ASTNode()
    arglistNode.type = "arglist"

    arglistNode.children.append(p[1])

    if len(p) > 2:
        arglistNode.children.append(p[3].children[0])

    p[0] = arglistNode
    logging.debug(p[0].type)

def p_isNumber(p):
    ''' idOrAlphanum : NUMBER '''

    logging.debug("idorstr"+ str(len(p)))
    for x in p:
        logging.debug(x)
    logging.debug("p_isNumber")

    termNode = ast.ASTNode()
    termNode.type = "terminal"
    if '.' in p[1]:
        termNode.value = float(p[1])
    else:
        termNode.value = int(p[1])
    p[0] = termNode
    logging.debug(p[0].type)

def p_isBoolean(p):
    ''' idOrAlphanum : TRUE 
                     | FALSE'''

    logging.debug("idorstr"+ str(len(p)))
    for x in p:
        logging.debug(x)
    logging.debug("p_isBoolean")

    termNode = ast.ASTNode()
    termNode.type = "terminal"
    termNode.value = p[1]
    p[0] = termNode
    logging.debug(p[0].type)

def p_isString(p):
    ''' idOrAlphanum : STRING '''

    logging.debug("idorstr "+str(len(p)))
    for x in p:
        logging.debug(x)
    logging.debug("p_isString")

    termNode = ast.ASTNode()
    termNode.type = "terminal"
    termNode.value = str(p[1][1:-1])
    p[0] = termNode
    logging.debug(p[0].type)

def p_isId(p):
    ''' idOrAlphanum : ID'''
    logging.debug("idorstr "+str(len(p)))
    for x in p:
        logging.debug(x)
    logging.debug("p_isID")

    termNode = ast.ASTNode()
    termNode.type = "id"
    termNode.children.append(p[1])
    p[0] = termNode
    logging.debug(p[0].type)

parser = yacc.yacc()
        
try:
    f = open("proc/state.json", 'w')
    f.write('{"lastNodeId": -1, "nodes": [], "links": []}')
    f.close()
except Exception, e:
    logging.critical("Unable to initialize.")
    helper.gexit()

if fread:
    with open(sys.argv[2]) as f:
        s = ' '
        for line in f:
            lineNo += 1
            s = s+line.rstrip()
            if len(s) == 0:
                s = ' '

            if s[-1] == ';' and helper.completeCodeStmt(s) == True:
                parser.parse(s)
                s = ' '
else:
    while True:
        try:
            s=raw_input('graphene> ').rstrip()
            lineNo += 1
            if len(s) == 0:
                s = ' '
            while s[-1] != ';' or helper.completeCodeStmt(s) == False:
                s = s+raw_input('>');
                lineNo += 1

        except EOFError:
            break

        except KeyboardInterrupt:
            print "\n"
            helper.gexit()
        if not s: continue
        parser.parse(s)
