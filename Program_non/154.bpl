//Loops.py 7
procedure main() returns () {
    var x0, x1: real;
    while (x0 >= x1) {
        x0, x1 := x0 - 4.0*x1*x1 + 4.0 * x1 + 3.0, x1-2.0;
    }
}
