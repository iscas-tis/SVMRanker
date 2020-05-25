//#rTerminationDerivable
/*
 * Date: 2014-06-13
 * Author: heizmann@informatik.uni-freiburg.de
 *
 * Ranking function: f(x) = x
 *
 */
var x : int;
const c : int;

//axiom c >= 1;

procedure main() returns ()
modifies x;
{
  while (x >= 0) {
    x := x - c;
  }
}

