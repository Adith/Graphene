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
import ast
import logging
# import symboltable

debug = 0
logger = logging.getLogger()
if len(sys.argv) > 1:
    if sys.argv[1] in ['--debug', '-d']:
        logger.setLevel(logging.DEBUG)
    elif sys.argv[1] in ['--info', '-i']:
        logger.setLevel(logging.INFO)

ids=dict()
function=dict()

NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)

tokens = ('ID', 'LPAREN', 'DEF', 'IMPLY', 'RPAREN', 'STRING', 'CURLBEGIN', 'CURLEND', 'NUMBER', 'WHITESPACE', 'COMMA', 'Node', 'Edge', 'Graph', 'new', 'NEWLINE', 'DOT', 'WHILE', 'HAS', 'COLON')
literals = [';', '=', '+', '-', '*', '/']

RESERVED = {
  "def": "DEF",
  "if": "IF",
  "return": "RETURN",
  "while": "WHILE",
  "has": "HAS"
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

t_Node = r'Node'

t_Edge = r'Edge'

t_Graph = r'Graph'

t_new = r'new'

def t_ID(t):
    r'[a-zA-Z\_][a-zA-Z\_0-9]*'
    t.type = RESERVED.get(t.value, "ID")
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
    t.value = decimal.Decimal(t.value)
    return t

def t_error(t):
    print "Syntax error:"
    print "Type: ",t.type
    print "Token: ",t.value
    print "Line: ",t.lineno
    print "Column: ",t.lexpos
    sys.exit()

def p_error(p):
    print "Error in input"
    print p.value
    sys.exit()

def strlen(node):
    print "Count:", len(G)

def myprint(node):
    logging.debug('******print******')
    logging.debug(type(node))
    print node.value
    
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

# ___________           ___
# \__    ___/___     __| _/____  
#   |    | /  _ \   / __ |/  _ \ 
#   |    |(  <_> ) / /_/ (  <_> )
#   |____| \____/  \____ |\____/ 
#                       \/       
#
#  Add default values for nodes in gui
#

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
#   To Do:
#   Graceful Cleanup
#


def gexit():
    sys.exit(0)

func_map = {'input' : ginput, 'output' : goutput,  'print' : myprint, 'strlen' : strlen, 'exit': gexit}  
    
lexer = lex.lex();

####################### TO BE MODIFIED ##############################

def p_program(p):
    '''program : declarationlist'''
    p[0]=p[1]
    
def p_declarations(p):
    '''declarationlist : declaration declarationlist
                       | declaration'''
    p[0]=p[1]
        
def p_declaration(p):
    '''declaration : funcdec
                   | vardec'''
    p[0]= p[1]
    evaluateAST(p[0])

def p_vardec(p):
    '''vardec : node'''
    logging.debug("----- variable declaration ------")

    p[0] = p[1]
    

def p_node(p):
    '''node : ID HAS keylist'''
    #Note - keylist implies parameters

    logging.debug("Node declaration")

    node = ast.ASTNode()
    node.type = 'node-dec'
    node.children.append(p[1])
    node.children.append(p[3])
    p[0] = node


def p_keylist(p):
    '''keylist : idOrAlphanum COLON idOrAlphanum
               | idOrAlphanum COLON idOrAlphanum COMMA keylist'''

    logging.debug("Node declaration keylist")

    p[0] = {}
    p[0][p[1]] = p[3]
    if len(p) == 5:
        if p[1] in p[5].keys():
            logging.critical("Same property name for node.")
            system.exit(-200)

        for k,v in p[5].items():
            p[0][k] = v


    
def p_decstatement(p):
    '''declaration : statement'''
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

def p_funcdef(p):
    '''funcdec : DEF parameters IMPLY ID compoundstatement'''
    #funcdef : DEF parameters IMPLY ID CURLBEGIN statementlist CURLEND IMPLY returnlist
    #p[0] = ast.Function(None, p[2], tuple(p[3]), (), 0, None, p[5])
    Node = ast.ASTNode()
    Node.type = 'function-dec'
    Node.children.append(p[4])
    Node.children.append(p[5])
    p[0]=Node

def p_parameters(p):
    """parameters : LPAREN RPAREN
                  | LPAREN varargslist RPAREN"""
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]
    
def p_varargslist(p):
    """varargslist : varargslist COMMA ID
                   | ID"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_return(p):
    """returnlist : LPAREN RPAREN
                  | LPAREN varargslist RPAREN"""
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]
        
######################################################################

def p_statementlist(p):
    '''statementlist : statement
                     | statement statementlist'''

    p[0]=p[1]
    
    logging.debug(type(p[0]))
    logging.debug(ast.printTree(p[0]))
    

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
        logging.debug(type(p[0]))

def p_expression(p):                       
    '''completeexpression : call
                  | assignmentexpression
                  '''
    logging.debug("expr")
    p[0] = p[1]
    logging.debug(type(p[0]))
                  
#removed this we are supporting dynamic typing (can introduce later if required)

##def p_assignmentexpression(p):
##    '''assignmentexpression : Type ID '=' Type '.' new '(' ')'
##                            | Type ID '=' assignmentexpression'''

def p_assignval(p):
    '''assignmentexpression : ID '=' expression'''
    #ids[p[1]] = p[3]
    node = ast.ASTNode()
    node.type="assignment"
    node.children.append(p[1])
    node.children.append(p[3])
    p[0] = node
    
    logging.debug("-------In assignExpr-------")
    logging.debug(ast.printTree(p[0]))
    
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
    logging.debug(type(p[0]))

def p_expression_number(p):
    '''expression : NUMBER'''
    logging.debug("p_expressionNumber")
    termNode = ast.ASTNode()
    termNode.type = "terminal"
    termNode.value = p[1]
    p[0] = termNode
    logging.debug(type(p[0]))

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
            node.children.append(func_map[p[1]][p[3]])
            node.children.append(p[5])
            p[0] = node
        elif(len(p) == 6):
            node.children.append(func_map[p[1]][p[3]])
            node.children.append([])
            p[0] = node
        elif(len(p) == 4):
            try:
                logging.debug("****inbuilt****")
                node.children.append(func_map[p[1]])
            except KeyError:
                logging.debug("****Userdefined****")
                node.type="Userdefined"
                node.children.append(function[p[1]])
            p[0] = node

        else:
            logging.debug("****call****")
            node.children.append(func_map[p[1]])
            node.children.append(p[3])
            p[0] = node
    except:
        logging.error("Function not found. Please replace developer")
        logging.debug(type(p[0]))
        
        
##def p_arglist(p):
##    '''arglist : idOrAlphanum
##               | idOrAlphanum COMMA arglist
##               | '''
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
    '''arglist : idOrAlphanum COMMA arglist
               | idOrAlphanum'''
    logging.debug("arglist")
    if len(p) == 4:
        #p[0] = p[1] + [p[3]]
        pass
    else:
        p[0] = p[1]
    logging.debug(type(p[0]))
    
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
    logging.debug(type(p[0]))
    
def p_isString(p):
    ''' idOrAlphanum : STRING '''
                   
    logging.debug("idorstr"+str(len(p)))
    for x in p:
        logging.debug(x)
    logging.debug("p_isString")

    termNode = ast.ASTNode()
    termNode.type = "terminal"
    termNode.value = p[1][1:-1]
    p[0] = termNode
    logging.debug(type(p[0]))

def p_isId(p):
    ''' idOrAlphanum : ID'''
    logging.debug("idorstr"+str(len(p)))
    for x in p:
        logging.debug(x)
    logging.debug("p_isID")
    
    termNode = ast.ASTNode()
    termNode.type = "id"
    termNode.children.append(p[1])
    p[0] = termNode
    logging.debug(type(p[0]))
    
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

def evaluateAST(a):
    
    logging.debug("Evaluating type: "+str(type(a)))
   
    if(a.type == "terminal"):
        logging.debug("Terminal value: "+str(a.value))
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
        logging.debug('-----call----')
        if len(a.children)>1:
            return a.children[0](evaluateAST(a.children[1]))
        else:
            return a.children[0]()

    if(a.type == "Userdefined"):
        logging.debug('-----Userdefined----')
        return evaluateAST(a.children[0])
    
    if(a.type == "sequence"):
        return evaluateAST(a.children[0])
    
    if(a.type == "id"):
        node=ast.ASTNode()
        node.type="terminal"
        try:
            node.value=ids[a.children[0]]
        except KeyError, e:
            logging.critical("Unknown variable: '"+str(a.children[0])+"'")
            sys.exit(-1)
        return node
    
    if(a.type == "function-dec"):
        function[a.children[0]]=a.children[1]
        print 'function ', a.children[0], ' defined, with value ', function[a.children[0]]

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
    if(0):    
        n1 = ast.ASTNode()
        n1.value = 5
        n1.type = "terminal"
        
        n3 = ast.ASTNode()
        n3.type = "terminal"
        n3.value = 11
        
        n4 = ast.ASTNode()
        n4.type = "terminal"
        n4.value = 10
        
        n2 = ast.ASTNode()
        n2.type = "arithmetic"
        
        n2.children.append(n3)
        n2.children.append(n4)
        def subtract(x,y):
            print "Subtracting: ",x,y 
            return x-y
            
        n2.children.append(subtract)
        
        a = ast.ASTNode()
        a.type = "arithmetic"
        a.children.append(n1)
        a.children.append(n2)
        
        def add(x,y):
            print "Adding: ",x,y 
            return x+y
        a.children.append(add)

        evaluateAST(a)
    
    try:
        s = raw_input('graphene> ')
    except EOFError:
        break
    if not s: continue
    if (not s.lower() == "exit"):
        result = parser.parse(s) 
    else:
        sys.exit()
