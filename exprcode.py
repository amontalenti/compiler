# exprcode.py
'''
Project 4 (part 1)
==================
Code generation for the Expr language.  In this project, you are going to turn
the AST into an intermediate machine code known as three-address code.  Three
address code is simple--it's a simple machine code where all operations only
involve at most two operands and a destination variable. 

Suppose you had a mathematical expression like this:

        a = 2 + 3*4 - 5

A three address code implementation might be as follows:

        int_1 = 2
        int_2 = 3
        int_3 = 4
        int_4 = int_2 * int_3
        int_5 = int_1 + int_4
        int_6 = 5
        int_7 = int_5 - int_6
        a = int_7

In this code, the int_n variables are simply temporaries used 
while performing the calculation.  They can be later thrown out.

One benefit of three address code is that it is very easy to encode
and manipulate. For example, you could encode the above sequence of
operations as tuples:

       [ 
         ('loadi', 2, 'int_1'),
         ('loadi', 3, 'int_2'),
         ('loadi', 4, 'int_3'),
         ('mul', 'int_2', 'int_3', 'int_4'),
         ('add', 'int_1', 'int_4', 'int_5'),
         ('loadi', 5, 'int_6'),
         ('sub', 'int_5','int_6','int_7'),
         ('store','int_7','a')
       ]

The other reason for using 3-address code is that it is very closely
matched to instructions one might carry out on the underlying CPU
hardware.  For example, these tuples could be translated to low level
machine instructions (for a hypothetical CPU) like this:

         MOVI   #2, R1
         MOVI   #3, R2
         MOVI   #4, R3
         MUL    R2, R3, R2
         ADD    R1, R2, R1
         MOVI   #5, R2
         SUB    R1, R2, R1
         STORE  R1, a

Your Task
=========
Your task is simple.  Write a AST Visitor() class that takes an
Expr program and flattens it to a single sequence of 3-address
code instructions represented as tuples of the form 

       (operation, operands, ..., destination)

Your 3-address code is only allowed to use the following operators:

       ('load', varname, target)      # Load from a variable
       ('loadi', literal, target)     # Load a literal value (immediate)
       ('newvar', source,varname)     # Create and store into a new variable
       ('store', source, varname)     # Store into a variable
       ('add',left,right,target)      # target = left + right
       ('sub',left,right,target)      # target = left - right
       ('mul',left,right,target)      # target = left * right
       ('idiv',left,right,target)     # target = left / right  (integer truncation)
       ('fdiv',left,right,target)     # target = left / right (floating point)
       ('eq',left,right,target)       # target = left == right
       ('neq',left,right,target)      # target = left != right
       ('gt',left,right,target)       # target = left > right
       ('gte',left,right,target)      # target = left >= right
       ('lt',left,right,target)       # target = left < right
       ('lte',left,right,target)      # target = left <= right
       ('uadd',source,target)         # target = +source
       ('uneg',source,target)         # target = -source
       ('not',source,target)          # target = !source
       ('print',source)               # Print value of source

       ('load_local',name,target)     # Load value of a local variable
       ('load_global',name,target)    # Load value of a global variable
       ('store_local',source,name)    # Store value of a local variable
       ('store_global',source,name)   # Store value of a global variable
       ('newvar_local',source,name)   # Make a new local variable
       ('newvar_global',source,name)  # Make a new global variable
       ('new_frame',)                 # Make new stack frame
       ('store_frame',source,name)    # Store value in new stack frame
       ('load_frame',name,target)     # Load value from stack frame
       ('newvar_frame',source,name)   # Make a new value in the stack frame
       ('call',name)                  # Call function with last created stack frame
       ('del_frame',)                 # Delete last created stack frame

When emitting 3-address code, you should never reuse names for temporary
variables.  Simply keep a counter and keep making new names whenever you
need a new temporary value (e.g., int_1, int_2, int_3, ...).  Also,
the name of the variable should start with the type as shown. For example,
use float_n for floats and string_n for strings.  Including the type
is useful for debugging and will have uses later on.

The 3-address sequence that you create should be attached to the code
generation class. Here is a rough idea of how it should work:

     top = parse(text)                # Get the parse tree
     exprcheck.check_program(top)     # Perform type checking
     if no_errors:
          gen = GenerateCode()
          gen.visit(top)
          code_sequence = gen.code    # Get the code sequence
'''

# STEP 1: Figure out some way to map operator names such as +, -, *, /
# to the opcode names 'add','sub','mul','div'.   I suggest doing this
# by adding information to the ExprType instances defined in exprtype.py.
#
# One reason for putting it on the type instances is that it becomes
# easier to change and customize later.  For example, if you needed
# to use a different set of opcodes for ints as for strings.

import exprtype
import exprast
import exprblock

# STEP 2: Implement the following Node Visitor class so that it creates
# a sequence of three-address code instructions and attaches it to
# the top-level Program AST node.
class GenerateCode(exprast.NodeVisitor):
    '''
    Node visitor class that creates 3-address encoded instruction sequences.
    '''
    def new_temp(self,type):
        name = "%s_%d" % (type.typename,self.temp_count)
        self.temp_count += 1
        return name

    def visit_Program(self,node):
        # Reset the sequence of instructions and temporary count

        self.code = exprblock.BasicBlock()
        self.program = self.code
        self.temp_count = 0
        # Visit all of the statements in the program
        self.visit(node.statements)

    # You must implement visit_Nodename methods for all of the other
    # AST nodes.  In your code, you will need to make instructions
    # and append them to the self.code list.
    #
    # One sample method follows

    def visit_Literal(self,node):
        target = self.new_temp(node.check_type)
        inst = ('loadi', node.value, target)
        self.code.append(inst)
        # Save the name of the temporary variable where the value was placed 
        node.gen_location = target

    def visit_Unaryop(self,node):
        self.visit(node.expr)
        target = self.new_temp(node.check_type)
        instruction = node.check_type.unary_opcodes[node.op] 
        inst = (instruction, node.expr.gen_location, target)
        self.code.append(inst)
        node.gen_location = target

    def visit_LoadLocation(self, node):
        target = self.new_temp(node.check_type)
        inst = ('load', node.location.name, target)
        self.code.append(inst)
        # Save the name of the temporary variable where the value was placed 
        node.gen_location = target

    def visit_Binop(self, node):
        self.visit(node.left)
        self.visit(node.right)
        target = self.new_temp(node.check_type)
        instruction = node.check_type.binary_opcodes[node.op]
        inst = (instruction, node.left.gen_location, node.right.gen_location, target)
        self.code.append(inst)
        node.gen_location = target

    def visit_Relop(self, node):
        self.visit(node.left)
        self.visit(node.right)
        target = self.new_temp(node.check_type)
        instruction = node.left.check_type.rel_opcodes[node.op]
        inst = (instruction, node.left.gen_location, node.right.gen_location, target)
        self.code.append(inst)
        node.gen_location = target

    def visit_VarDeclaration(self, node):
        self.visit(node.expr)
        if node.scope_level == 0:
            opcode = "newvar_global"
        else:
            opcode = "newvar_local"
        inst = (opcode, node.expr.gen_location, node.name)
        self.code.append(inst)

    def visit_ConstDeclaration(self, node):
        self.visit(node.expr)
        if node.scope_level == 0:
            opcode = "newvar_global"
        else:
            opcode = "newvar_local"
        inst = (opcode, node.expr.gen_location, node.name)
        self.code.append(inst)

    def visit_AssignmentStatement(self, node):
        self.visit(node.expr)
        inst = ("store_local", node.expr.gen_location, node.location.name)
        self.code.append(inst)

    def visit_PrintStatement(self, node):
        self.visit(node.expr)
        inst = ("print", node.expr.gen_location)
        self.code.append(inst)

    def visit_IfStatement(self, node):
        #print("visiting %r" % node)
        ifblock = exprblock.IfBlock()
        self.code.next = ifblock
        ifblock.truebranch = exprblock.BasicBlock()
        self.code = ifblock
        self.visit(node.expr)
        self.code.condvar = node.expr.gen_location
        self.code = ifblock.truebranch
        self.visit(node.truebranch)
        if node.falsebranch is not None:
            ifblock.falsebranch = exprblock.BasicBlock()
            self.code = ifblock.falsebranch
            self.visit(node.falsebranch)
        # Done expanding if statement, now link to a fresh block
        self.code = exprblock.BasicBlock()
        ifblock.next = self.code

    def visit_WhileStatement(self, node):
        whileblock = exprblock.WhileBlock()
        self.code.next = whileblock
        whileblock.truebranch = exprblock.BasicBlock()
        self.code = whileblock
        self.visit(node.expr)
        self.code.condvar = node.expr.gen_location
        self.code = whileblock.truebranch
        #print("visiting %r" % node)
        self.visit(node.truebranch)
        # Done expanding while statement, now link to fresh block
        self.code = exprblock.BasicBlock()
        whileblock.next = self.code

    def visit_FuncCall(self, node):
        print("encountered function call")
        self.code.append(("new_frame",))
        self.visit(node.arguments)
        for arg in node.arguments.arguments:
            self.code.append(("store_frame", arg.gen_location, arg.parm.name))
        self.code.append(("call", node.name))

    def visit_FuncCallArguments(self, node):
        for arg in node.arguments:
                self.visit(arg)




# STEP 3: Testing
# 
# Try running this program on the input file good.e and viewing
# the resulting 3-address code sequence.
#
#     bash % python exprcode.py good.e
#     ... look at the output ...
#

# ----------------------------------------------------------------------
#                       DO NOT MODIFY ANYTHING BELOW       
# ----------------------------------------------------------------------
def generate_code(node):
    '''
    Generate three-address code from the supplied AST node.
    '''
    gen = GenerateCode()
    gen.visit(node)
    return gen.program

class JumpGenerator(exprblock.BlockVisitor):
    def visit_BasicBlock(self,block):
        print("Block:[%s]" % block)
        for inst in block.instructions:
            print("    %s" % (inst,))
        print("")

    def visit_IfBlock(self,block):
        # Emit a conditional jump around the if-branch
        #inst = ('if', block.condvar)
        #block.append(inst)
        self.visit_BasicBlock(block)
        if block.falsebranch:
            pass
            # Emit a jump around the else-branch (if there is one)
            #inst = ('else',)
            #block.truebranch.append(inst)
        self.visit(block.truebranch)
        if block.falsebranch:
            self.visit(block.falsebranch)

    def visit_WhileBlock(self,block):
        # Emit a conditional jump around the if-branch
        #inst = ('while', block.condvar)
        #block.append(inst)
        self.visit_BasicBlock(block)
        self.visit(block.truebranch)


if __name__ == '__main__':
    import exprlex
    import exprparse
    import exprcheck
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
            code = generate_code(program)
            # Emit the code sequence
            JumpGenerator().visit(code)
            for inst in code:
                print(inst)
