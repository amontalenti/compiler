class AST(object):
      pass

class Assignment(AST):
      def __init__(self,location,value):
          self.location = location
          self.value = value

class BinaryOperator(AST):
      def __init__(self,operator,left,right):
          self.operator = operator
          self.left = left
          self.right = right

class Number(AST):
      def __init__(self,value):
          self.value = value

class Identifier(AST):
      def __init__(self,name):
          self.name = name

text = "b = 23 + 42"
location = Identifier("b")
left = Number(23)
right = Number(42)
value = BinaryOperator("+", left, right)
node = Assignment(location, value)

grammar = r"""
assignment ::=  ID '=' expr ';'

expression ::= term { ('+'|'-') term }*

term       ::= factor { ('*'|'/') factor }*

factor     ::= '(' expression ')'
           |   NUMBER
           |   ID
"""

