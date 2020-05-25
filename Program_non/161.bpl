//Loops.py 14
procedure main() returns () {
    var x0, x1, x2: real;
    while (x0>=0.0 && x0+x1>=0.0) {
        x0, x1, x2 := x0 +x1+(x2-1.0)/(1.0+x2*x2), 0.0 -x2*(x2+1.0)/(1.0+x2*x2),x2*x2;
    }
}
