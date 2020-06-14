

int test_fun(int x, int y, int z)
{
    int c = 0;
    while ((x > z) && (y > z)) {
        x = x - 1;
        y = y - 1;
        c = c + 1;
    }
    return c;
}

int main() {
    return test_fun(0, 0, 0);
}
