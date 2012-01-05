import ast
top = ast.parse("1+2+3+4")
print(ast.dump(top))
def foo():
    print(1+2+3+4)
import dis
dis.dis(foo)
class NumFolder(ast.NodeTransformer):
    mapping = {
        ast.Add: "__add__", 
        ast.Sub: "__sub__", 
        ast.Mult: "__mul__"
    }
    def visit_BinOp(self, node):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        if isinstance(node.left, ast.Num) and isinstance(node.right, ast.Num):
            for cls, method in self.mapping.items(): 
                if isinstance(node.op, cls): 
                    opmethod = method
            if opmethod is None: 
                return node
            return ast.Num(getattr(node.left.n, opmethod)(node.right.n))
        return node
top = NumFolder().visit(top)
print(ast.dump(top))
