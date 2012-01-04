/* errors.e

   A sample program with a wide variety of semantic errors that must be catch by
   your compiler.

*/

/* Type errors on operators */
var e int;
e = "foo";

print 2 + 2.5;               // Type error : int + float
print 2 + "4";               // Type error : int + string

/* Checks for unsupported operations on strings */

print "Hello" - "World";     // Type error: Unsupported operator - for type string
print "Hello" * "World"; 
print "Hello" / "World";
print +"Hello";
print -"Hello";

/* Assignment to an undefined variable */
b = 2;

/* Assignment to a constant */
const c = 4;
c = 5;

/* Assignment type error */
var d int;
d = 4;       // Good
d = 4.5;     // Bad

/* Bad type names */
var e foo;
var f d;

/* Variable declaration type error */
var g int = 2.5;

/* Propagation of types in expressions */
var h int;
var i float;
var j int = h * i;

/* Undefined variable in an expression */
print 2 + x;

/* Bad location */
print 2 + int;

/* Duplicate definition */

var d float;
var int int;


