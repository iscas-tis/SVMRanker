procedure ackermann(m: int, n: int)
{
  if ((m==0))
  {
  }

  if ((n==0))
  {
  }

}procedure main()
{
  var m: int;
  var n: int;
  var result: int;
  m := 0;
  if (((m<0)||(m>3)))
  {
  }

  n := 0;
  if (((n<0)||(n>23)))
  {
  }

  result := ackermann(m,n);
  if ((((m<0)||(n<0))||(result>=0)))
  {
  } else {
    ERROR:     __VERIFIER_error();  }

}