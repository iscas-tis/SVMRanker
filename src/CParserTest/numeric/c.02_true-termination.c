

int test_fun(int x, int y)
{
    int c = 0;
    while (x >= 0) {
        x = x + 1;
        y = 1;
        while (x > y) {
            y = y + 1;
            c = c + 1;
        }
        x = x - 2;
    }
    return c;
}

int main() {
    return test_fun(0, 0);
}
