procedure main() returns () {
    var x1, x2: real;
    while (x1 * x1 + x2 * x2 <= 1) {
        x2 := x2 - 2.0*x1 + 1.0;
    }
}