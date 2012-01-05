/* testrelbad.e

   Code involving bad relations and operations.  You should get a variety
   of errors during type checking.
   */

var a int = 2;
var b int = 3;

print 2 < 2.5;      // Type error:   int < float
print 2 && 3;       // Type error:   int && int

var c bool;
var d bool;
print c && d;       // Good.
print c < d;        // Type error.  Unsupported operator '<'
print c <= d;       // Type error.  Unsupported operator '<='
print c > d;        // Type error.  Unsupported operator '>'
print c >= d;       // Type error.  Unsupported operator '>='
print c == d;       // Good
print c != d;       // Good

print !a;           // Type error. Unsupported operator !
print !c;           // Good.
print !(a<b);       // Good.



