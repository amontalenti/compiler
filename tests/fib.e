/* Compute fibonacci numbers */

var a int = 1;
var b int = 1;
var t int;
var n int = 0;
const LAST = 20;

while n < LAST {
    print a;
    t = a + b;
    a = b;
    b = t;
    n = n + 1;
}
