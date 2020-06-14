procedure test_fun(i: int, j: int, k: int, tmp: int)
{
  var c: int;
  c := 0;
  while (((i<=100)&&(j<=k)))
  {
  tmp := i;
  i := j;
  j := (tmp+1);
  k := (k-1);
  c := (c+1);  }

}procedure main()
{

}