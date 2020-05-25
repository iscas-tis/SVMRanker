//#rTermination
/*
 * Date: 2013-01-11
 * Author: leike@informatik.uni-freiburg.de
 *
 * Ranking function: f(x, c) = x;
 * needs the loop invariant c >= 1, which holds over
 * integers, but not over rationals.
 */

procedure NonTerminationOverReals(c: int) returns (x: int)
{
  while (x >= 0) {
    x := x - 2*c + 1;
  }
}
