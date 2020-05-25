//Loops.py 30
procedure main() returns () {
    var x0, x1: real;
    while (x0 > 0.0 ) {
    	if(x1>0.0){
    		x0, x1 := x0 - x1 -1.0, x1;
    	}
    	else{
    		x0, x1 := x0 + x1 -1.0, x1;
    	}
    }
}
