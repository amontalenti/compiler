# exprtype.py
'''
Expr Type System
================
This file defines classes representing types.  There is a general
class used to represent all types.  Each type is then a singleton
instance of the type class.

class ExprType(object):
      pass

int_type = ExprType("int",...)
float_type = ExprType("float",...)
string_type = ExprType("string", ...)

The contents of the type class is entirely up to you.  However, you
will minimally need to encode some information about:

   a.  What operators are supported (+, -, *, etc.).
   b.  Default values
   c.  ????
   d.  Profit!

Once you have defined the built-in types, you will need to
make sure they get registered with any symbol tables or
code that checks for type names in 'exprcheck.py'.

Note:  This file is expanded in later stages of the compiler project.
'''

import operator

class ExprType(object):
    '''
    Class that represents a type in the Expr language.  Types 
    are declared as singleton instances of this type.
    '''
    def __init__(self, typename, default, 
                 unary_opcodes=None, binary_opcodes=None, 
                 binary_ops=None, unary_ops=None,
                 binary_folds=None, unary_folds=None,
                 rel_ops=None, rel_opcodes=None):
        '''
        You must implement yourself and figure out what to store.
        '''
        self.typename = typename
        self.binary_ops = binary_ops or set()
        self.unary_ops = unary_ops or set()
        self.default = default
        self.unary_opcodes = unary_opcodes or {}
        self.binary_opcodes = binary_opcodes or {}
        self.unary_folds = unary_folds or set()
        self.binary_folds = binary_folds or set()
        self.rel_ops = rel_ops or set()
        self.rel_opcodes = rel_opcodes or {}

    def __repr__(self):
        return "ExprType({})".format(self.typename)

IntType = ExprType("int", int(), 
    binary_ops={"+", "-", "*", "/"}, 
    unary_ops={"+", "-"},
    binary_opcodes={"+": "add", "-": "sub", "*": "imul", "/": "idiv"},
    unary_opcodes={"+": "uadd", "-": "uneg"},
    binary_folds={"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv},
    unary_folds={"+": operator.pos, "-": operator.neg},
    rel_ops={"==", "!=", "<", ">", "<=", ">="},
    rel_opcodes={"==": "eq", "!=": "neq", ">": "gt", "<": "lt", ">=": "gte", "<=": "lte"}
)
FloatType = ExprType("float", float(), 
    binary_ops={"+", "-", "*", "/"}, 
    unary_ops={"+", "-"},
    binary_opcodes={"+": "add", "-": "sub", "*": "fmul", "/": "fdiv"},
    unary_opcodes={"+": "uadd", "-": "uneg"},
    binary_folds={"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.floordiv},
    unary_folds={"+": operator.pos, "-": operator.neg},
    rel_ops={"==", "!=", "<", ">", "<=", ">="},
    rel_opcodes={"==": "eq", "!=": "neq", ">": "gt", "<": "lt", ">=": "gte", "<=": "lte"}
)
StringType = ExprType("string", str(), 
    binary_ops={"+"},
    binary_opcodes={"+": "add"},
    binary_folds={"+": operator.add},
    rel_ops={"==", "!="},
    rel_opcodes={"==": "eq", "!=": "neq"}
)
BoolType = ExprType("bool", bool(),
    unary_ops={"!"},
    rel_ops={"==", "!=", "&&", "||"},
    rel_opcodes={"==": "eq", "!=": "neq", "&&": "land", "||": "lor"}
)
