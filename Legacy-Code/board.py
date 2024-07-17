from square import Square
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


class Board:
    def __init__(self):
        self.cols = 100
        self.rows = 100
        self.squares=[[0 for row in range(self.rows)] for col in range(self.cols)]
        self.last_move=None
        self._create()
        self.plot_board()
        #self._add_pieces('white')
        #self._add_pieces('black')

    def _sum_territory(self, country_label):
        territory_count = 0
        for row in self.squares:
            territory_count += sum(cell.land == country_label for cell in row)
        return territory_count

    def _generate_country(self, row, col, label):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)  # Shuffle the directions
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.squares[new_row][new_col].land == 0 and self._sum_territory(label) < random.randint(10,20):
                self.squares[new_row][new_col].land = label
                self._generate_country(new_row, new_col, label)

    def _create(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.squares[row][col] = Square(row, col, None, 0)


        num_countries = 6 #random.randint(3, 6)  # Random number of countries between 3 and 6
        country_labels = ['c' + str(i) for i in range(1, num_countries + 1)]

        for label in country_labels:
            start_row = random.randint(0, self.rows - 1)
            start_col = random.randint(0, self.cols - 1)
            self._generate_country(start_row, start_col, label)

    def plot_board(self):
        unique_countries = set(np.ravel(self.squares.land))  # Extract unique country labels
        num_countries = len(unique_countries)
        country_to_numeric = {country: i for i, country in enumerate(unique_countries)}

        numeric_grid = np.zeros_like(self.squares.land, dtype=int)
        for i in range(self.cols):
            for j in range(self.rows):
                if self.squares[i][j] != 0:
                    numeric_grid[i][j] = country_to_numeric[self.squares[i][j].land]

        colors = plt.cm.get_cmap('tab10', num_countries)  # Generate unique colors for each country

        cmap = ListedColormap([colors(i) for i in range(num_countries)])
        bounds = list(range(num_countries + 1))
        norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

        plt.figure(figsize=(8, 8))
        plt.imshow(numeric_grid, cmap=cmap, norm=norm)
        plt.colorbar(ticks=range(num_countries), label='Country')
        plt.title('Risk Board')
        plt.xlabel('Columns')
        plt.ylabel('Rows')
        plt.show()
board = Board()
