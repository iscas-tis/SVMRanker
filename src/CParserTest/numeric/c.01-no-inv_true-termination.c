

int test_fun(int x, int y)
{
    int c = 0;
    while (x >= 0) {
        y = 1;
        while (x > y) {
            y = 2*y;
            c = c + 1;
        }
        x = x - 1;
    }
    return c;
}

int main() {
    return test_fun(0, 0);
}
