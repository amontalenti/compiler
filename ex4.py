import ast
class CodeGenerator(ast.NodeVisitor):
    def __init__(self):
        self.code = []

    def visit_BinOp(self,node):
        self.visit(node.left)
        self.visit(node.right)
        opname = node.op.__class__.__name__
        inst = ("BINARY_"+opname.upper(),)
        self.code.append(inst)

    def visit_Name(self,node):
        if isinstance(node.ctx, ast.Load):
            inst = ('LOAD_GLOBAL',node.id)
        else:
            inst = ('Unimplemented',)
        self.code.append(inst)

    def visit_Num(self,node):
        inst = ('LOAD_CONST',node.n)
        self.code.append(inst)

top = ast.parse("a + 2*b - 3*c")
gen = CodeGenerator()
gen.visit(top)
print(gen.code)

