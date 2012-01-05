def foo(x):
    """Python will do constant folding and make this method equivalent to
    foo_fold."""
    return 1 + 2 + 3 + 4 + x

def foo_fold(x):
    return 10 + x

def baz(x):
    """Python will also do constant folding and make this function equivalent
    to baz_fold."""
    return x + (1 + 2 + 3 + 4)

def baz_fold(x):
    return x + 10

def bar(x):
    """It seems like this method could use constant folding, but Python
    will not fold the expression 1 + 2 + 3 + 4. Why might this be?"""
    return x + 1 + 2 + 3 + 4

def bar_fold(x):
    """Here is the folded version of the function."""
    return x + 10

"""
Perhaps it has to do with Python's support for operator overloading
and operator chaining by associativity rules. chain_add implements 
this in the Python runtime.
"""

def chain_add(*args):
    """Implements chained __add__ call semantics, as
    the Python interpreter might. For example:

        >>> chain_add(1, 2, 3) # like 1.__add__(2).__add__(3)
        6

    Required because calling __add__ directly on an integer
    literal is actually a syntax error in Python, even though
    that's precisely what the interpreter does under the hood.
    """
    i = args[0]
    for j in args[1:]:
        i = getattr(i, "__add__")(j)
    return i

def foo_expanded():
    """
    So, the idea is that for foo, folding can happen on first 4
    arguments because all arguments have a known, int-like implementation
    of __add__.
    """
    return chain_add(1, 2, 3, 4, x)

def baz_expanded():
    """
    In baz, it is also OK -- no matter what, x.__add__ will receive the
    same value, folded or not.
    """
    return x.__add__(chain_add(1, 2, 3, 4))

def bar_expanded():
    """
    In bar, however, we have a problem. Since x__add__ will receive
    the value 1 in the non-folded case, but the value 10 in the folded
    case, an "evil" implementation of X that does not follow kosher
    rules for integer addition may react differently to each of these 
    values.
    """
    return chain_add(x, 1, 2, 3, 4)

class EvilX(object):
    """Here is an evil implementation of x that implements addition 
    in a wonky way. When `other` is 1, it returns 0. But when other
    is greater than 1, it simply returns 15."""
    def __add__(self, other):
        if other == 1:
            return 0
        if other > 1:
            return 15
    """To cause even more confusion, this implementation also makes
    right addition, subtraction, and right subtraction all use exactly
    the same rule."""
    __radd__ = __add__
    __sub__ = __add__
    __rsub__ = __add__

"""We'll now try out this evil x on our functions and see what happens.
To guide in understanding Python's proper constant folding rules, we also
disassemble each of the functions to see Python bytecode."""

import dis
x = EvilX()
dis.dis(foo)
print("foo", foo(x))
dis.dis(baz)
print("baz", baz(x))
dis.dis(bar)
print("bar", bar(x))
dis.dis(bar_fold)
print("bar_fold", bar_fold(x))
assert bar_fold(x) != bar(x)

"""Notice that in the end, bar_fold returns the value 15 whereas bar returns
the value 9. This is thanks to our EvilX. Therefore, bar is not equivalent
to bar_fold, so Python does the right thing by refusing the do constant 
folding on it."""

