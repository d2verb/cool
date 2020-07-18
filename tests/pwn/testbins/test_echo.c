#include <stdio.h>
#include <string.h>

int main(void) {
  char buf[128];

  setvbuf(stdout, NULL, _IONBF, 0);

  for(;;) {
    printf(">> ");
    scanf("%217s", buf);
    if (!strncmp(buf, "exit", 5))
      break;
    printf("%s\n", buf);
  }
}
