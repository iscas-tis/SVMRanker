

int test_fun(int x, int y, int z)
{
    int c = 0;
    while ((x > z) || (y > z)) {
        if (x > z) {
            x = x - 1;
        } else {
            if (y > z) {
                y = y - 1;
            } else {
                
            }
        }
        c = c + 1;
    }
    return c;
}

int main() {
    return test_fun(0, 0, 0);
}
