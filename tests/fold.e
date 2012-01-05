/* fold.e   

   Simple test to check constant folding
*/

const a = 1 + 2; // this can fold
print a;

var b int = a + 1 + 2 + 3 + 4; // this can fold because a is const
print b;

var c int = 1 + 2 + 3; // this can fold
var d int = c + 4; // but this cannot fold
