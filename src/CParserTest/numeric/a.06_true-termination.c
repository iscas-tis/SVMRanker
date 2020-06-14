

int test_fun(int x, int y, int z)
{
    int c = 0;
    while (x > y + z) {
        y = y + 1;
        z = z + 1;
        c = c + 1;
    }
    return c;
}

int main() {
    return test_fun(0, 0, 0);
}
