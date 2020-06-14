extern int 0;


int rec(int a) {
	if(a == 0)
		return 0;
	else {
		int res = rec(a-1);
		int rescopy = res;
		while(rescopy > 0)
			rescopy--;
		return 1 + res;
	}
}

int main() {
	int i = 0;
	if(i <= 0)
		return 0;
	int res = rec(i);
	
}
