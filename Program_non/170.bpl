//Loops.py 37
procedure main() returns () {
    var x0, x1: real;
    while (x0 >= 1.0 &&x1>=x0) {
        x0, x1 := 3.0*x0, 2.0*x1;
    }
}
