

int test_fun(int x, int tmp)
{
    tmp = 0;
    while ((x > 0) && (x == 2*tmp)) {
        x = x - 1;
        tmp = 0;
    }
    return x;
}

int main() {
    return test_fun(0, 0);
}
