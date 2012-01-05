code = """\
start
if a < 0:
    a + b
else:
    a - b
done
"""
import ast
top = ast.parse(code)
print(ast.dump(top))

class Block(object):
    def __init__(self):
        self.instructions = []   # Instructions in the block
        self.next_block =None    # Link to the next block

    def append(self,instr):
        self.instructions.append(instr)

    def __iter__(self):
        return iter(self.instructions)

class BasicBlock(Block):
    '''
    Class for a simple basic block.  Control flow unconditionally
    flows to the next block.
    '''
    pass

class IfBlock(Block):
    '''
    Class for a basic-block representing an if-else.  There are
    two branches to handle each possibility.
    '''
    def __init__(self):
        super(IfBlock,self).__init__()
        self.if_branch = None
        self.else_branch = None

class CodeGenerator(ast.NodeVisitor):
    '''
    Sample code generator with basic blocks and a control flow graph
    '''
    def __init__(self):
        self.current_block = BasicBlock()
        self.start_block = self.current_block

    def visit_If(self,node):
        '''
        Example of compiling a simple Python if statement. You
        might want to draw a picture of the links.
        '''
        # Step 1: Make a new BasicBlock for the conditional test
        ifblock = IfBlock()
        self.current_block.next_block = ifblock
        self.current_block = ifblock

        # Step 2:  Evaluate the test condition
        self.visit(node.test)

        # Step 3: Create a branch for the if-body
        self.current_block = BasicBlock()
        ifblock.if_branch = self.current_block

        # Step 4: Traverse all of the statements in the if-body
        for bnode in node.body:
            self.visit(bnode)

        # Step 5: If there's an else-clause, create a new block and
        if node.orelse:
            self.current_block = BasicBlock()
            ifblock.else_branch = self.current_block

            # Visit the body of the else-clause
            for bnode in node.orelse:
                self.visit(bnode)

        # Step 6: Create a new basic block to start the next section
        self.current_block = BasicBlock()
        ifblock.next_block = self.current_block

    def visit_BinOp(self,node):
        self.visit(node.left)
        self.visit(node.right)
        opname = node.op.__class__.__name__
        inst = ("BINARY_"+opname.upper(),)
        self.current_block.append(inst)

    def visit_Compare(self,node):
        self.visit(node.left)
        opname = node.ops[0].__class__.__name__
        self.visit(node.comparators[0])
        inst = ("BINARY_"+opname.upper(),)
        self.current_block.append(inst)

    def visit_Name(self,node):
        if isinstance(node.ctx, ast.Load):
            inst = ('LOAD_GLOBAL',node.id)
        else:
            inst = ('Unimplemented,')
        self.current_block.append(inst)

    def visit_Num(self,node):
        inst = ('LOAD_CONST',node.n)
        self.current_block.append(inst)

class BlockVisitor(object):
    '''
    Class for visiting basic blocks.  Define a subclass and define
    methods such as visit_BasicBlock or visit_IfBlock to implement
    custom processing (similar to ASTs).
    '''
    def visit(self,block):
        while block:
            name = "visit_%s" % type(block).__name__
            if hasattr(self,name):
                getattr(self,name)(block)
            block = block.next_block

class PrintBlocks(BlockVisitor):
    def visit_BasicBlock(self,block):
        print("Block:[%s]" % block)
        for inst in block.instructions:
            print("    %s" % (inst,))
        print("")

    def visit_IfBlock(self,block):
        self.visit_BasicBlock(block)
        self.visit(block.if_branch)
        self.visit(block.else_branch)

top = ast.parse("""\
start
if a < 0:
   a + b
else:
   a - b
done
""")
gen = CodeGenerator()
gen.visit(top)
PrintBlocks().visit(gen.start_block)

class EmitBlocks(BlockVisitor):
    def visit_BasicBlock(self,block):
        print("Block:[%s]" % block)
        for inst in block.instructions:
            print("    %s" % (inst,))

    def visit_IfBlock(self,block):
        self.visit_BasicBlock(block)
        # Emit a conditional jump around the if-branch
        inst = ('JUMP_IF_FALSE',
                block.else_branch if block.else_branch else block.next_block)
        print("    %s" % (inst,))
        self.visit(block.if_branch)
        if block.else_branch:
            # Emit a jump around the else-branch (if there is one)
            inst = ('JUMP', block.next_block)
            print("    %s" % (inst,))
            self.visit(block.else_branch)

EmitBlocks().visit(gen.start_block)
