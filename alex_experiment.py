import pygame
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
NUM_ROWS = SCREEN_HEIGHT // CELL_SIZE
NUM_COLS = SCREEN_WIDTH // CELL_SIZE
NUM_PLAYERS = 5

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.troops = 0

class Territory:
    def __init__(self, continent=None, troops=0, owner=None):
        self.continent = continent
        self.troops = troops
        self.owner = owner

def generate_grid(rows, cols):
    grid = [[('w0', 0, None) for _ in range(cols)] for _ in range(rows)]  # Initialize grid with water ('w')

    def sum_territory(grid, country_label):
        territory_count = 0
        for row in grid:
            territory_count += sum(cell[0] == country_label for cell in row)
        return territory_count

    def generate_country(row, col, label):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)  # Shuffle the directions
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                cell = grid[new_row][new_col]
                if cell[0] == 'w0' and sum_territory(grid, label) < random.randint(10, 20):
                    grid[new_row][new_col] = (label, 0, None)  # Set continent with 0 troops and no owner
                    generate_country(new_row, new_col, label)

    num_countries = 6  # Random number of countries between 3 and 6
    country_labels = ['c' + str(i) for i in range(1, num_countries + 1)]

    for label in country_labels:
        start_row = random.randint(0, rows - 1)
        start_col = random.randint(0, cols - 1)
        grid[start_row][start_col] = (label, 0, None)  # Set starting continent with 0 troops and no owner
        generate_country(start_row, start_col, label)

    return grid

def draw_grid(screen):
    for y in range(NUM_ROWS):
        for x in range(NUM_COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Risk Game")

    players = [Player(f"Player {i+1}", (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) for i in range(NUM_PLAYERS)]

    territories = [[Territory() for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    # Assign territories to players (randomly for demonstration)
    grid = generate_grid(NUM_ROWS, NUM_COLS)

    for y in range(NUM_ROWS):
        for x in range(NUM_COLS):
            designation, troops, _ = grid[y][x]
            if not designation.startswith('w'):
                territories[y][x] = Territory(continent=designation, troops=troops, owner=random.choice(players))
            else:
                territories[y][x] = Territory(continent=designation, troops=troops)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
                    cell_x = x // CELL_SIZE
                    cell_y = y // CELL_SIZE
                    territory = territories[cell_y][cell_x]
                    if territory.owner == players[0]:  # Only allow player 1 to add troops (for demonstration)
                        territory.troops += 1
                        players[0].troops -= 1

        screen.fill(BLACK)
        draw_grid(screen)
        # Draw territories
        for y, row in enumerate(territories):
            for x, territory in enumerate(row):
                color = territory.owner.color if territory.owner else WHITE
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if territory.troops > 0:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(territory.troops), True, BLACK)
                    text_rect = text_surface.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                    screen.blit(text_surface, text_rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Risk Game")

    players = [Player(f"Player {i+1}", (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) for i in range(NUM_PLAYERS)]

    territories = [[Territory() for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    # Assign territories to players (randomly for demonstration)
    for row in territories:
        for territory in row:
            territory.owner = random.choice(players)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
                    cell_x = x // CELL_SIZE
                    cell_y = y // CELL_SIZE
                    territory = territories[cell_y][cell_x]
                    if territory.owner == players[0]:  # Only allow player 1 to add troops (for demonstration)
                        territory.troops += 1
                        players[0].troops -= 1

        screen.fill(BLACK)
        plot_board(screen)
        # Draw territories
        for y, row in enumerate(territories):
            for x, territory in enumerate(row):
                color = territory.owner.color if territory.owner else WHITE
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if territory.troops > 0:
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(territory.troops), True, BLACK)
                    text_rect = text_surface.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                    screen.blit(text_surface, text_rect)

        pygame.display.flip()

    pygame.quit()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Risk Game")

    grid = generate_grid(NUM_ROWS, NUM_COLS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        plot_board(screen, grid)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
