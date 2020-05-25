//Loops.py 15
procedure main() returns () {
    var x0, x1, x2: real;
    while (5.0*x0*x0 + 4.0*x2*x2 <=40.0*x1 && x1+x2<= 0.0-1.0) {
        x0, x1, x2 := x0 +x1, x0+x2,x2-x2*x2-1.0/(x2*x2);
    }
}
