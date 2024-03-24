import pygame
import random
from enum import Enum
from hud import *
from snake import snaker as paul_muadib_atreides_snake_game

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HUD_WIDTH = 250
HUD_HEIGHT = 600
HUD_BG_COLOR = WHITE#(200, 200, 200)

playercolors = [(255, 0, 0), (0,0,0), (255,105,180), (0, 0, 255)]

continent_names = ["North America", "South America", "Europe", "Africa", "Australia", "Asia"]
continentcolors =  [
    (194, 178, 128), #sand sand
    (150, 75, 0),      # North America (brown)
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
CELL_SIZE = 20
NUM_CONTINENTS = 6
NUM_ROWS = SCREEN_HEIGHT // CELL_SIZE
NUM_COLS = SCREEN_WIDTH // CELL_SIZE
NUM_PLAYERS = 4

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.troops = 0
        self.territories = []
        self.gained = 0

class Continent:
    def __init__(self, name, territories):
        self.name = name
        self.territories = territories
        self.owner = -1
        self.score = len(self.territories) // 2

    def add_territory(self, territory):
        self.territories.append(territory)

    def is_owned(self, player):
        for territory in self.territories:
            if territory.owner != player:
                return False
        self.owner = player
        return True

class Territory:
    def __init__(self, continent=0, troops=1, owner=None, location=None):
        self.continent = continent
        self.troops = troops
        self.owner = owner
        self.color = continentcolors[continent]
        self.location = location

    def is_adjacent(self, other):
        sx, sy = self.location
        ox, oy = other.location
        if sx == ox and (sy == oy + 1 or sy == oy - 1):
            return True
        if sy == oy and (sx == ox + 1 or sx == ox - 1):
            return True
        return False

def generate_grid(rows, cols, NUM_CONTINENTS):
    grid = [[(0, 0, (0,0,0)) for _ in range(cols)] for _ in range(rows)]  # Initialize grid with water ('w')

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
                if cell[0] == 0 and sum_territory(grid, label) < random.randint(20, 30):
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

def max_troops(player: Player, territories, num_players):
    # refresh continents
    continents = [Continent(name=designation, territories=[territory for row in territories for territory in row if territory.continent == designation]) for designation in range(1, NUM_CONTINENTS + 1)]

    # 1 additional troop for every 3 territories above start
    mx_trps = 3

    mx_trps += max(0, player.gained // 3)

    # Continent troop bonus
    for continent in continents:
        if continent.is_owned(player):
            print("here")
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
    path = ["House of Atreides'", "House of Harkonnen's", "House of Corrino's", "Fremen's"]
    img = [0, 0, 0, 0]
    for i in range(4):
        texture=os.path.join(f'{path[i]}.png')
        img[i] = pygame.image.load(texture)
        img[i] = pygame.transform.scale(img[i], (100, 100))
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
            else:
                territories[y][x] = Territory(continent=designation, troops=troops, location = (y,x))

    running = True

    #draw initial territories
    for y, row in enumerate(territories):
        for x, territory in enumerate(row):
            if not territory.continent:
                pygame.draw.rect(screen, territory.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                continue
            pygame.draw.rect(screen, (0,0,0),(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, territory.color, (x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE -2, CELL_SIZE-2))
            draw_hud(screen, 0, 0, img)
            if territory.troops > 0:
                font = pygame.font.Font(None, 24)
                text_surface = font.render(str(territory.troops), True, territory.owner.color)
                text_rect = text_surface.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text_surface, text_rect)

    #game loop
    player_turn = 0
    phase = 0
    selected_attacker = None
    mx_troops = max_troops(players[player_turn], territories, NUM_PLAYERS)
    font = pygame.font.Font(None, 19)
    pygame.draw.rect(screen, WHITE, (800, 225, 250, 30))
    text_surface = font.render(f"Troops left to place: {mx_troops}", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(925, 250))
    screen.blit(text_surface, text_rect)

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
                                mx_troops = max_troops(players[player_turn], territories, NUM_PLAYERS)
                            else:
                                phase = 1
                            draw_hud(screen, phase, player_turn, img)
                            if phase == 0:
                                font = pygame.font.Font(None, 19)
                                pygame.draw.rect(screen, WHITE, (800, 225, 250, 30))
                                text_surface = font.render(f"Troops left to place: {mx_troops}", True, (0, 0, 0))
                                text_rect = text_surface.get_rect(center=(925, 250))
                                screen.blit(text_surface, text_rect)
                        continue
                        #do hud stuff(end attack, end placing troops)

                    #otherwise add troops
                    cell_x = x // CELL_SIZE
                    cell_y = y // CELL_SIZE
                    territory = territories[cell_y][cell_x]

                    if phase and territory.owner is None and selected_attacker is not None and selected_attacker.is_adjacent(territory):
                        sound = Sound(os.path.join('Dune scream song meme.mp3'))
                        sound.play()
                        cells = paul_muadib_atreides_snake_game(screen, territories, x, y, players[player_turn].color)

                        if cells == 0:
                            selected_attacker.troops = 1

                            pygame.draw.rect(screen, selected_attacker.color, (attackx * CELL_SIZE + 1, attacky * CELL_SIZE + 1, CELL_SIZE -2, CELL_SIZE-2))
                            font = pygame.font.Font(None, 24)
                            text_surface = font.render(str(selected_attacker.troops), True, selected_attacker.owner.color)
                            text_rect = text_surface.get_rect(center=(attackx * CELL_SIZE + CELL_SIZE // 2, attacky * CELL_SIZE + CELL_SIZE // 2))
                            screen.blit(text_surface, text_rect)
                            continue

                        cell_y, cell_x = cells
                        new_territory = territories[cell_y][cell_x]

                        if new_territory.owner == players[player_turn]:
                            new_territory.troops += selected_attacker.troops - 1
                            selected_attacker.troops = 1
                        else:
                            while(selected_attacker.troops > 1 and new_territory.troops > 0):
                                attack(screen, selected_attacker, new_territory, True)
                            selected_attacker.troops = 1

                        pygame.draw.rect(screen, selected_attacker.color, (attackx * CELL_SIZE + 1, attacky * CELL_SIZE + 1, CELL_SIZE -2, CELL_SIZE-2))
                        font = pygame.font.Font(None, 24)
                        text_surface = font.render(str(selected_attacker.troops), True, selected_attacker.owner.color)
                        text_rect = text_surface.get_rect(center=(attackx * CELL_SIZE + CELL_SIZE // 2, attacky * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text_surface, text_rect)

                        pygame.draw.rect(screen, new_territory.color, (cell_x * CELL_SIZE + 1, cell_y * CELL_SIZE + 1, CELL_SIZE -2, CELL_SIZE-2))
                        font = pygame.font.Font(None, 24)
                        text_surface = font.render(str(new_territory.troops), True, new_territory.owner.color)
                        text_rect = text_surface.get_rect(center=(cell_x * CELL_SIZE + CELL_SIZE // 2, cell_y * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text_surface, text_rect)

                        selected_attacker = None
                        continue
                    elif territory.owner is None:
                        continue
                    elif territory.owner == players[player_turn] and mx_troops > 0 and not phase:
                        territory.troops += 1
                        mx_troops -= 1
                        font = pygame.font.Font(None, 19)
                        pygame.draw.rect(screen, WHITE, (800, 225, 250, 30))
                        text_surface = font.render(f"Troops left to place: {mx_troops}", True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=(925, 250))
                        screen.blit(text_surface, text_rect)

                        #redraw that tile
                        pygame.draw.rect(screen, territory.color, (cell_x * CELL_SIZE + 1, cell_y * CELL_SIZE + 1, CELL_SIZE -2, CELL_SIZE-2))

                        font = pygame.font.Font(None, 24)
                        text_surface = font.render(str(territory.troops), True, territory.owner.color)
                        text_rect = text_surface.get_rect(center=(cell_x * CELL_SIZE + CELL_SIZE // 2, cell_y * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text_surface, text_rect)
                    elif phase and territory.owner == players[player_turn]:
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
