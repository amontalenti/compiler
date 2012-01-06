/* A simple conditional */

var a int = 2;
var b int = 3;

while a < b {
    a = a + 1;
}
if a < b {
   print "Less than";
} else {
  print "Greater than";
}
