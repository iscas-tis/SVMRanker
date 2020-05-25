//Loops.py 21
procedure main() returns () {
    var x0, x1, x2: real;
    while (x1<=x2 && x0>=1.0 && x1>=1.0) {
        x0, x1, x2 := x0 + 1.0, x1*x0+x1,x2;
    }
}
