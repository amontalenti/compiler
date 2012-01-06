# exprblock.py
'''
Project 7: Basic Blocks and Control Flow
----------------------------------------
This file defines classes and functions for creating and navigating
basic blocks.  You need to write all of the code needed yourself.

See Exercise 7.
'''

class Block(object):
    def __init__(self):
        self.instructions = []   # Instructions in the block
        self.next = None   # Link to the next block

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
        super(IfBlock, self).__init__()
        self.truebranch = None
        self.falsebranch = None

class WhileBlock(Block):
    '''
    '''
    def __init__(self):
        super(WhileBlock, self).__init__()
        self.truebranch = None

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
            block = getattr(block, "next", None)

