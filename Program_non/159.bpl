//Loops.py 12
procedure main() returns () {
    var x0, x1: real;
    while (1.0 <= x0 && x1 *x1 + 2.0 *x0 <=3.0*x1) {
        x0, x1 := 1.0+1.0/(x0*x0), 0.0 - x1*x0 - 3.0 *x1 +x1*x1 + 1.0;
    }
}
