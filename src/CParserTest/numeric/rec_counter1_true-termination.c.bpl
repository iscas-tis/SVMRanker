procedure rec(a: int)
{
  if ((a==0))
  {
  } else {
    res := rec((a-1));
    rescopy := res;
    while ((rescopy>0))
    {
    rescopy := rescopy - 1;    }
  }

}procedure main()
{
  var i: int;
  var res: int;
  i := __VERIFIER_nondet_int();
  if ((i<=0))
  {
  }

  res := rec(i);
}