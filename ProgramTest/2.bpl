procedure main()
{
  var q: int;
  var a: int;
  var b: int;
  q := __VERIFIER_nondet_int();
  a := __VERIFIER_nondet_int();
  b := __VERIFIER_nondet_int();
  while ((q>0))
  {
  q := ((q+a)-1);
  old_a := a;
  a := ((3*old_a)-(4*b));
  b := ((4*old_a)+(3*b));  }

}