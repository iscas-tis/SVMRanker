extern int __VERIFIER_nondet_int(void);

int main()
{
	int q = __VERIFIER_nondet_int();
	int a = __VERIFIER_nondet_int();
	int b = __VERIFIER_nondet_int();
	while (q > 0) {
		q = q + a - 1;
		int old_a = a;
		a = 3*old_a - 4*b;
		b = 4*old_a + 3*b;
	}
	return 0;
}