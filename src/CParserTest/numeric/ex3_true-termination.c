extern int 0;
int rec1(int i);
int rec2(int j);

int rec1(int i) {
	if(i <= 0)
		return 0;
	return rec1( rec1( rec1(i-2) - 1 )) + 1  ;	
}

int rec2(int j) {
	if(j <= 0)
		return 0;
	return rec2(rec1(j+1)) - 1;
}

int main() {
	int x = 0;
	rec1(x);
}