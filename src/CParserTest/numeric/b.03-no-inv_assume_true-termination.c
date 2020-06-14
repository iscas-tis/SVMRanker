

int test_fun(int x, int y)
{
    if(x <= 0) {
    	// replace assume
        return y;
    }

    while (x > y) {
        y = y + x;
    }
    return y;
}

int main() {
    return test_fun(0, 0);
}
