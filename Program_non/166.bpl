//Loops.py 27
procedure main() returns () {
    var x0, x1, x2: real;
    while ((x0<0.0 || x0>0.0) && x1>=0.0 && x0 >=0.0 && x2>=x0 && x2>=x1 && x2 ==10.0) {
    	if(x1>0.0){
        	x0, x1, x2 := x0, x1-1.0,x2;
    	}
    	else{
        	x0, x1, x2 := x0 - 1.0, x2,x2;
        }
    }
}
