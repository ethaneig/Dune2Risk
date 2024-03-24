import pygame
import random
from enum import Enum
from hud import *

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HUD_WIDTH = 250
HUD_HEIGHT = 600
HUD_BG_COLOR = (200, 200, 200)

playercolors = [(0,0,0), (150, 75, 0), (255, 0, 0)]

continent_names = ["North America", "South America", "Europe", "Africa", "Australia", "Asia"]
continentcolors =  [
    (0, 0, 255), #blue water
    (255,105,180),      # North America (pink)
    (255, 165, 0),    # South America (Orange)
    (255, 255, 0),    # Europe (Yellow)
    (0, 128, 0),      # Africa (Green)
    (128, 0, 128),     # Australia (Purple)
    (0, 255, 255)  #asian(aqua)
]

# Define constants
num_countries = 6
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
NUM_CONTINENTS = 6
NUM_ROWS = SCREEN_HEIGHT // CELL_SIZE
NUM_COLS = SCREEN_WIDTH // CELL_SIZE
NUM_PLAYERS = 2

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.troops = 0
        self.territories = []

    def update_territories():
        self.territories = [territory for territory in territory if territory.owner == self]

class Continent:
    def __init__(self, name, territories):
        self.name = name
        self.territories = territories
        self.owned = 0
        self.score = len(self.territories) // 2

    def add_territory(self, territory):
        self.territories.append(territory)

    def is_owned(player):
        for territory in self.territories:
            if territory.owner != player:
                return False
        self.owned = players.index(player)
        return True

class Territory:
    def __init__(self, continent=0, troops=1, owner=None, location=None):
        self.continent = continent
        self.troops = troops
        self.owner = owner
        self.color = continentcolors[continent]
        self.location = location

def generate_grid(rows, cols, NUM_CONTINENTS):
    grid = [[(0, 0, None) for _ in range(cols)] for _ in range(rows)]  # Initialize grid with water ('w')

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
                if cell[0] == 0 and sum_territory(grid, label) < random.randint(10, 20):
                    grid[new_row][new_col] = (label, 0, None)  # Set continent with 0 troops and no owner
                    generate_country(new_row, new_col, label)

    country_labels = [i for i in range(1, NUM_CONTINENTS + 1)]

    for label in country_labels:
        start_row = random.randint(0, rows - 1)
        start_col = random.randint(0, cols - 1)
        while(grid[start_row][start_col][1]):
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

def max_troops(player: Player, territories, continents, num_players):

    mx_trps = player.troops

    # 1 additional troop for every 3 territories above start
    mx_trps += (player.territories - len(territories) // num_players) // 3

    # Continent troop bonus
    for continent in continents:
        if player == continent.owner:
            mx_trps += continent.score

    return mx_trps

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH+HUD_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    draw_grid(screen)
    pygame.display.set_caption("Risk Game")
    global playercolors
    players = [Player(f"Player {i+1}", (playercolors[i])) for i in range(NUM_PLAYERS)]

    territories = [[Territory() for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

    # assign territories to players (randomly for demonstration)
    grid = generate_grid(NUM_ROWS, NUM_COLS, NUM_CONTINENTS)

    # generate territories
    continents = []

    for name in range(1,NUM_CONTINENTS + 1):
        continents.append(Continent(name, []))

    for y in range(NUM_ROWS):
        for x in range(NUM_COLS):
            designation, troops, _ = grid[y][x]
            if designation:
                territories[y][x] = Territory(continent=designation, troops=random.randint(1,3), owner=random.choice(players), location = (y,x))
                continents[designation - 1].add_territory(territories[y][x])
            else:
                territories[y][x] = Territory(continent=designation, troops=troops, location = (y,x))

    # generate continents
    continents = list()

    for continent in range(1,7):
        continents.append(Continent(continent, territories))

    running = True

    #draw initial territories
    for y, row in enumerate(territories):
        for x, territory in enumerate(row):
            if not territory.continent:
                pygame.draw.rect(screen, territory.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                continue
            pygame.draw.rect(screen, (0,0,0),(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, territory.color, (x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE -2, CELL_SIZE-2))
            draw_hud(screen, 0, 0)
            if territory.troops > 0:
                font = pygame.font.Font(None, 24)
                text_surface = font.render(str(territory.troops), True, territory.owner.color)
                text_rect = text_surface.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text_surface, text_rect)

    #game loop
    player_turn = 0
    phase = 0
    selected_attacker = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
                    if(x > SCREEN_WIDTH):
                        if(x > 850 and x < 950 and y > 300 and y < 350):
                            if phase == 1:
                                player_turn += 1
                                if(player_turn == NUM_PLAYERS):
                                    player_turn = 0
                                phase = 0
                            else:
                                phase = 1
                            draw_hud(screen, phase, player_turn)
                        continue
                        #do hud stuff(end attack, end placing troops)

                    #otherwise add troops
                    cell_x = x // CELL_SIZE
                    cell_y = y // CELL_SIZE
                    territory = territories[cell_y][cell_x]

                    #if it's the right player
                    if territory.owner == players[player_turn] and not phase:  # Only allow player 1 to add troops (for demonstration)
                        territory.troops += 1
                        players[player_turn].troops -= 1

                        #redraw that tile
                        pygame.draw.rect(screen, territory.color, (cell_x * CELL_SIZE + 1, cell_y * CELL_SIZE + 1, CELL_SIZE -2, CELL_SIZE-2))

                        font = pygame.font.Font(None, 24)
                        text_surface = font.render(str(territory.troops), True, territory.owner.color)
                        text_rect = text_surface.get_rect(center=(cell_x * CELL_SIZE + CELL_SIZE // 2, cell_y * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text_surface, text_rect)
                    elif phase and territory.owner == players[player_turn]:
                        print("Choose Territory to Attack")
                        selected_attacker = territory
                        attackx = cell_x
                        attacky = cell_y
                        continue
                    elif phase and selected_attacker is not None:
                        attack(screen, selected_attacker, territory)

                        pygame.draw.rect(screen, selected_attacker.color, (attackx * CELL_SIZE + 1, attacky * CELL_SIZE + 1, CELL_SIZE -2, CELL_SIZE-2))
                        font = pygame.font.Font(None, 24)
                        text_surface = font.render(str(selected_attacker.troops), True, selected_attacker.owner.color)
                        text_rect = text_surface.get_rect(center=(attackx * CELL_SIZE + CELL_SIZE // 2, attacky * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text_surface, text_rect)

                        pygame.draw.rect(screen, territory.color, (cell_x * CELL_SIZE + 1, cell_y * CELL_SIZE + 1, CELL_SIZE -2, CELL_SIZE-2))
                        font = pygame.font.Font(None, 24)
                        text_surface = font.render(str(territory.troops), True, territory.owner.color)
                        text_rect = text_surface.get_rect(center=(cell_x * CELL_SIZE + CELL_SIZE // 2, cell_y * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text_surface, text_rect)

                        selected_attacker = None


        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
