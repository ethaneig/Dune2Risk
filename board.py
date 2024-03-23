from square import Square

class Board:
    def __init__(self):
        self.squares=[[0 for row in range(100)] for col in range(100)]
        self.last_move=None
        self._create()
        print(self.squares)
        #self._add_pieces('white')
        #self._add_pieces('black')

    def _create(self):
        for row in range(100):
            for col in range(100):
                self.squares[row][col] = Square(row, col)
board = Board()
