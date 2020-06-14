

int iterate(int bound) {
  int i;
  int sum = 0;
  for(i=0; i<bound; i++) {
    sum += i;
  }
  return sum;
}

int main() {
    return iterate(0);
}
