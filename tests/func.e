/* Sample function definitions */

var lastfib int = 20;
const startcount = 10;

    func add(x int, y int) int {
         return x+y;
    }

    func fibonacci(n int) int {
         if n > 1 {
            return fibonacci(n-1) + fibonacci(n-2);
         } else {
            return 1;
         }
     }

     func countdown(n int) int {
         while n > 0 {
              print n;
              n = n - 1;
         }
         print "Boom!";
         return 0;
     }

     func main() int {
         var n int = 0;
         print add(2,3);
	 while n < lastfib {
	    print fibonacci(n);
            n = n + 1;
         }
	 n = countdown(startcount);
	 return 0;
      }
          