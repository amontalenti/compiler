# codegen.py

'''
Generic code generator class for 3-address code instruction sequences.
The base class CodeEmitter simply walks through the instruction
sequence and dispatches opcodes for the form (opcode, arg1, arg2, ...)
to a method of the name emit_opcode(arg1, arg2, ...).

Actual code generators should inherit from this class and implement
the required emit_opcode() methods.

The programming interface is based on generators.  It should be used
roughly like this:

     top = parse()           # Get the AST
     code = generate_code()  # Generate the 3-address code
     emitter = SomeCodeEmitter()
     for s in emitter.process(code):
          # Do something with s

s can be anything at all, but a common output might be a line of text.
'''

class CodeEmitter(object):
    def process(self,instructions):
        for inst in instructions:
            opcode = inst[0]
            args = inst[1:]
            methname = "emit_" + opcode
            if hasattr(self,methname):
                result = getattr(self,methname)(*args)
                if isinstance(result,list):
                    for line in result:
                        yield line
                else:
                    yield result
            else:
                raise RuntimeError("No method %s" % methname)



    

    
