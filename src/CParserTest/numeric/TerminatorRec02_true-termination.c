// public class TerminatorRec02 {
	// public static void main(String[] args) {
		// fact(args.length);
	// }

	// public static int fact(int x) {
		// if (x > 1) {
			// int y = fact(x - 1);
			// return y * x;
		// }
		// return 1;
	// }
// }



int fact(int x) {
		if (x > 1) {
			int y = fact(x - 1);
			return y * x;
		}
		return 1;
	}

int main() {
	int x = 0;
	if(x < 0)
		return 0;
	int y = 0;
	if(y < 0) 
		return 0;
	int z = 0;
	fact(x);

}
