#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <iomanip>


using std::cout;
using std::endl;
using std::setprecision;


double & triple_grade(double& grade)
{
  grade = grade * 3;
  return grade;
}


int main(int argc, char *argv[])
{
  double grade = 0.001;
  setprecision(3);
  cout << "Before: " << grade << endl;
  triple_grade(grade);
  cout << "After: " << grade << endl;
}
