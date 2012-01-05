# exprconst.py
'''
Project 5 - Optimization : Constant folding
===========================================

In this file, implement a NodeTransformer class that walks the AST and performs
a constant folding optimization.

Essentially constant folding is the process of evaluating constant expressions
at compile time.  For example, if you have this statement:

      a = 1 + 2 + 3 + 4;

The compiler will simply evaluate the right-hand constant and rewrite the
AST so that it looks like this:

      a = 10;

Unlike other AST walking tasks, this file actually rewrites and simplifies
the AST.  To do this, you should use the NodeTransformer class defined
in exprast.py.  To use this class, you write the same node walking code
as before except that every method is now expected to return a replacement
node.  See instructions below.
'''

# STEP 1: Implement compile-time evaluation rules for types
#
# Go to the exprtype.py file and give types the ability to perform compile-time
# evaluation.   To do this, I would suggest giving types two new attributes:
#
#       compile_binary_ops
#       compile_unary_ops
#
# These attributes should be dictionaries that map operator names to 
# functions that can carry out the operation at compile time.  The operator
# module is useful for this.  Here is an example:
#
# int_type = ExprType(
#    name = "int",
#    ...
#    compile_binary_ops = {
#           '+' : operator.add,
#           '-' : operator.sub,
#           '*' : operator.mul,
#           '/' : operator.floordiv
#    },
#    compile_unary_ops = {
#           '+' : operator.pos,
#           '-' : operator.neg
#  }

import exprtype

# STEP 2: Implement a Node Transformation class
#
# To transform the AST, define a class that inherits from exprast.NodeTransformer.
# In this class, you write visit_NodeName() methods as before except that you must
# now return a result.  The result is the replacement AST node (if any), the same
# node as before, or None (in which case the node is deleted).
#
# For example:
#
#      class ConstantFolder(exprast.NodeTransformer):
#           def visit_Binop(self,node):
#                 node.left = self.visit(node.left)     # Rewrite left node
#                 node.right = self.visit(node.right)   # Rewrite right node
# 
#                 new_node = SomeNewNode(...)           # Create a new kind of node
#                 return new_node
#      ...
#
# Implement the class below and make the indicated transformations

import exprast

class ConstantFolder(exprast.NodeTransformer):
    def visit_Program(self,node):
        # Get a reference to the program symbol table for later use
        self.symtab = node.symtab
        self.visit(node.statements)
        return node

    def visit_Binop(self,node):
        # If both the left and right are constant literals, replace the node
        # with a literal value that is the result of the binary operator
        pass

    def visit_Unaryop(self,node):
        # If the operand is a constant literal, replace the node with a
        # literal value that is the result of the unary operator
        pass

    def visit_LoadLocation(self,node):
        # If the lookup location is a constant (found in symbol table),
        # replace the node with a Literal node that has the value of the constant
        pass


    def visit_ConstDeclaration(self,node):
        # Delete the node by returning nothing.   Constants are held in the symbol table,
        # but do not need to be emitted.
        pass

# STEP 3 : Testing
#
# Try running this program on the good.e program and viewing the resulting
# program.  If it's working, it should be significantly smaller than before.
#
#     bash % python exprconst.py good.e > a.py
#     bash % python a.py
#     ... make sure output is the same ...
#
# Compare the output against the output of the exprpygen.py program:
#
#     bash % python exprpygen.py good.e > a.py
#
#

#
# ----------------------------------------------------------------------
#                       DO NOT MODIFY ANYTHING BELOW       
# ----------------------------------------------------------------------

def fold_constants(node):
    '''
    Perform constant folding optimization on the AST.
    '''
    return ConstantFolder().visit(node)

if __name__ == '__main__':
    import exprlex
    import exprparse
    import exprcheck
    import exprcode
    import exprpygen

    import sys
    from errors import subscribe_errors, errors_reported
    lexer = exprlex.make_lexer()
    parser = exprparse.make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())
        # Check the program
        exprcheck.check_program(program)
        # If no errors occurred, generate code
        if not errors_reported():
            # Perform constant constants
            program = fold_constants(program)
            # Create 3-address IR
            exprcode.generate_code(program)
            # Generate Python code output
            exprpygen.emit_pycode("main", program.code)
            print("if __name__ == '__main__':")
            print("     main()")
