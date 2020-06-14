

int test_fun(int x, int y, int r)
{
    r = 1;
    while (y > 0) {
        r = r*x;
        y = y - 1;
    }
    return r;
}

int main() {
    return test_fun(0, 0, 0);
}
