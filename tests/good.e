/* Good Expr code */

const a = 1;
const b = 2;
var c int = a + b + 3;
print c;            // Should output 6

var d int = c + 4;
print d;            // Should output 4

var e int = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9;
print e;            // Should output 45

print 2*3 - 1;      // Should output 5
print 10 - 3 - 2;   // Should output 5

print 2.0 / 4.0;  // Should output 0.5
print -b;        // Should output -2

/* Test some floats */
const pi = 3.14159;
var twopi float = 2.0*pi;

print pi;
print twopi;

/* Test some strings */
var s1 string = "hello";
var s2 string = "world";
print s1;
print s2;
print s1+s2;
