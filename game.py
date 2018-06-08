from random import randint
from matrix_expansion import findSurroundings

## colors:
## blue = #cfe2f3 < #9fc5e8 < #6fa8dc
## green = #65c680 < #17c651
## red = #c67474 < #c63d3d
## yellow = #ffd966 < #f1c232
##
## \u2620 = skull and bones
## \u2691 = flag

class Square:
    """
    Class representing all squares in the rectangular grid of the game.
    Each square has a tkinter Button as an internal attribute.
    Has also three important attributes: state, value and flag.
    """

    def __init__(self, row, col):
        self._row = row
        self._col = col
        self._state = 0 # 0, 1
        self._value = " " # " ", "1-8", "\u2620"
        self._flag = "" # "\u2691", "?"

    def setButton(self, new_button):
        self._button = new_button

    def getButton(self):
        return self._button

    def getRow(self):
        return self._row

    def getCol(self):
        return self._col

    def getState(self):
        return self._state

    def disable(self):
        self._state = 1
        self._button.config(state="disabled", bg="#cfe2f3",
                            disabledforeground="black",
                            text=self._value)

    def getValue(self):
        return self._value

    def setValue(self, new_value):
        self._value = new_value
        if self._state == 1:
            self._button["text"] = str(new_value)

    def getFlag(self):
        return self._flag

    def setFlag(self, new_flag):
        self._flag = new_flag
        if new_flag: #isn't empty string
            self._button["text"] = str(new_flag)
        else:
            self._button["text"] = " "

class Grid:
    """
    Class containing the game's grid. Every square of the grid
    is a Square object.
    Has methods to handle number of flags, set and count mines,
    expand from a position, and others.
    """

    def __init__(self, height, width, n_mines):
        self._height = height
        self._width = width
        self._n_mines = n_mines

        self._grid = []
        for r in range(height):
            row = []
            for c in range(width):
                sq = Square(r, c)
                row.append(sq)
            self._grid.append(row)

        self._n_flagged_squares = 0

    def getHeight(self):
        return self._height

    def getWidth(self):
        return self._width

    def getNMines(self):
        return self._n_mines

    def getGrid(self):
        return self._grid

    def getSquare(self, row, col):
        return self._grid[row][col]

    def addFlaggedSquare(self):
        self._n_flagged_squares += 1

    def removeFlaggedSquare(self):
        self._n_flagged_squares -= 1

    def getNFlaggedSquares(self):
        return self._n_flagged_squares

    def setMines(self, row, col):
        mines = []
        surr_first = findSurroundings(self._grid, [row, col])

        for n in range(self._n_mines):
            while True:
                mi = randint(0, self._height-1)
                mj = randint(0, self._width-1)
                if [mi, mj] != [row, col] and [mi, mj] not in surr_first \
                   and [mi, mj] not in mines:
                    break
            mines.append([mi, mj])

        for row, col in mines:
            self.getSquare(row, col).setValue("\u2620") #skull and bones

    def countMines(self, row, col):
        surr_pos = findSurroundings(self._grid, [row, col])
        n_mines = 0
        for row, col in surr_pos:
            if self.getSquare(row, col).getValue() == "\u2620":
                n_mines += 1

        return n_mines

    def expandPosition(self, row, col):
       checking = [[row, col]]

       to_check = []

       while checking != []:

           for row, col in checking:
               if self.getSquare(row, col).getState() == 0 \
               and self.getSquare(row, col).getValue() == " ":
                    self.getSquare(row, col).disable()
                    if self.getSquare(row, col).getFlag() == "\u2691":
                        self.removeFlaggedSquare()
                    self.getSquare(row, col).setFlag("")

                    n_mines = self.countMines(row, col)
                    if n_mines > 0:
                        self.getSquare(row, col).setValue(str(n_mines))
                    else:
                        surr_pos = findSurroundings(self._grid, [row, col])
                        for p in surr_pos:
                            if p not in to_check and p not in checking:
                                to_check.append(p)

           checking = to_check[:]
           del to_check[:]

    def showAll(self, win=False, lose=False):
        for r in self._grid:
            for sq in r:
                if win:
                    sq.disable()
                    if sq.getValue() == "\u2620":
                        sq.setFlag("\u2691")
                        sq.getButton()["bg"] = "#6fa8dc"
                        self._n_flagged_squares = self._n_mines
                if lose:
                    if sq.getState() == 0:
                        sq.disable()
                        sq.getButton()["bg"] = "#6fa8dc"
                    else:
                        sq.disable()
                    if sq.getFlag() == "\u2691":
                        if sq.getValue() != "\u2620":
                            sq.getButton().config(text="\u2691",
                                                  disabledforeground="red")
                        else:
                            sq.getButton().config(text="\u2691")
