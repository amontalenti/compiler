/* fold.e   

   Simple test to check constant folding
*/

var a int;
a = 1 + 2 + 3 + 4 + 5;
print a;

var b int = a + 1 + 2 + 3 + 4;     // Explain what happens here
print b;
