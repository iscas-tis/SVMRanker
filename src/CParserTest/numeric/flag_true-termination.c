

int f(int x, int y)
{
    int flag = 1;
    int c = 0;
    while (flag) {
        flag = (x++ < y);
        c = c + 1;
    }
    return c;
}

int main() {
    return f(0, 0);
}
