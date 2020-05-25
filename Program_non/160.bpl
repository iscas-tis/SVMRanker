//Loops.py 13
procedure main() returns () {
    var x0, x1: real;
    while (x0 >= 0.0 && 1.0+8.0*x0*x0*x0 <= x1*x1*x1 + x1 - 4.0 * x1*x1) {
        x0, x1 := 0.0-x0*x0-4.0*x1*x1+x1, 0.0-x1*x0-1.0/(x1+1);
    }
}
