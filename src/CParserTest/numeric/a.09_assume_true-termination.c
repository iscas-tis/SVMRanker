

int test_fun(int x, int y, int z)
{
    if(y <= 0) {
    	// replace assume
    	return z;
    }
    while (x >= z) {
    	if(y <= 0) {
		// replace assume
		return z;
    	}
        z = z + y;
    }
    return z;
}

int main() {
    return test_fun(0, 0, 0);
}
