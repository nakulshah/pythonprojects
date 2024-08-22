# Spiral Matrix III
# You start at the cell (rStart, cStart) of an rows x cols grid facing east.
# The northwest corner is at the first row and column in the grid, and the southeast corner is at the
# last row and column.
#
# You will walk in a clockwise spiral shape to visit every position in this grid.
# Whenever you move outside the grid's boundary, we continue our walk outside the grid
# (but may return to the grid boundary later.). Eventually, we reach all rows * cols spaces of the grid.
#
# Return an array of coordinates representing the positions of the grid in the order you visited them.
from typing import List


class Solution(object):
    def spiralMatrixIII(self, rows, cols, rStart, cStart):
        rows: int
        cols: int
        rStart: int
        cStart: int

        ''''
        use x & y
        initialize x with rStart
        initialize y with cStart
        
        x_dir = right
        y_dir = down
        if(x < rows && x >= 0 && y < cols && y >= 0)
            append [x, y]
            if(x_dir == right)
                x = x + 1
            else
                x = x - 1
        else if(x == rows)
            y_dir == down
            y = y + 1
            x = x - 1
            x_dir = left
        else if(x >= rows && x >= 0 && y < cols && y >= 0)
            x = x - 1
            x_dir = left
        else if(x == 0)
            y = y - 1
            y_dir = up
            x_dir = right
        else if(y == 0)
            x = x + 1
            x_dir = right
        '''
        temp_list = [rStart, cStart]

        to_return = [temp_list]

        return to_return


