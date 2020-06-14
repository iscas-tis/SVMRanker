

int test_fun(int x, int y, int z)
{
    int c = 0;
    while (x < y) {
        if (x < z) {
            x = x + 1;
        } else {
            z = z + 1;
        }
        c = c + 1;
    }
    return c;
}

int main() {
    return test_fun(0, 0, 0);
}


