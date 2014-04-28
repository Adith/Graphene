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
from vendors import gui

from itertools import chain
import itertools
import sys
import types
import string
import decimal
import random
import json
from lib import grapheneLib as lib
from lib import grapheneHelper as helper
from lib import ast
from collections import namedtuple
import ast
import logging

# import symboltable

logger = logging.getLogger()
if len(sys.argv) > 1:
    if sys.argv[1] in ['--debug', '-d']:
        logger.setLevel(logging.DEBUG)
    elif sys.argv[1] in ['--info', '-i']:
        logger.setLevel(logging.INFO)

function=dict()

NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)

tokens = ('ID', 'LPAREN', 'DEF', 'IMPLY', 'RPAREN', 'STRING', 'SQRBEGIN', 'SQREND', 'CURLBEGIN', 'CURLEND', 'NUMBER', 'IF', 'ELSE', 'COMMA', 'GR', 'LS', 'NODE', 'GRAPH','GRAPHTYPE', 'CONNECTOR', 'NEW', 'NEWLINE', 'DOT', 'WHILE', 'FOR', 'FOREACH', 'IN', 'HAS', 'ON', 'COLON', 'GRTEQ','LESSEQ','EQUAL','NEQUAL','LOGAND','LOGOR')
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
  "d": "GRAPHTYPE",
  "u": "GRAPHTYPE",
  "->": "CONNECTOR",
  "<->": "CONNECTOR"
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

#TODO - this symbol is giving lexer error -NEHA
# add parsing for logical OR.
#t_LOGOR = r'\||'

t_LPAREN = r'\('

t_RPAREN = r'\)'

t_STRING = r'[\"|\'][a-zA-Z\ /.0-9]*[\"|\']'

t_COMMA = r','

t_NODE = r'Node'

t_GRAPH = r'Graph'

t_NEW = r'new'

t_CONNECTOR = r'<?->'

t_GRAPHTYPE = r'(d|u){1}'

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
        print "Syntax error at line {}: unexpected token {}".format(p.lineno, p.value)

    #Ugly hack since Ply doesn't provide any useful error information
    import inspect
    frame = inspect.currentframe()
    cvars = frame.f_back.f_locals
    print 'Expected:', ', '.join(cvars['actions'][cvars['state']].keys())
    print 'Found:', cvars['ltype']
    print 'Current stack:', cvars['symstack']
    sys.exit()

def strlen(node):
    print "Count:", len(G)

def gprint(*node):
    logging.debug('******print******')
    for e in node:
        if type(e).__bases__[0].__name__ in ["Node"]:
            print "Node has"
            e.print_data();
        elif isinstance(e, lib.Graph):
            print "Graph has {"
            e.print_data();
            print "}"
        elif isinstance(e,list):
            for v in e:
                if isinstance(v, ast.ASTNode):
                    gprint(evaluateAST(v).value)
                else:
                    gprint(v)
        else:
            print evaluateAST(e)

# ████████╗ ██████╗     ██████╗  ██████╗
# ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔═══██╗
#    ██║   ██║   ██║    ██║  ██║██║   ██║
#    ██║   ██║   ██║    ██║  ██║██║   ██║
#    ██║   ╚██████╔╝    ██████╔╝╚██████╔╝
#    ╚═╝    ╚═════╝     ╚═════╝  ╚═════╝
# Graph to be displayed visually. Global nodelist has to be
# size limited to only the nodes in the specified graph
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def goutput(graph=None):
    # Prints state to D3
    # Note: state = ALL graphs

    # Dump state to json
    nodes = []
    graphs = []

    if graph == None:
        nodes = helper.inToOutNodes(lib.nodeList)
        for k,g in lib.graphList.iteritems():
            graphs.extend(helper.inToOutLinks(g.get_data()))
    else:
        graphs.extend(helper.inToOutLinks(graph.get_data()))
        g = graph.get_data()
        graph_nodelist = {}
        for source, destinations in g.iteritems():
            graph_nodelist[source] = lib.nodeList[source]
            for destination, properties in destinations.iteritems():
                graph_nodelist[destination] = lib.nodeList[destination]

        nodes = helper.inToOutNodes(graph_nodelist)

    # Nodes and Links converted from IR to json
    logging.debug("nodes:"+str(nodes))
    logging.debug("links:"+str(graphs))

    # Dump json to file
    with open('./proc/state.json', 'w') as outfile:
         json.dump({"nodes":nodes, "lastNodeId": len(nodes)-1, "links": graphs}, outfile)

    gui.output()

#
#  ████████╗ ██████╗     ██████╗  ██████╗
#  ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔═══██╗
#     ██║   ██║   ██║    ██║  ██║██║   ██║
#     ██║   ██║   ██║    ██║  ██║██║   ██║
#     ██║   ╚██████╔╝    ██████╔╝╚██████╔╝
#     ╚═╝    ╚═════╝     ╚═════╝  ╚═════╝
#
# Add default values for nodes in gui

def ginput(*args):
    if len(args)==2:
        #########################################
        try:
            f = open(args[1],'r')
        except Exception, e:
            logging.error("File Not Found.")
            gexit()
            
        lines = f.readlines()
        f.close()
        finalEdgeList = dict()
        nodes = {}
        number_of_nodes = len(lib.nodeList)
    
        # new_node_class = type('facebook', (lib.Node,), dict(((el,None) for i,el in enumerate(['weight'])),__init__=lib.node_init, print_data=lambda self:lib.Node.print_data(self), get_data= lambda self: lib.Node().get_data(self), mapping=dict((i,el) for i,el in enumerate(['name','artist','match','playcount']))))
        # func_map['facebook'] = new_node_class
    
        for i,line in enumerate(lines):
            properties = {}
            edgeF, edgeT = [int(x) for x in line.split()]
            #print edgeF,edgeT
            properties["__connector__"] = "->"
            if edgeF not in lib.nodeList.keys():
                lib.nodeList[edgeF] = func_map[args[0]](id_generator(), id_generator())
                lib.nodeList[edgeF].id = edgeF
            if edgeT not in lib.nodeList.keys():
                lib.nodeList[edgeT] = func_map[args[0]](id_generator(), id_generator())
                lib.nodeList[edgeT].id = edgeT
            try:
                finalEdgeList[edgeF][edgeT] = properties
            except KeyError:
                finalEdgeList[edgeF] = {edgeT : properties}
        
        lib.graphList[len(lib.graphList)+1] = lib.Graph(finalEdgeList)
        print "One graph and",len(lib.nodeList)-number_of_nodes,"nodes touched."

        
        #########################################
    elif len(args)==0:
        input = json.loads(gui.input())
        lib.graphList[len(lib.graphList)+1] = lib.Graph(helper.outToInLinks(input['links']))

        # Unfortunately, we have to decide whether to create a template node class or one for EVERY node in input. This one does the former.
        template_node_class = type("template", (lib.Node,), dict(((k,None) for k,v in input["nodes"][0].iteritems()),__init__=lib.node_init, print_data=lambda self:lib.Node.print_data(self), get_data= lambda self: lib.Node().get_data(self), mapping=dict((i,el) for i,el in enumerate(input["nodes"][0]))))
    
        for k in input['nodes']:
           lib.nodeList[k["id"]] = (template_node_class(k));

        print "One graph and",len(input["nodes"]),"nodes touched."
        logging.debug(lib.nodeList)
        logging.debug(lib.graphList)
        logging.debug(helper.outToInNodes(input['nodes']))
        logging.debug(helper.outToInLinks(input['links']))
    else:
        logging.error("Input takes 0 arguments for input from user, or 3 for input from file <node_type, file>.")
        gexit()

#
#  ████████╗ ██████╗     ██████╗  ██████╗
#  ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔═══██╗
#     ██║   ██║   ██║    ██║  ██║██║   ██║
#     ██║   ██║   ██║    ██║  ██║██║   ██║
#     ██║   ╚██████╔╝    ██████╔╝╚██████╔╝
#     ╚═╝    ╚═════╝     ╚═════╝  ╚═════╝
#
#   Graceful Cleanup
#


def gexit():
    sys.exit(0)

def get_data(e):
    ''' Used for debugging'''
    logging.debug(e.get_data())

func_map = {'input' : ginput, 'output' : goutput,  'print' : gprint, 'strlen' : strlen, 'exit': gexit, 'get_data': get_data}

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
    evaluateAST(p[0])

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
    '''graph-dec : GRAPH ID HAS GRAPHTYPE CURLBEGIN edgelist CURLEND
                 | GRAPH ID HAS GRAPHTYPE CURLBEGIN edgelist CURLEND ON idOrAlphanum '''

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
    evaluateAST(p[0])

def p_compoundstatement(p):
    '''statement : compoundstatement'''
    p[0]=p[1]

def p_compoundstatementdef(p):
    '''compoundstatement : CURLBEGIN statementlist CURLEND
                         | CURLBEGIN CURLEND '''
    if len(p)==4:
       p[0] = ast.ASTNode()
       p[0].type = 'compoundstatement'
       p[0].children.append(p[2])
    else:
        p[0]=None

######### function def #########################

def p_funcdec(p):
    '''funcdec : func'''
    p[0] = p[1]

def p_func(p):
    '''func : DEF parameters IMPLY ID compoundstatement IMPLY returnarguments'''
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
    '''returnset : idOrAlphanum
                | idOrAlphanum COMMA returnset'''

    logging.debug("returnset")

    arglistNode = ast.ASTNode()
    arglistNode.type = "returnset"

    arglistNode.children.append(p[1])

    if len(p) > 2:
        arglistNode.children.extend(p[3].children)
    p[0] = arglistNode

######################################################################

#
#  ████████╗ ██████╗     ██████╗  ██████╗
#  ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔═══██╗
#     ██║   ██║   ██║    ██║  ██║██║   ██║
#     ██║   ██║   ██║    ██║  ██║██║   ██║
#     ██║   ╚██████╔╝    ██████╔╝╚██████╔╝
#     ╚═╝    ╚═════╝     ╚═════╝  ╚═════╝
#
#   Handle multiple statements
#

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
##    logging.debug(ast.printTree(p[0]))


def p_statement(p):
    '''statement : expressionstatement
                 | iterationstatement
				 | selectionstatement'''

    logging.debug("statement")

    p[0]=p[1]

def p_edgeexpression(p):
    '''edgeaddition : ID '+' idOrAlphanum CONNECTOR idOrAlphanum'''
    logging.debug("-------In edgeaddition-------")
    node = ast.ASTNode()
    node.type = "addedge"
    node.children.append(p[1])
    node.children.append(p[3])
    node.children.append(p[4])
    node.children.append(p[5])
    #print helper.ids[p[2]].get_list()
    p[0] = node

def p_node_removal_expression(p):
    '''noderemoval : ID '-' nodeLookup'''
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
    else:
        node.children.append(p[1])
        node.children.append(p[3])
    p[0] = node


def p_iterationstatement(p):
    '''iterationstatement : WHILE LPAREN expression RPAREN statement
                          | FOR LPAREN statement expression ';' statement RPAREN CURLBEGIN statement CURLEND
                          | FOREACH LPAREN ID IN ID RPAREN CURLBEGIN statementlist CURLEND'''

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
                            | ID '=' callchain
                            | ID '=' nodeLookup
                            | ID '=' SQRBEGIN values SQREND
                            | ID '=' SQRBEGIN SQREND
                            | ID '=' ID SQRBEGIN SQREND
                            | ID '=' ID SQRBEGIN idOrAlphanum SQREND
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

# TODO - add grammar for logical OR - symbol waw giving error - NEHA.
def p_expression_logicalop(p):
    '''expression : expression LOGAND expression'''
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

def p_expression_string(p):
    '''expression : STRING'''
    logging.debug("p_expressionString")
    termNode = ast.ASTNode()
    termNode.type = "terminal"
    termNode.value = str(p[1][1:-1])
    p[0] = termNode
    logging.debug(p[0].type)

def p_expression_number(p):
    '''expression : NUMBER'''
    logging.debug("p_expressionNumber")
    termNode = ast.ASTNode()
    termNode.type = "terminal"
    if '.' in p[1]:
        termNode.value = float(p[1])
    else:
        termNode.value = int(p[1])
    p[0] = termNode
    logging.debug(p[0].type)

def p_expression_name(p):
    '''expression : ID'''
    try:
        logging.debug("p_expressionId")
        node = ast.ASTNode()
        node.type = "id"
        node.children.append(p[1])
        p[0]=node
    except LookupError:
        logging.error(str("Undefined name '%s'" % p[1]))
        p[0] = 0

#################################

def p_callchain(p):
    '''callchain : call 
                 | call DOT callchain'''
        
    node = ast.ASTNode()
    node.type = "callchain"
    node.children.append(p[1])
    node.chain_next = None
    if len(p)>2:
        node.chain_next = p[3]
    p[0] = node

def p_call(p):
    '''call : ID LPAREN arglist RPAREN
            | ID DOT ID LPAREN arglist RPAREN
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
            child = ast.ASTNode()
            child.type = 'arglist'
            child.value = p[5]
            node.children.append(child)
    else:
        node.children.append(p[1])
        if len(p) == 5:
            logging.debug("****func_arg****")
            child = ast.ASTNode()
            child.type = 'arglist'
            child.value = p[3]
            node.children.append(child)  #actual arguments passed to function
        else:
            node.children.append(None)  #No arguments passed

    p[0] = node

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
    termNode.value = int(p[1])
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
    
def evaluateAST(a):

    global ids

    if(isinstance(a,basestring)):
        return a

    if(isinstance(a,int)):
        return a

    if(isinstance(a,float)):
        return a

    if(isinstance(a,list)):
        ret = []
        for e in a:
            val = evaluateAST(e)
            if isinstance(val, ast.ASTNode):
                ret.append(evaluateAST(e).value)
            else:
                ret.append(val)
        return ret

    logging.debug("Evaluating type: "+str(a.type))

    if(a.type =="statementlist"):
        a.value = []
        logging.debug('Evaluating a list of statements')
        for e in a.children:
            logging.debug('Evaluating a statement in it...')
            evaluateAST(e)
        return a

    if(a.type == "terminal"):
        logging.debug("Terminal value: "+str(a.value))
        return a

    # if(a.type == "values"):
    #     logging.debug("Terminal value: "+str(a.value))
        # return a

    if(a.type == "edgelist"):
        a.value = {}
        child_edge_list = {}
        child_edge_list_attr = {}
        child_edge_list_attr["__connector__"] = a.children[1]
        child_edge_list[a.children[2].value] = child_edge_list_attr
        a.value[a.children[0].value] = child_edge_list

        if len(a.children) != 3:
            if a.children[3] != None:
                for i,e in enumerate(evaluateAST(a.children[3]).value):
                    child_edge_list_attr[i] = e

        if len(a.children) == 5:
            for k,v in evaluateAST(a.children[4]).iteritems():
                if k in a.value.keys():
                    for k1,v1 in v.iteritems():
                        a.value[k][k1] = v1
                a.value[k] = v
        return a.value

    if(a.type == "arglist" or a.type == "returnset"):
        logging.debug("------argList | returnset-----")
        a.value = []

        for e in a.children:
            a.value.append(evaluateAST(e).value)
        return a

    if(a.type == "plus"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=evaluateAST(a.children[0]).value+evaluateAST(a.children[1]).value;
        return node

    if(a.type == "minus"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=evaluateAST(a.children[0]).value-evaluateAST(a.children[1]).value;
        return node

    if(a.type == "multiply"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=evaluateAST(a.children[0]).value*evaluateAST(a.children[1]).value;
        return node

    if(a.type == "divide"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=evaluateAST(a.children[0]).value/evaluateAST(a.children[1]).value;
        return node

    if(a.type == "less"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=evaluateAST(a.children[0]).value<evaluateAST(a.children[1]).value;
        return node

    if(a.type == "greater"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=evaluateAST(a.children[0]).value>evaluateAST(a.children[1]).value;
        return node

    if(a.type == "greaterequal"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=evaluateAST(a.children[0]).value>=evaluateAST(a.children[1]).value;
        return node

    if(a.type == "lessequal"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=evaluateAST(a.children[0]).value<=evaluateAST(a.children[1]).value;
        return node

    if(a.type == "equal"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=evaluateAST(a.children[0]).value==evaluateAST(a.children[1]).value;
        return node

    if(a.type == "nequal"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=evaluateAST(a.children[0]).value!=evaluateAST(a.children[1]).value;
        return node

    if(a.type == "land"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=(evaluateAST(a.children[0]).value)and(evaluateAST(a.children[1]).value);
        return node

    if(a.type == "lor"):
        node=ast.ASTNode()
        node.type="terminal"
        node.value=(evaluateAST(a.children[0]).value)or(evaluateAST(a.children[1]).value);
        return node

    if(a.type == "assignment"):
        logging.debug(a.children[0])
        logging.debug(a.children[1])
        helper.ids[a.children[0]]= evaluateAST(a.children[1]).value
        logging.info('Assigned '+str(helper.ids[a.children[0]])+' to '+str(a.children[0])+' of type '+str(type(helper.ids[a.children[0]])))
        return

    if(a.type == "addedge"):
        logging.debug("------argEdge-----")
        curr =  helper.ids[a.children[0]].get_data()
        shadow = helper.ids[a.children[0]].get_shadow()
        if a.children[1].value in curr.keys():
            curr[a.children[1].value][a.children[3].value]={"__connector__":a.children[2]}
        else:
            curr[a.children[1].value] = {a.children[3].value : {"__connector__":a.children[2]}}
        try:
            shadow[a.children[3].value][a.children[1].value] = None
        except KeyError, e:
            shadow[a.children[3].value] = { a.children[1].value : None }
        
        helper.ids[a.children[0]].edgeList=curr
        return

    if(a.type == "removenode"):
        logging.debug("------noderemoval-----")
        links =  helper.ids[a.children[0]].get_data()
        shadow = helper.ids[a.children[0]].get_shadow()

        nodes =  evaluateAST(a.children[1]).value
        for node in nodes:
            node_id_to_be_removed = node.id
            pop_from_shadow = []
            if node_id_to_be_removed in links:
                pop_from_shadow = links[node_id_to_be_removed].keys()
            links.pop(node_id_to_be_removed, None)
            if node_id_to_be_removed in shadow:
                pop_from_links = [] 
                for destination in shadow[node_id_to_be_removed].keys():
                    links[destination].pop(node_id_to_be_removed, None)
                    if len(links[destination]) == 0:
                        pop_from_links.append(destination)
    
                for p in pop_from_links:
                    links.pop(p, None)
                pop_cleanup = []
                for p in pop_from_shadow:
                    shadow[p].pop(node_id_to_be_removed, None)
                    if len(shadow[p]) == 0:
                        pop_cleanup.append(p)
                for p in pop_cleanup:
                    shadow.pop(p, None)
                shadow.pop(node_id_to_be_removed, None)
        helper.ids[a.children[0]].edgeList=links
        helper.ids[a.children[0]].shadowEdgeList=shadow
        return

    if(a.type == "lookupnode"):
        try:
            result = ast.ASTNode()
            result.type = "terminal"
            nodeSet = []
            result.value = nodeSet
            logging.debug("------lookupnode-----")
            key =  a.children[0]
            value = evaluateAST(a.children[1]).value
            if key in ["id","ID"]:
                nodeSet.append(lib.nodeList[value])
                return result
            key = key.value
            for id,node in lib.nodeList.iteritems():
                data = node.get_data()
                if key in data: 
                    if data[key] == value:
                        nodeSet.append(node)
            result.value = nodeSet
            return result
        except KeyError, e:
            logging.critical("Node not found")
            gexit()

    if(a.type == "member_funccall"):
        logging.debug('-----eval: member func_call----')
        
        node = ast.ASTNode()
        node.type = "terminal"
        try:
            if isinstance(helper.ids[a.children[0]],ast.ASTNode):
                if len(a.children) <= 2:
                    node.value = getattr(lib.modified_list(evaluateAST(helper.ids[a.children[0]])),a.children[1])()
                else: 
                    node.value = getattr(helper.ids[a.children[0]].value,a.children[1])(evaluateAST(a.children[2].value).value)
            else:
                if len(a.children) <= 2:
                    try:
                        node.value = getattr(helper.ids[a.children[0]],a.children[1].children[0])()
                    except Exception, e:
                        node.value = getattr(helper.ids[a.children[0]],a.children[1])()
                    # node.value = getattr(helper.ids[a.children[0]],a.children[1])()
                else:
                    node.value = getattr(helper.ids[a.children[0]],a.children[1])(*evaluateAST(a.children[2].value).value)

            return node
        except KeyError, e:
            logging.error("Unknown variable"+str(a.children[0]))
            gexit()

        logging.info('Assigned '+str(helper.ids[a.children[0]])+' to '+str(a.children[0]))
        return

    if(a.type == "listassignment"):
        logging.debug("--- list assignment ---")
        listValues = []

        if len(a.children[1].children) == 0:
            temp = evaluateAST(a.children[1]).value
            for t in temp:

                if t.type == "terminal":
                    listValues.append(t) 

                if t.type == "id" and isinstance(evaluateAST(t).value,ast.ASTNode):
                    if isinstance(evaluateAST(t).value.value,list):
                        ttemp = evaluateAST(t).value.value
                        innerList = []
                        for tt in ttemp:
                            innerList.append(tt.value)
                        n = ast.ASTNode()
                        n.type = "terminal"
                        n.value = innerList
                        listValues.append(n)

                elif t.type == "id":
                    n = ast.ASTNode()
                    n.type = "terminal"
                    n.value = evaluateAST(t).value
                    listValues.append(n)

        nlistValues = lib.modified_list(listValues)
        node = ast.ASTNode()
        node.type = "list"

        node.value = nlistValues
        helper.ids[a.children[0]] = node

        return


    if(a.type == 'list'):
        logging.debug("List value: "+str(a.value))
        return evaluateAST(a.value)

    if(a.type == 'indexassignment'):
        logging.debug("--- index assignment ---")
        value = evaluateAST(helper.ids[evaluateAST(a.children[1]).value])[evaluateAST(a.children[2]).value]
        if isinstance(value,list):
            node = ast.ASTNode()
            node.type = "list"
            nlistValues = lib.modified_list(value)
            node.value = nlistValues
            helper.ids[a.children[0]] = node
        else:
            helper.ids[a.children[0]] = value
        return

    if(a.type == 'rindexassignment'):
        logging.debug("--- rindex assignment ---")

        listValues = evaluateAST(helper.ids[a.children[0]])
        if evaluateAST(a.children[1]).value == len(listValues):
            listValues.append(evaluateAST(a.children[2]).value)
        else:
            listValues[evaluateAST(a.children[1]).value] = evaluateAST(a.children[2]).value
        
        nlistValues = lib.modified_list(listValues)
        node = ast.ASTNode()
        node.type = "list"
        node.value = nlistValues
        helper.ids[a.children[0]] = node

        return


    if(a.type == "addedge"):
           logging.debug("------argEdge-----")
           curr =  helper.ids[a.children[0]].get_data()
           if a.children[1].value in curr.keys():
               curr[a.children[1].value][a.children[3].value]={"__connector__":a.children[2]}
           else:
               curr[a.children[1].value] = {a.children[3].value : {"__connector__":a.children[2]}}
           helper.ids[a.children[0]].edgelist=curr
           return

    if(a.type == "callchain"):
        logging.debug('-----eval: callchain----')
        ret = evaluateAST(a.children[0])
        if a.chain_next != None:
            node = ast.ASTNode()
            node.type = "member_funccall"
            helper.ids["__chaining_buffer__"] = ret.value
            node.children.append("__chaining_buffer__")                #object
            node.children.append(a.chain_next.children[0])      #member function
            if len(a.chain_next.children) >1:
                child = ast.ASTNode()
                child.type = 'arglist'
                child.value = a.chain_next.children[1]
                node.children.append(child)
            try:
                return evaluateAST(node)
            except Exception, e:
                raise                        
        return ret

    if(a.type == "funccall"):
        logging.debug('-----eval: call----')

        node=ast.ASTNode()
        node.type="terminal"
        args = []
        # built in
        func = ast.ASTNode()
        func.type = "funccall"
        try:
            try:
                logging.debug("****inbuilt****")
                func.children.append(func_map[a.children[0]])
                if(len(a.children)> 1):
                    logging.debug("****func_arg****")
                    func.children.append(a.children[1])
                else:
                    func.children.append(None)

            except KeyError:
                # User-defined
                logging.debug("****userdefined****")
                func.children.append(function[a.children[0]].children[0])    #statements
                func.children.append(function[a.children[0]].children[1])    #arguments
                func.children.append(function[a.children[0]].children[2])    #returnargs
                if len(a.children) >1:
                    logging.debug("****func_arg****")
                    func.children.append(a.children[1])  #actual arguments passed to function
                else:
                    func.children.append(None)  #No arguments passed
        except KeyError, e:
            logging.error("Function not found.")
            logging.error("Offending function: "+a.children[0])
            gexit()

        if isinstance(func.children[0],ast.ASTNode):
            #Packing
            #scope_in() #Commented because it should now be handled by scoping in and out by compoundstatement evaluation
            #End packing
            
            numArgs = len(func.children[1].children)
            
            if func.children[1].children[0] == None:
                numArgs = 0
            
            for i in range(0,numArgs):
                helper.ids[func.children[1].children[i]]= evaluateAST(func.children[3].value).value[i]
                logging.info('Assigned '+str(func.children[1].children[i])+' to '+str(helper.ids[func.children[1].children[i]])+' inside funccall')
            logging.debug("MODIFIED scope: Before call:",helper.ids)
            evaluateAST(func.children[0])
            node.value = []

            if func.children[2].children[0] != None:       
                for ret in func.children[2].children:
                    node.value.append(evaluateAST(ret))
            
            #Unpacking
            #scope_out() #Refer above at scope_in() call
            #End unpacking
            logging.debug("MODIFIED scope: After call:",helper.ids)
        else:    
            if func.children[1] != None:
                x = evaluateAST(func.children[1].value).value
                node.value=func.children[0](*x)
            else:
                node.value=func.children[0]()
            try:
                if func.children[0].__bases__[0].__name__ in ["Node"]:
                    lib.nodeList[lib.globalLastNodeIDVal] = node.value
            except Exception, e:
                pass

        return node

        
    if (a.type == 'compoundstatement'):
        logging.debug('Evaluating compound statement...')
        helper.scope_in()
        evaluateAST(a.children[0])
        helper.scope_out()
        
        # #User-defined functions
        # if len(a.children):
        #     # Number of formal arguments - len(a.children[1].children)
        #     # Fist argument - a.children[1].children[0]
        #     # Number of actual arguments - len(evaluateAST(a.children[3].value).value)
        #     # First argument - evaluateAST(a.children[3].value).value[0]

        #     # if a.children[1].children[0] == None:
        #     #     print "No formal arguments"

        #     # if a.children[3] == None:
        #     #     print "No actual arguments"

        #     if (a.children[1].children[0] == None and a.children[3] != None) or (a.children[1].children[0] != None and a.children[3] == None):
        #         print "Error! - Number of arguments in function call does not match"
        #         sys.exit(0)

        #     elif a.children[1].children[0] != None and a.children[3] != None and len(a.children[1].children) != len(evaluateAST(a.children[3].value).value):
        #         print "Error! - Number of arguments in function call does not match"
        #         sys.exit(0)

        #     global funcIds

        #     numArgs = len(a.children[1].children)
        #     for i in range(0,numArgs):
        #         funchelper.ids[a.children[1].children[i]]= evaluateAST(a.children[3].value).value[i]
        #         logging.info('Assigned '+str(a.children[1].children[i])+' to '+str(funchelper.ids[a.children[1].children[i]])+' inside funccall')


        #     node = ast.ASTNode()
        #     node.type = 'terminal'
        #     node.value = evaluateAST(a.children[0])

        #     funcIds=dict()

        #     return node

        # if len(a.children)>1 and len(a.children)!=3:
        #     print "outer if"
        #     if(a.children[1].type == "arglist"):
        #         print "inner if"
        #         node=ast.ASTNode()
        #         node.type="terminal"
        #         args = []
        #         node.value=a.children[0](*evaluateAST(a.children[1].value).value)
        #         return node
        #     else:
        #         print "inner else"
        #         node=ast.ASTNode()
        #         node.type="terminal"
        #         node.value=a.children[0](evaluateAST(a.children[1]))
        #         return node
        # else:
        #     print "outer else"
        #     node=ast.ASTNode()
        #     node.type="terminal"
        #     node.value=evaluateAST(a.children[0])
        #     return node
    
    if(a.type == "sequence"):
        return evaluateAST(a.children[0])

    if(a.type == "id"):
        node=ast.ASTNode()
        node.type="terminal"
        try:
            if a.children[0] in helper.ids:
                node.value = helper.ids[a.children[0]]
            else:
                node.value=helper.ids[a.children[0]]
        except KeyError, e:
            logging.critical("Unknown variable: '"+str(a.children[0])+"'")
            sys.exit(-1)
        return node

    if(a.type == "node-dec"):
        logging.debug('-----eval: node-dec----')
        new_node_class = type(a.children[0].value, (lib.Node,), dict(((el,None) for i,el in enumerate(a.children[1].value)),__init__=lib.node_init, print_data=lambda self:lib.Node.print_data(self), get_data= lambda self: lib.Node().get_data(self), mapping=dict((i,el) for i,el in enumerate(a.children[1].value))))

        func_map[a.children[0].value] = new_node_class
        return

    if(a.type == "graph-dec"):
        logging.debug('-----eval: graph-dec----')

        new_graph = lib.Graph(evaluateAST(a.children[3]), evaluateAST(a.children[1]), evaluateAST(a.children[2]))
        lib.graphList[lib.globalLastGraphIDVal] = new_graph

        for source, destinations in new_graph.get_data().iteritems():
            source = int(source)
            if source not in lib.nodeList.keys():
                logging.error("Source Node #"+str(source)+" not found.")
                sys.exit(0)
            for destination, properties in destinations.iteritems():
                destination = int(destination)
                if destination not in lib.nodeList.keys():
                    logging.error("Destination Node #"+str(destination)+"not found.")
                    sys.exit(0)

        helper.ids[a.children[0].value] = new_graph

        # new_graph.print_data()
        return

    if(a.type == "function-dec"):
        function[a.children[0]]=a.children[1]

    #while loop
    if(a.type == 'while'):
        #TODO - change condition to True/False --Pooja
        logging.debug("evaluateAST of while")
        logging.debug("*********************")
        logging.debug(evaluateAST(a.children[0]))
        logging.debug("*********************")
        while (evaluateAST(a.children[0]).value != 0):
            evaluateAST(a.children[1])

    if(a.type == "if"):
        logging.debug("evaluateAST of if")
        logging.debug("*********************")
        logging.debug(evaluateAST(a.children[0]))
        logging.debug("*********************")
        if(evaluateAST(a.children[0]).value):
            evaluateAST(a.children[1])
        elif(len(a.children)>2):
            evaluateAST(a.children[2])

    if(a.type == 'for'):
        logging.debug("evaluateAST of for")
        logging.debug("*********************")
        logging.debug(evaluateAST(a.children[0]))
        logging.debug("*********************")

        evaluateAST(a.children[0]); # Initialization

        while (evaluateAST(a.children[1]).value != 0): # Check condition
            evaluateAST(a.children[3]) # Evaluate statement
            evaluateAST(a.children[2]) # Update loop statement
            
    if(a.type == 'foreach'):
        logging.debug("evaluateAST of foreach")
        logging.debug("*********************")
        logging.debug(evaluateAST(a.children[0]))
        logging.debug("*********************")
        iterVar = 0
        
        helper.scope_in()
        
        while iterVar < len(evaluateAST(helper.ids[a.children[1]])):
            logging.debug(helper.ids[a.children[1]])
            helper.ids[a.children[0]] = evaluateAST(helper.ids[a.children[1]])[iterVar] #Update iterVariable
            logging.debug('Evaluating foreach statement')
            evaluateAST(a.children[2]) #evaluate child compoundstatement
            iterVar += 1 #increment index of iterVar
        
        helper.scope_out()
        

while True:
    try:
        s = raw_input('graphene> ')
    except EOFError:
        break
    if not s: continue
    if (not s.lower() == "exit"):
        result = parser.parse(s)
    else:
        sys.exit()
