procedure main() returns () {
    var x0, x1: real;
    while (x1*x1 + 10.0 <=x0+6.0*x1 && x0*x0 + 6.0 <= 4.0*x0 +x1) {
        x0, x1 := x0 +x1, x1-1.0;
    }
}
