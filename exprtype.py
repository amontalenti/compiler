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

class ExprType(object):
    '''
    Class that represents a type in the Expr language.  Types 
    are declared as singleton instances of this type.
    '''
    def __init__(self, typename, binary_ops=None, unary_ops=None):
        '''
        You must implement yourself and figure out what to store.
        '''
        self.typename = typename
        self.binary_ops = binary_ops or set()
        self.unary_ops = unary_ops or set()

    def __repr__(self):
        return "ExprType({})".format(self.typename)

IntType = ExprType("int", binary_ops={"+", "-", "*", "/"}, unary_ops={"+", "-"})
FloatType = ExprType("float", binary_ops={"+", "-", "*", "/"}, unary_ops={"+", "-"})
StringType = ExprType("string", binary_ops={"+"})
