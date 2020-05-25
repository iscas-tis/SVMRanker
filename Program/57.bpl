//#rTerminationDerivable
/*
 * Date: 09.07.2013
 * Author: heizmann@informatik.uni-freiburg.de
 *
 * Ranking function: f(x) = x
 */

var x: int;

procedure main() returns (x: int, y: int)
modifies x;
{
  while (true) {
    assume (x >= 0);
    x := x - 1;
  }
}
