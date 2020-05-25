//#rTermination
/*
 * Date: 2013-01-15
 * Author: leike@informatik.uni-freiburg.de
 *
 * Ranking function: f(y) = y
 * with supporting invariant x8 >= x0 + 1.
 *
 * Nevertheless, a more precise supporting invariant
 * x8 >= x0 + 99999999 is discovered.
 */

procedure ExponentialGrowth() returns (y: int, z: int)
{
  var x0, x1, x2, x3, x4, x5, x6, x7, x8: int;
  while (y >= 0) {
    y := y - x8 + x0;
  }
}
