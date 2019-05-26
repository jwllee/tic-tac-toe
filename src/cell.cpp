#include "cell.h"

bool Cell::is_empty()
{
  return val == MarkerType::null;
}
