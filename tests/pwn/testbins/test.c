// test_x64.elf: gcc -no-pie test.c -o test_x64.elf
// test_x32.elf: gcc -no-pie -m32 test.c -o test_x32.elf

#include <stdio.h>

int main(void)
{
  puts("Hello, World\n");
  return 0;
}
