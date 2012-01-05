# exprparse.py
'''
Project 2:  Write a parser
==========================
In this project, you write the basic shell of a parser for the expression
language.  A formal BNF of the language follows.  Your task is to write
parsing rules and build the AST for this grammar using PLY.

program : basicblock

basicblock : statements
           | empty

statements :  statements statement
           |  statement

statement :  const_declaration
          |  var_declaration
          |  assign_statement
          |  print_statement

if_statement : if expression { basicblock }

if_else_statement : if expression { basicblock } else { basicblock }

while_statement : while expression { basicblock }

const_declaration : CONST identifier = expression ;

var_declaration : VAR identifier typename ;
                | VAR identifier typename = expression ;

assign_statement : location = expression ;

print_statement : PRINT expression ;

expression :  + expression
           |  - expression
           |  ! expression
           | expression + expression
           | expression - expression
           | expression * expression
           | expression / expression
           | expression > expression
           | expression >= expression
           | expression < expression
           | expression <= expression
           | expression == expression
           | expression != expression
           | expression && expression
           | expression || expression
           | ( expression )
           | location
           | literal

literal : INTEGER     
        | FLOAT       
        | STRING      
        | BOOL

location : ID

typename : ID

empty    :

To do the project, follow the instructions contained below.
'''

# ----------------------------------------------------------------------
# parsers are defined using PLYs yacc module.
#
# See http://www.dabeaz.com/ply/ply.html#ply_nn23
# ----------------------------------------------------------------------
from ply import yacc

# ----------------------------------------------------------------------
# The following import loads a function error(lineno,msg) that should be
# used to report all error messages issued by your parser.  Unit tests and
# other features of the compiler will rely on this function.  See the
# file errors.py for more documentation about the error handling mechanism.
from errors import error

# ----------------------------------------------------------------------
# Get the token list defined in the lexer module.  This is required
# in order to validate and build the parsing tables.
from exprlex import tokens

# ----------------------------------------------------------------------
# Get the AST nodes.  
# Read instructions in exprast.py
from exprast import *

# ----------------------------------------------------------------------
# Operator precedence table.   Operators must follow the same 
# precedence rules as in Python.  Instructions to be given in the project.
# See http://www.dabeaz.com/ply/ply.html#ply_nn27
precedence = (
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('nonassoc', 'GT', 'GTE', 'LT', 'LTE', 'EQ', 'NEQ'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UNARY'),
)

# ----------------------------------------------------------------------
# YOUR TASK.   Translate the BNF in the string below into a collection
# of parser functions.  For example, a rule such as :
#
#   program : statements
#
# Gets turned into a Python function of the form:
#
# def p_program(p):
#      '''
#      program : statements
#      '''
#      p[0] = Program(p[1])
#
# For symbols such as '(' or '+', you'll need to replace with the name
# of the corresponding token such as LPAREN or PLUS.
#
# In the body of each rule, create an appropriate AST node and assign it
# to p[0] as shown above.
#
# For the purposes of lineno number tracking, you should assign a line number
# to each AST node as appropriate.  To do this, I suggest pulling the 
# line number off of any nearby terminal symbol.  For example:
#
# def p_print_statement(p):
#     '''
#     print_statement: PRINT expr SEMI
#     '''
#     p[0] = PrintStatement(p[2],lineno=p.lineno(1))
#

def p_program_empty(p):
    '''
    program : empty
    '''
    p[0] = Program(None)

def p_program(p):
    '''
    program : basicblock
    '''
    p[0] = Program(p[1])
    
def p_basicblock(p):
    '''
    basicblock : statements
               | empty
    '''
    p[0] = p[1]

def p_statements(p):
    '''
    statements : statements statement
    '''
    p[0] = p[1]
    p[0].append(p[2])

def p_statements_1(p):
    '''
    statements : statement
    '''
    p[0] = Statements([p[1]])


def p_statement(p):
    '''
    statement : const_declaration
              |  var_declaration
              |  assign_statement
              |  print_statement
              |  if_statement
              |  if_else_statement
              |  while_statement
    '''
    p[0] = p[1]

def p_if_statement(p):
    '''
    if_statement : IF expression LCURL basicblock RCURL
    '''
    p[0] = IfStatement(p[2], p[4], None)

def p_if_else_statement(p):
    '''
    if_else_statement : IF expression LCURL basicblock RCURL ELSE LCURL basicblock RCURL
    '''
    p[0] = IfStatement(p[2], p[4], p[8])

def p_while_statement(p):
    '''
    while_statement : WHILE expression LCURL basicblock RCURL
    '''
    p[0] = WhileStatement(p[1], p[2])

def p_const_declaration(p):
    '''
    const_declaration : CONST ID ASSIGN expression SEMI
    '''
    p[0] = ConstDeclaration(p[2],p[4],lineno=p.lineno(1))

def p_var_declaration(p):
    '''
    var_declaration : VAR ID typename SEMI
    '''
    p[0] = VarDeclaration(p[2],p[3],None,lineno=p.lineno(1))

def p_var_declaration_expr(p):
    '''
    var_declaration : VAR ID typename ASSIGN expression SEMI
    '''
    p[0] = VarDeclaration(p[2],p[3],p[5],lineno=p.lineno(1))

def p_assign_statement(p):
    '''
    assign_statement : location ASSIGN expression SEMI
    '''
    p[0] = AssignmentStatement(p[1],p[3],lineno=p.lineno(2))

def p_print_statement(p):
    '''
    print_statement : PRINT expression SEMI
    '''
    p[0] = PrintStatement(p[2],lineno=p.lineno(1))

def p_expression_unary(p):
    '''
    expression : PLUS expression %prec UNARY
               | MINUS expression %prec UNARY
               | NOT expression %prec UNARY
    '''
    p[0] = Unaryop(p[1],p[2],lineno=p.lineno(1))

def p_expression_binary(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
    '''
    p[0] = Binop(p[2],p[1],p[3],lineno=p.lineno(2))

def p_expression_rel(p):
    '''
    expression : expression GT expression
               | expression GTE expression
               | expression LT expression
               | expression LTE expression
               | expression EQ expression
               | expression NEQ expression
               | expression LAND expression
               | expression LOR expression
    '''
    p[0] = Relop(p[2],p[1],p[3],lineno=p.lineno(2))

def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_expression_location(p):
    '''
    expression : location
    '''
    p[0] = LoadLocation(p[1], lineno=p[1].lineno)

def p_expression_literal(p):
    '''
    expression : literal
    '''
    p[0] = p[1]

def p_literal(p):
    '''
    literal : INTEGER
            | FLOAT
            | STRING
            | BOOL
    '''
    p[0] = Literal(p[1],lineno=p.lineno(1))

def p_location(p):
    '''
    location : ID
    '''
    p[0] = Location(p[1],lineno=p.lineno(1))

def p_typename(p):
    '''
    typename : ID
    '''
    p[0] = Typename(p[1],lineno=p.lineno(1))

def p_empty(p):
    '''
    empty    :
    '''

# ----------------------------------------------------------------------
# DO NOT MODIFY
#
# catch-all error handling.   The following function gets called on any
# bad input.  See http://www.dabeaz.com/ply/ply.html#ply_nn31
def p_error(p):
    if p:
        error(p.lineno, "Syntax error in input at token '%s'" % p.value)
    else:
        error("EOF","Syntax error. No more input.")

# ----------------------------------------------------------------------
#                     DO NOT MODIFY ANYTHING BELOW HERE
# ----------------------------------------------------------------------

def make_parser():
    parser = yacc.yacc()
    return parser

if __name__ == '__main__':
    import exprlex
    import sys
    from errors import subscribe_errors
    lexer = exprlex.make_lexer()
    parser = make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())

    # Output the resulting parse tree structure
    for depth,node in flatten(program):
        print("%s%s" % (" "*(4*depth),node))

