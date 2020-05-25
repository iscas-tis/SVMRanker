//Loops.py 18
procedure main() returns () {
    var x0, x1, x2: real;
    while (0.0<=x0 && x1-2.0*x0>=x2 && x2>=1.0) {
        x0, x1, x2 := 0.0 - x0*x0 - 4.0*x1*x1 + x2*x2, 0.0 - x0*x1 - x2*x2, x2*x2;
    }
}
