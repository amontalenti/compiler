# expr.py
'''
The Expr compiler.  Entry point for everything
'''
if __name__ == '__main__':
    import exprlex
    import exprparse
    import exprcheck
    import exprcode
    import exprpygen
    import exprconst

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
            # Fold constants
            program = exprconst.fold_constants(program)
            # Generate 3 address code IR
            code = exprcode.generate_code(program)
            # Emit Python code
            exprpygen.emit_pycode("main", code)
            print("if __name__ == '__main__':")
            print("     main()")
