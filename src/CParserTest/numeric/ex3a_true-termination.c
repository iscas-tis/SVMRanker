

int test_fun(int x)
{
    int c = 0;
    while ((x > 1) && (x < 100)) {
        x = x*x;
        c = c + 1;
    }
    return c;
}

int main() {
    return test_fun(0);
}
