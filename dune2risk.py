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
    grid = [[(0, 0, (0,0,0)) for _ in range(cols)] for _ in range(rows)]  # Initialize grid with sand

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

    owned = 0

    # Continent troop bonus
    for continent in continents:
        if continent.is_owned(player):
            mx_trps += continent.score
            owned += 1

    if owned == len(continents):
        return -1

    return mx_trps

def draw_square(screen, loc, f_color, s_color, text):
    x, y = loc
    pygame.draw.rect(screen, s_color, (x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2))
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, f_color)
    text_rect = text_surface.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
    screen.blit(text_surface, text_rect)
    return None

def update_hud(screen, text):
    font = pygame.font.Font(None, 19)
    pygame.draw.rect(screen, WHITE, (800, 225, 250, 30))
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(925, 250))
    screen.blit(text_surface, text_rect)
    return None

def update_territories(screen, territories):
    for y, row in enumerate(territories):
        for x, territory in enumerate(row):
            if not territory.continent:
                pygame.draw.rect(screen, territory.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                continue
            pygame.draw.rect(screen, (0,0,0),(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, territory.color, (x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE -2, CELL_SIZE-2))
            if territory.troops > 0:
                font = pygame.font.Font(None, 24)
                text_surface = font.render(str(territory.troops), True, territory.owner.color)
                text_rect = text_surface.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    flags = pygame.SCALED
    screen = pygame.display.set_mode([SCREEN_WIDTH+HUD_WIDTH, SCREEN_HEIGHT], flags, vsync=1)
    screen.fill(BLACK)
    draw_grid(screen)
    pygame.display.set_caption("Risk Game")
    clock = pygame.time.Clock()
    clock.tick(10)
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
    texture=os.path.join(f'knife_chip_shatter.jpg')
    img2 = pygame.image.load(texture)
    img2 = pygame.transform.scale(img2, (1050, 600))
    img_center = (525, 300)
    texture_rect = img2.get_rect(center = img_center)
    screen.blit(img2,texture_rect)
    font = pygame.font.Font("Dune_Rise.ttf", 36)
    text_surface = font.render(f"May Thy Knife Chip and Shatter", True, (255,0,0))
    text_rect = text_surface.get_rect(center=(525, 100))
    screen.blit(text_surface, text_rect)
    font = pygame.font.Font("Dune_Rise.ttf", 24)
    text_surface = font.render(f"Click to start", True, (255,0,0))
    text_rect = text_surface.get_rect(center=(525, 135))
    screen.blit(text_surface, text_rect)
    sound = Sound(os.path.join('lisanalgaib.mp3'))
    sound.play()
    pygame.display.flip()

    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                break

    #draw initial territories
    update_territories(screen, territories)
    draw_hud(screen, 0, 0, img)

    #game loop
    player_turn = 0
    phase = 0
    selected_attacker = None
    mx_troops = max_troops(players[player_turn], territories, NUM_PLAYERS)
    update_hud(screen, f"Troops left to place: {mx_troops}")

    while mx_troops + 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Quiting :(
                mx_troops = -1
                break
            elif event.type == pygame.MOUSEBUTTONDOWN: #click
                x, y = event.pos

                #Clicking hud
                if x > SCREEN_WIDTH:
                    if x > 850 and x < 950 and y > 300 and y < 350:
                        if phase == 1:
                            player_turn += 1
                            if player_turn == NUM_PLAYERS :
                                player_turn = 0
                            phase = 0
                            mx_troops = max_troops(players[player_turn], territories, NUM_PLAYERS)
                        else:
                            phase = 1
                        draw_hud(screen, phase, player_turn, img)
                        if phase == 0:
                            update_hud(screen, f"Troops left to place: {mx_troops}")
                    continue

                # Troop Placing Phase
                elif phase == 0:
                    cell_x = x // CELL_SIZE
                    cell_y = y // CELL_SIZE
                    territory = territories[cell_y][cell_x]
                    if territory.owner == players[player_turn] and mx_troops > 0:
                        territory.troops += 1
                        mx_troops -= 1
                        update_hud(screen, f"Troops left to place: {mx_troops}")
                        draw_square(screen, (cell_x, cell_y), territory.owner.color, territory.color, str(territory.troops))

                # Attacking Phase
                elif phase == 1:
                    cell_x = x // CELL_SIZE
                    cell_y = y // CELL_SIZE
                    territory = territories[cell_y][cell_x]

                    #Select territory to attack with
                    if territory.owner == players[player_turn]:
                        selected_attacker = territory
                        attackx = cell_x
                        attacky = cell_y
                        continue

                    #Select territory to attack
                    elif selected_attacker is not None and selected_attacker.is_adjacent(territory) and selected_attacker.troops > 1:

                        #Perform the attack
                        if territory.owner is not None:
                            attack(screen, selected_attacker, territory)
                            draw_square(screen, (attackx, attacky), selected_attacker.owner.color, selected_attacker.color, str(selected_attacker.troops))
                            draw_square(screen, (cell_x, cell_y), territory.owner.color, territory.color, str(territory.troops))
                            selected_attacker = None

                        #SNAKE TIMEEEEEEEE
                        else:
                            cells = paul_muadib_atreides_snake_game(screen, territories, x, y, players[player_turn].color)
                            sound = Sound(os.path.join('Dune scream song meme.mp3'))
                            sound.play()

                            #Unsuccessful
                            if cells == 0:
                                selected_attacker.troops = 1
                                pygame.draw.rect(screen, (255, 255, 255), (800, 225, 250, 60))
                                text_surface = font.render(f"Shai Hulud killed your troops", True, (0, 0, 0))
                                text_rect = text_surface.get_rect(center=(925, 250))
                                screen.blit(text_surface, text_rect)
                                draw_square(screen, (attackx, attacky), selected_attacker.owner.color, selected_attacker.color, str(selected_attacker.troops))
                                update_territories(screen, territories)

                            #Successful, attacks target territory
                            else:
                                cell_y, cell_x = cells
                                new_territory = territories[cell_y][cell_x]
                                if new_territory.owner == players[player_turn]:
                                    if new_territory != selected_attacker:
                                        new_territory.troops += selected_attacker.troops - 1
                                        selected_attacker.troops = 1
                                else:
                                    while(selected_attacker.troops > 1 and new_territory.troops > 0):
                                        attack(screen, selected_attacker, new_territory, True)
                                    selected_attacker.troops = 1
                                draw_square(screen, (attackx, attacky), selected_attacker.owner.color, selected_attacker.color, str(selected_attacker.troops))
                                draw_square(screen, (cell_x, cell_y), new_territory.owner.color, new_territory.color, str(new_territory.troops))
                                update_territories(screen, territories)

                        selected_attacker = None

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
