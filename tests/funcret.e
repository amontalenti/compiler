/* Test some return statement errors */

func error4(x int) int {   // No return statement
     print x;
}

func error5(x int) int {  // No return
     if x < 0 {
          return -x;
     }
}

func noterror6(x int) int {
    if x < 0 {
         return -x;
    } else {
         return +x;
    }
}
