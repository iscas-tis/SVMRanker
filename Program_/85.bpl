//#rNonTermination
/*
 * Date: 2014-07-11
 * Author: leike@informatik.uni-freiburg.de
 *
 * 
 */

procedure main() returns ()
{
  var q, a, b: real;
  while (q < 0.0) {
    q    := q + a - 1.0;
    a, b := 0.6*a - 0.8*b, 0.8*a + 0.6*b;
  }
}
