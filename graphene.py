import ply.yacc as yacc
import ply.lex as lex

fn_names = ["print", "count", "listEdges"]
#print("Hello world!")

tokens = ('ID', 'LPAREN', 'RPAREN', 'STRING', 'WHITESPACE')

t_ID = r'[a-zA-Z\_][a-zA-Z\_0-9]+'
     
t_LPAREN = r'\('

t_RPAREN = r'\)'
    
t_STRING = r'\"[a-zA-Z\ 0-9]+\"'

def t_error(t):
    print "Lex Error"

lexer = lex.lex()


def p_call(p):
    '''call : ID LPAREN STRING RPAREN'''
    if(p[1] in fn_names):
        print p[3][1:-1]
    else:
        print "You sir, suck."

parser = yacc.yacc()


while True: 

    try:
        s = raw_input('graphene> ')
    except EOFError:
        break
    if not s: continue 
    result = parser.parse(s) 