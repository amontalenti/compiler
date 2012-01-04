import ast

code = """\
a = 23
b = 42
c = a + 2*b - z
"""

top = ast.parse(code)
print(ast.dump(top))

print("first visit")
print("-"*10)

class NameVisitor(ast.NodeVisitor):
    def visit_Name(self,node):
        print((node.id,node.ctx))
NameVisitor().visit(top)

print("second visit")
print("-"*10)
class NameNumVisitor(ast.NodeVisitor):
    def visit_Name(self, node):
        print((node.id, node.ctx))
    def visit_Num(self, node):
        print(node.n)
NameNumVisitor().visit(top)

print("third visit")
print("-"*10)

class NameChecker(ast.NodeVisitor):
     def __init__(self):
         self.symbols = set()
     def visit_Name(self, node):
         if isinstance(node.ctx, ast.Store):
             self.symbols.add(node.id)
         elif isinstance(node.ctx, ast.Load):
             if node.id not in self.symbols:
                 print("Error: Name %s not defined" % node.id)

NameChecker().visit(top)

print("type checking")
print("-"*10)

class TypeCheck(ast.NodeVisitor):
     def visit_Num(self,node):
         node.check_type = "num"

     def visit_Str(self,node):
         node.check_type = "str"

# Perform type checking
TypeCheck().visit(top)

top = ast.parse("2+3")
ast.dump(top)
TypeCheck().visit(top)
print(top.body[0].value.left.check_type)
print(top.body[0].value.right.check_type)

class TypeCheck(ast.NodeVisitor):
    def visit_Num(self,node):
        node.check_type = "num"

    def visit_Str(self,node):
        node.check_type = "str"

    def visit_BinOp(self,node):
        self.visit(node.left)
        self.visit(node.right)
        if hasattr(node.left, "check_type") and hasattr(node.right, "check_type"):
            if node.left.check_type != node.right.check_type:
                print("Type Error: %s %s %s" % (node.left.check_type,
                                                node.op.__class__.__name__,
                                                node.right.check_type))
            else:
                node.check_type = node.left.check_type

    def visit_UnaryOp(self,node):
        self.visit(node.operand)
        if hasattr(node.operand, "check_type"):
            node.check_type = node.operand.check_type

top = ast.parse("3 + 4 * (23 - 45) / 2")
TypeCheck().visit(top)
print(top.body[0].value.check_type)

top = ast.parse("2+ 'Hello'")
TypeCheck().visit(top)

class TypeDefinition(object):
    def __init__(self,name,bin_ops, unary_ops):
        self.name = name
        self.bin_ops = bin_ops
        self.unary_ops = unary_ops

num_type = TypeDefinition("num", {'Add','Sub','Mult','Div'}, {'UAdd','USub'})
str_type = TypeDefinition("str", {'Add'},set())

class TypeCheck(ast.NodeVisitor):
    def __init__(self):
        self.symtab = {}

    def visit_Assign(self,node):
        self.visit(node.value)
        check_type = getattr(node.value,"check_type",None)
        # Store known type information in the symbol table (if any)
        for target in node.targets:
            self.symtab[target.id] = check_type

    def visit_Name(self,node):
        if isinstance(node.ctx,ast.Load):
            # Check if any type information is known.  If so, attach it
            if node.id in self.symtab:
                check_type = self.symtab[node.id]
                if check_type:
                    node.check_type = check_type
            else:
                print("Undefined identifier %s" % node.id)

    def visit_Num(self,node):
        node.check_type = num_type

    def visit_Str(self,node):
        node.check_type = str_type

    def visit_BinOp(self,node):
        self.visit(node.left)
        self.visit(node.right)
        opname = node.op.__class__.__name__
        if hasattr(node.left,"check_type") and hasattr(node.right,"check_type"):
            if node.left.check_type != node.right.check_type:
                print("Type Error: %s %s %s" % (node.left.check_type.name,
                                                opname,
                                                node.right.check_type.name))
            elif opname not in node.left.check_type.bin_ops:
                print("Unsupported binary operation %s for type %s" % (opname, node.left.check_type.name))
            else:
                node.check_type = node.left.check_type

    def visit_UnaryOp(self,node):
        self.visit(node.operand)
        opname = node.op.__class__.__name__
        if hasattr(node.operand,"check_type"):
            if opname not in node.operand.check_type.unary_ops:
                print("Unsupported unary operation %s for type %s" % (opname, node.operand.check_type.name))
            else:
                node.check_type = node.operand.check_type

top = ast.parse("2 + 'hello'")
TypeCheck().visit(top)
top = ast.parse("'Hello' - 'World'")
TypeCheck().visit(top)
top = ast.parse("2 + 3 * (4 + 20) % 3")
TypeCheck().visit(top)

checker = TypeCheck()
code = """
a = 23
b = 45
c = "Hello"
d = a + 20 * b - 30
"""
checker.visit(ast.parse(code))
print(checker.symtab)

def check(expr):
    checker.visit(ast.parse(expr))

check("99*d - a + b")
check("99*d - c + b")
check("c + 'World'")
check("c - 'World'")
check("10 + a + b * x")
