

int test_fun(int x, int y, int tmp)
{
    while (x > y) {
        tmp = x;
        x = y;
        y = tmp;
    }
    return tmp;
}

int main() {
    return test_fun(0, 0, 0);
}
