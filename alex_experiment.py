import random
import matplotlib.pyplot as plt

def generate_grid(rows, cols):
    grid = [[0] * cols for _ in range(rows)]  # Initialize grid with all elements as 0 (water)

    for i in range(rows): # Markov Chain Process for Generating Land
        for j in range(cols):
            if i == 0 and j == 0:
                continue  # Skip the first cell since it's always water
            if j == 0:  # First column
                if grid[i - 1][j] == 1:  # If the previous cell is land
                    grid[i][j] = 1 if random.random() < 0.85 else 0  # 80% chance of land
                else:
                    grid[i][j] = 1 if random.random() < 0.1 else 0  # 20% chance of land
            if i == 0:  # First row
                if grid[i][j - 1] == 1:  # If the previous cell is land
                    grid[i][j] = 1 if random.random() < 0.85 else 0  # 80% chance of land
                else:
                    grid[i][j] = 1 if random.random() < 0.1 else 0  # 20% chance of land
            else:  # Remaining columns
                if grid[i - 1][j - 1] + grid[i][j - 1] + grid[i - 1][j] > 1.5:  # Refer to left corner square
                    grid[i][j] = 1 if random.random() < 0.85 else 0  # 80% chance of land
                else:
                    grid[i][j] = 1 if random.random() < 0.1 else 0  # 20% chance of land

    return grid

def visualize_grid(grid):
    plt.imshow(grid, cmap='ocean', interpolation='nearest')
    plt.colorbar(ticks=[0, 1], label='Land (1) - Water (0)')
    plt.title('Grid Visualization')
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.show()

# Example usage:
rows = 20
cols = 20
grid = generate_grid(rows, cols)

# Assuming 'grid' is your generated grid
visualize_grid(grid)
