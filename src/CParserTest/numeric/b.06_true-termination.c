

int test_fun(int x, int y)
{
    int c = 0;
    while ((x > 0) && (y > 0)) {
        x = x - 1;
        y = y - 1;
        c = c + 1;
    }
    return c;
}

int main() {
    return test_fun(0, 0);
}
