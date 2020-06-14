

int test_fun(int x, int y)
{
    int c = 0;
    while (x + y > 0) {
        if (x > y) {
            x = x - 1;
        } else {
            if (x == y) {
                x = x - 1;
            } else {
                y = y - 1;
            }
        }
        c = c + 1;
    }
    return c;
}

int main() {
    return test_fun(0, 0);
}
