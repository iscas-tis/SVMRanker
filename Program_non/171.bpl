//Loops.py 38
procedure main() returns () {
    var x0, x1: real;
    while (x0 >=0.0 && x1>= 0.0 ) {
        x0, x1 := 0.0 - x0 - 3.0*x1 + 2.0, 0.0-4.0*x0*x0+x1-1.0;
    }
}
