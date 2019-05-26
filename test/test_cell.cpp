#define CATCH_CONFIG_MAIN

#include "catch.h"
#include "cell.h"

unsigned int simple_test(unsigned int n)
{
  return n;
}


TEST_CASE("Simple test", "[simple]")
{
  REQUIRE(simple_test(0) == 0);
  REQUIRE(simple_test(1) == 1);
}
