

int test_fun(int i, int j, int k, int tmp)
{
    int c = 0;
    while ((i <= 100) && (j <= k)) {
        tmp = i;
        i = j;
        j = tmp + 1;
        k = k - 1;
        c = c + 1;
    }
    return c;
}

int main() {
    return test_fun(0, 0, 0, 0);
}
