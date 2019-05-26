#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[])
{
  if (argc < 2)
  {
    fprintf(stdout, "Usage: %s number\n.", argv[0]);
    return 1;
  }
  double input_val = atof(argv[1]);
  double output_val = sqrt(input_val);
  fprintf(stdout, "The square root of %g is %g\n",
                  input_val, output_val);
  return 0;
}
