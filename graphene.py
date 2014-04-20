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

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from vendors import gui

from itertools import chain
import itertools
import sys
import types
import decimal
import json
from lib import grapheneLib as lib
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

ids=lib.modified_dict()
function=dict()

NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)

tokens = ('ID', 'LPAREN', 'DEF', 'IMPLY', 'RPAREN', 'STRING', 'CURLBEGIN', 'CURLEND', 'NUMBER', 'WHITESPACE', 'COMMA', 'NODE', 'EDGE', 'GRAPH','GRAPHTYPE', 'CONNECTOR', 'NEW', 'NEWLINE', 'DOT', 'WHILE', 'HAS', 'ON', 'COLON')
literals = [';', '=', '+', '-', '*', '/']

RESERVED = {
  "def": "DEF",
  "if": "IF",
  "return": "RETURN",
  "while": "WHILE",
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
     
t_DOT = r'\.'

t_COLON = r':'

t_LPAREN = r'\('

t_RPAREN = r'\)'
    
t_STRING = r'\"[a-zA-Z\ 0-9]*\"'

t_COMMA = r','

t_NODE = r'Node'

t_EDGE = r'Edge'

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
    t.type = "NEWLINE"
    if t.lexer.paren_count == 0:
        return t

def t_WHITESPACE(t):
    r'\s+'
    t.lexpos += len(t.value)

def t_NUMBER(t):
    r"""(\d+(\.\d*)?|\.\d+)([eE][-+]? \d+)?"""
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
    logging.error("Error in input")
    logging.error(p.value)
    sys.exit()

def strlen(node):
    print "Count:", len(G)

def myprint(*node):
    logging.debug('******print******')

    for e in node:

        if type(e).__bases__[0].__name__ in ["Node"]:
            print "Node has"
            e.print_data();
        elif isinstance(e, lib.Graph):
            print "Graph has"
            e.print_data();
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

def goutput(graph_name):
    # Displays graph visually
    return

def goutput(graph_name, graph_nodes):
    # Displays graph on console
    return

def goutput():
    # Prints state to D3
    # Note: state = ALL graphs
    
    # Dump state to json
    nodes = []
    for n in lib.nodeList:
        nodes.append(n.get_prop())

    graphs = []
    for g in lib.graphList:
        graphs.extend(g.get_list()[0])

    # Nodes and Links converted from IR to json 
    logging.debug("nodes:", str(nodes))
    logging.debug("links:", str(graphs))

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

def ginput():
    input = gui.input()
   
    input = json.loads(input)

    lib.graphList.append(lib.Graph(input['links']))

    for k in input['nodes']:
       lib.nodeList.insert(k["id"],lib.Node(k));

   # pretty prints json response
    logging.debug(lib.nodeList)
    logging.debug(lib.graphList)
    logging.debug(outToInNodes(input['nodes']))
    logging.debug(outToInLinks(input['links']))

    print json.dumps(input, indent=4, sort_keys=True)


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

func_map = {'input' : ginput, 'output' : goutput,  'print' : myprint, 'strlen' : strlen, 'exit': gexit}  
    
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
    '''node-dec : NODE ID HAS keylist'''
    #Note - keylist implies parameters

    logging.debug("----- Node declaration -----")

    node = ast.ASTNode()
    node.type = 'node-dec'

    child1 = ast.ASTNode()
    child1.value = p[2]
    child2 = ast.ASTNode()
    child2.value = p[4]

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
       p[0] = p[2]
    else:
        p[0]=[]

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

def p_statementlist(p):
    '''statementlist : statement
                     | statement statementlist'''

    node = ast.ASTNode();
    node.type = "statementlist";
    node.children.append(p[1]);
    if len(p)==3:
        node.children.append(p[2]);
    p[0]=node
    
    logging.debug(p[0].type)
##    logging.debug(ast.printTree(p[0]))
    

def p_statement(p):
    '''statement : expressionstatement
                 | iterationstatement'''
    
    logging.debug("statement")
    
    p[0]=p[1]


def p_iterationstatement(p):
    '''iterationstatement : WHILE LPAREN expression RPAREN statement'''

    Node = ast.ASTNode()
    Node.type = 'while'
    Node.children.append(p[3])
    Node.children.append(p[5])
    p[0]=Node

    logging.debug("-------In iterationstatement-------")

def p_expressionstatement(p):
    '''expressionstatement : ';'
                           | completeexpression ';'  '''
    
    logging.debug("expStatement")

    if(not (len(p) == 2)):
        logging.debug("non empty statement")
        p[0] = p[1]
        logging.debug(p[0].type)

def p_expression(p):                       
    '''completeexpression : call
                  | assignmentexpression
                  '''
    logging.debug("expr")
    p[0] = p[1]
    logging.debug(p[0].type)
                  
#removed this we are supporting dynamic typing (can introduce later if required)

##def p_assignmentexpression(p):
##    '''assignmentexpression : Type ID '=' Type '.' new '(' ')'
##                            | Type ID '=' assignmentexpression'''

def p_assignval(p):
    '''assignmentexpression : ID '=' expression
                            | ID '=' call '''
    #ids[p[1]] = p[3]
    node = ast.ASTNode()
    node.type="assignment"
    node.children.append(p[1])
    node.children.append(p[3])
    p[0] = node
    
    logging.debug("-------In assignExpr-------")
    logging.info('assigned '+str(p[1]))
    
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

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN '''
    p[0] = p[2]
    
def p_expression_string(p):
    '''expression : STRING'''
    logging.debug("p_expressionString")
    termNode = ast.ASTNode()
    termNode.type = "terminal"
    termNode.value = p[1][1:-1]
    p[0] = termNode
    logging.debug(p[0].type)

def p_expression_number(p):
    '''expression : NUMBER'''
    logging.debug("p_expressionNumber")
    termNode = ast.ASTNode()
    termNode.type = "terminal"
    termNode.value = p[1]
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



def p_call(p):
    '''call : ID LPAREN arglist RPAREN
            | ID DOT ID LPAREN arglist RPAREN 
            | ID DOT ID LPAREN RPAREN
            | ID LPAREN RPAREN '''
    
    logging.debug("call")
    for x in p:
        logging.debug(x)
        
    logging.debug("p_call")
    node = ast.ASTNode()
    node.type = "funccall"
    
    try:
        if(len(p) == 7):
            node.children.append(func_map[[p[1]][p[3]]])
            child = ast.ASTNode()
            child.type = 'arglist'
            child.value = p[5]
            node.children.append(child)
        elif(len(p) == 6):
            node.children.append(func_map[p[1]][p[3]])
        else:
            try:
                logging.debug("****inbuilt****")
                node.children.append(func_map[p[1]])
            
            except KeyError:
                logging.debug("****userdefined****")
                node.children.append(function[p[1]].children[0])    #statements
                node.children.append(function[p[1]].children[1])    #arguments
                node.children.append(function[p[1]].children[2])    #returnargs
                if len(p) == 5:
                    child = ast.ASTNode()
                    child.type = 'arglist'
                    child.value = p[3]
                    node.children.append(child)  #actual arguments passed to function
                else:
                    node.children.append(None)  #No arguments passed
                
                
            if(len(p) == 5):
                logging.debug("****func_arg****")
                child = ast.ASTNode()
                child.type = 'arglist'
                child.value = p[3]
                node.children.append(child)
        p[0] = node

    except:
        logging.error("Function not found. Please replace developer")
        logging.debug(p[0])

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
    termNode.value = p[1][1:-1]
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
        # print node
        finalStr.append({'id:': node, 'name': nodeL[node]})
    return finalStr

def inToOutLinks(sources):
    final = []
    for source in sources.keys():
        # print source
        for target in sources[source]:
           final.append({'source': source, 'target' :target['target'], 'left':True, 'right':True, 'weight':target['weight']})

    return final

def evaluateAST(a):
    global ids
    if(isinstance(a,basestring)):
        return a

    if(isinstance(a,decimal.Decimal)):
        return a

    if(isinstance(a,list)):
        ret = []
        for e in a:
            ret.append(evaluateAST(e).value)
        return ret

    logging.debug("Evaluating type: "+str(a.type))

    if(a.type =="statementlist"):
        a.value = []
        for e in a.children:
            evaluateAST(e)
        return a

    if(a.type == "terminal"):
        logging.debug("Terminal value: "+str(a.value))
        return a
    
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

    if(a.type == "assignment"):
        logging.debug(a.children[0])
        logging.debug(a.children[1])
        ids[a.children[0]]= evaluateAST(a.children[1]).value
        logging.info('Assigned '+str(ids[a.children[0]])+' to '+str(a.children[0]))
        return 
        
    if(a.type == "funccall"):
        logging.debug('-----eval: call----')

        # print "@@@@@@@@@@@@@@@@",a.children[0]
        # statementlist
        # function-pars
        # return-args

        #inbuilt functions - tested with print()
        node=ast.ASTNode()
        node.type="terminal"
        args = []
        if isinstance(a.children[0],ast.ASTNode):
            ids = lib.modified_dict({"__global__": ids})
            numArgs = len(a.children[1].children)
            for i in range(0,numArgs):
                ids[a.children[1].children[i]]= evaluateAST(a.children[3].value).value[i]
                logging.info('Assigned '+str(a.children[1].children[i])+' to '+str(ids[a.children[1].children[i]])+' inside funccall')
            logging.debug("MODIFIED scope:",ids)
            evaluateAST(a.children[0])
            node.value = []
            for ret in a.children[2].children:
                node.value.append(evaluateAST(ret))
            ids = ids["__global__"]
        else:
            if len(a.children) > 1:
                node.value=a.children[0](*evaluateAST(a.children[1].value).value)
            else:
                node.value=a.children[0]()
        return node

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
        #         funcIds[a.children[1].children[i]]= evaluateAST(a.children[3].value).value[i]
        #         logging.info('Assigned '+str(a.children[1].children[i])+' to '+str(funcIds[a.children[1].children[i]])+' inside funccall')


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
            if a.children[0] in ids:
                node.value = ids[a.children[0]]
            else:
                node.value=ids[a.children[0]]
        except KeyError, e:
            logging.critical("Unknown variable: '"+str(a.children[0])+"'")
            sys.exit(-1)
        return node
    
    if(a.type == "node-dec"):
        logging.debug('-----eval: node-dec----')
        new_node_class = type(a.children[0].value, (lib.Node,), dict(((el,None) for i,el in enumerate(a.children[1].value)),__init__=lib.node_init, print_data=lambda self:lib.Node.print_data(self),mapping=dict((i,el) for i,el in enumerate(a.children[1].value))))
        function[a.children[0].value] = new_node_class
        return

    if(a.type == "graph-dec"):
        logging.debug('-----eval: graph-dec----')
        
        new_graph = lib.Graph(evaluateAST(a.children[1]), evaluateAST(a.children[2]), evaluateAST(a.children[3]))
        ids[a.children[0].value] = new_graph

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
