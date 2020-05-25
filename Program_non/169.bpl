//Loops.py 35
procedure main() returns () {
    var x0: int;
    while (x0!=0) {
    	if(x0 > 0)
    	{
        	x0 := 0-x0 + 1;
    	}
    	else
    	{
    		x0 := 0-x0 - 1;
    	}
    }
}
