import sys

def printstack():
    frame = sys._getframe()      # Get current stack frame
    while frame:
            print("[%s]" % frame.f_code.co_name)
            print("   Locals: %s" % list(frame.f_locals))
            frame = frame.f_back  # Go to next frame

def recursive(n):
    if n > 0:
            recursive(n-1)
    else:
            printstack()

import dis
dis.dis(recursive)
recursive(5)
