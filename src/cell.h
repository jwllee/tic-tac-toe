#ifndef CELL_H
#define CELL_H

#include "marker_type.h"

class Cell {
    public:
        int row, col;
        MarkerType val;

        Cell(): row(0), col(0), val(MarkerType::null) { };
        bool is_empty();
}

#endif //CELL_H
