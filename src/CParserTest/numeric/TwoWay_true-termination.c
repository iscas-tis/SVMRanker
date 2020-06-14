// package TwoWay;

// public class TwoWay {
	// public static void main(String[] args) {
		// Random.args = args;
		// twoWay(true, Random.random());
	// }

	// public static int twoWay(boolean terminate, int n) {
		// if (n < 0) {
			// return 1;
		// } else {
			// int m = n;
			// if (terminate) {
				// m--;
			// } else {
				// m++;
			// }
			// return m*twoWay(terminate, m);
		// }
	// }
// }



int twoWay(int terminate, int n) {
		if (n < 0) {
			return 1;
		} else {
			int m = n;
			if (terminate) {
				m--;
			} else {
				m++;
			}
			return m*twoWay(terminate, m);
		}
	}

int main() {
	int x = 0;
	if(x < 0)
		return 0;
	int y = 0;
	if(y < 0) 
		return 0;
	int z = 0;
	twoWay(1,x);

}
