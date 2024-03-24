import pygame

# Define colors
HUD_WIDTH = 250
HUD_HEIGHT = 600
HUD_BG_COLOR = (200, 200, 200)
def draw_hud(screen, phase, player_turn):
    # Create a surface for HUD
    hud_surface = pygame.Surface((HUD_WIDTH, HUD_HEIGHT))
    hud_surface.fill(HUD_BG_COLOR)
    # Add text to the HUD (for demonstration purposes)
    font = pygame.font.Font(None, 24)
    text_surface = font.render(f"Player {player_turn + 1}'s turn", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(HUD_WIDTH // 2, 50))
    hud_surface.blit(text_surface, text_rect)
    if phase == 0:
        text_surface = font.render("Place Troops", True, (0, 0, 0))
    else:
       text_surface = font.render("Choose Territory to Attack", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(HUD_WIDTH // 2, 100))
    hud_surface.blit(text_surface, text_rect)

    pygame.draw.rect(hud_surface, (255, 0, 0), (50, 300, 150, 50))
    text_surface = font.render("End Action", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(HUD_WIDTH // 2, 325))
    hud_surface.blit(text_surface, text_rect)
    # Blit the HUD onto the screen
    screen.blit(hud_surface, (screen.get_width() - HUD_WIDTH, 0))