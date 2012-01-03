import re

# some basic lexing regexes
NUMBER = r'(?P<NUMBER>\d+)'
ID = r'(?P<ID>[a-zA-Z_][a-zA-Z0-9_]*)'
WS = r'(?P<WS>\s+)'

# a tokenizer generator using a master pattern and regexes
def tokenizer(pat,text):
    index = 0
    while index < len(text):
        m = pat.match(text,index)
        if m:
            yield m
            index = m.end()
        else:
            raise SyntaxError("Bad char %r" % text[index])

# some sample text
text = "12345 foo"

# creates a master pattern by joining that
pat = re.compile("|".join([NUMBER, ID, WS]))

print("Part a")

# print token stream
for m in tokenizer(pat, text):
    tok = (m.lastgroup, m.group())
    print(tok)

print("Part b")

ASSIGN = r'(?P<ASSIGN>=)'
EQ = r'(?P<EQ>==)'

# ordering matters
master = "|".join([NUMBER,ID,WS,EQ,ASSIGN])
pat = re.compile(master)
text2 = "a = b == c"
for m in tokenizer(pat, text2):
    tok = (m.lastgroup,m.group())
    print(tok)

print("Part c")

# keyword matching is a better approach than using regexes for those
FOR = r'(?P<FOR>for)'
master = "|".join([NUMBER,ID,WS,EQ,ASSIGN])
pat = re.compile(master)
keywords = {'for': 'FOR', 'if': 'IF', 'while': 'WHILE'}
text3 = "if 5"
for m in tokenizer(pat, text3):
    tokname = m.lastgroup
    tokvalue = m.group()
    if tokname == "ID":
        tokname = keywords.get(tokvalue, "ID")
    tok = (tokname,tokvalue)
    print(tok)

