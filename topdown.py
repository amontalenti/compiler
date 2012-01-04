# topdown.py
#
# Sample top-down parser.  An example of recursive descent parsing.
#
# Solution code is in the Solution directory.

import re
from ply.lex import lex

# ------------------------------------------------------------
# Tokenizer

tokens = ['NUMBER','ID','ASSIGN','PLUS','MINUS','TIMES','DIVIDE','LPAREN','RPAREN','SEMI']
t_ignore = ' \n\t'

t_NUMBER = r'\d+'
t_ID     = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ASSIGN = r'='
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI   = r'\;'

def t_error(t):
    print("Bad input %r" % t.value[0])
    t.lexer.skip(1)

lexer = lex()

# ------------------------------------------------------------
# Abstract syntax tree nodes
class AST(object):
    '''
    Base class. Don't use directly.
    '''
    pass

class Identifer(AST):
    '''
    An identifier.
    '''
    def __init__(self,id):
        self.id = id

    def __repr__(self):
        return "Identifier(%r)" % self.id

class Number(AST):
    '''
    A number
    '''
    def __init__(self,value):
        self.value = value
    
    def __repr__(self):
        return "Number(%r)" % self.value

class Binop(AST):
    '''
    A binary operator (e.g., left + right)
    '''
    def __init__(self,op,left,right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return "Binop(%r,%r,%r)" % (self.op,self.left,self.right)

class Assignment(AST):
    '''
    Variable assignment
    '''
    def __init__(self,location,expr):
        self.location = location
        self.expr = expr

    def __repr__(self):
        return "Assignment(%r,%r)" % (self.location,self.expr)

# ------------------------------------------------------------
# Recursive Descent Parser.
#
# You must modify the methods of this class to build the parse tree
class RecursiveDescentParser(object):
    '''
    Implementation of a recursive descent parser.   Each method
    implements a single grammar rule.  Use the ._accept() method
    to test and accept the current lookahead token.  Use the ._expect()
    method to exactly match and discard the next token on on the input
    (or raise a SyntaxError if it doesn't match).

    The .tok attribute hold the last accepted token.  The .nexttok
    attribute holds the next lookahead token.
    '''
    def assignment(self):
        '''
        assignment : ID = expression ;
        '''
        if self._accept("ID"):
            name = self.tok.value
            self._expect("ASSIGN")
            expr = self.expression()
            self._expect("SEMI")
            return Assignment(name,expr)
        else:
            raise SyntaxError("Expected an identifier")
        
    def expression(self):
        '''
        expression : term { ('+'|'-') term }          # EBNF
                   ''' 
        # You need to complete
        expr = self.term()
        while self._accept("PLUS") or self._accept("MINUS"):
            operator = self.tok.value
            right = self.term()
            expr = Binop(operator,expr,right)
        return expr
    
    def term(self):
        '''
        term : factor { ('*'|'/') factor }            # EBNF
             '''
        term = self.factor()
        while self._accept("TIMES") or self._accept("DIVIDE"):
            operator = self.tok.value
            right = self.factor()
            term = Binop(operator,term,right)
        return term

    def factor(self):
        '''
        factor : ID
               | NUMBER
               | ( expression )
               '''
        if self._accept("ID"):
            return Identifier(self.tok.value)
        elif self._accept("NUMBER"):
            return Number(self.tok.value)
        elif self._accept("LPAREN"):
            expr = self.expression()
            self._expect("RPAREN")
            return expr
        else:
            raise SyntaxError("Expected ID, NUMBER, or LPAREN")

    # ------------------------------------------------------------
    # Utility functions.  Don't change anything below here
    def _advance(self):
        'Advanced the tokenizer by one symbol'
        self.tok, self.nexttok = self.nexttok, lexer.token()

    def _accept(self,toktype):
        'Consume the next token if it matches an expected type'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self,toktype):
        'Consume and discard the next token or raise SyntaxError'
        if not self._accept(toktype):
            raise SyntaxError("Expected %s" % toktype)

    def start(self):
        'Entry point to parsing'
        self._advance()              # Load first lookahead token
        return self.assignment()

    def parse(self,text):
        'Entry point to parsing'
        self.tok = None             # Last symbol consumed
        self.nexttok = None         # Next symbol tokenized
        lexer.input(text)
        return self.start()

if __name__ == '__main__':
    text = "a = 2 + 3 * (4 + 5);"
    parser = RecursiveDescentParser()
    top = parser.parse(text)

    print(top)
    assert repr(top) == "Assignment('a',Binop('+',Number('2'),Binop('*',Number('3'),Binop('+',Number('4'),Number('5')))))"

    # Check operator precedence
    text = "b = 2 - 3 - 4;"
    top = parser.parse(text)
    print(top)
    assert repr(top) == "Assignment('b',Binop('-',Binop('-',Number('2'),Number('3')),Number('4')))"


            
        
