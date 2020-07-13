int main(){
	int x;
	int y;
	int oldx;
	while(4*x + y >= 1){
		oldx = x;
		x = 4*y - 2*x;
		y = 4*oldx;
	}
}
