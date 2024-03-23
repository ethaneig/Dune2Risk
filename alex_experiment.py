import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def generate_grid(rows, cols):
    grid = [['w0' for _ in range(cols)] for _ in range(rows)]  # Initialize grid with water ('w')

    def sum_territory(grid, country_label):
        territory_count = 0
        for row in grid:
            territory_count += sum(cell == country_label for cell in row)
        return territory_count

    def generate_country(row, col, label):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)  # Shuffle the directions
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row][new_col] == 'w0' and sum_territory(grid, label) < random.randint(10,20):
                grid[new_row][new_col] = label
                generate_country(new_row, new_col, label)


    num_countries = 6 #random.randint(3, 6)  # Random number of countries between 3 and 6
    country_labels = ['c' + str(i) for i in range(1, num_countries + 1)]

    for label in country_labels:
        start_row = random.randint(0, rows - 1)
        start_col = random.randint(0, cols - 1)
        generate_country(start_row, start_col, label)

    return grid

# Example usage:
rows = 15
cols = 15
grid = generate_grid(rows, cols)

def plot_board(grid):
    unique_countries = set(np.ravel(grid))  # Extract unique country labels
    num_countries = len(unique_countries)
    country_to_numeric = {country: i for i, country in enumerate(unique_countries)}

    numeric_grid = np.zeros_like(grid, dtype=int)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 'w':
                numeric_grid[i][j] = country_to_numeric[grid[i][j]]

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