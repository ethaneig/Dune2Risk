import pygame
import random

# Define colors
HUD_WIDTH = 250
HUD_HEIGHT = 600
HUD_BG_COLOR = (200, 200, 200)

def attack(screen, attacker, defender):
    # Ensure attacker has at least 2 troops (1 for attacking and 1 for defense)
    player = attacker.owner
    if attacker.troops < 2:
        print("Attacker doesn't have enough troops to attack.")
        return

    if attacker.location[0] != defender.location[0] + 1 and attacker.location[0] != defender.location[0] - 1 and attacker.location[1] != defender.location[1] + 1 and attacker.location[1] != defender.location[1] - 1:
        print("Attack is not against a valid location.")
        return

    if defender.owner == player or defender.continent == 0:
        print("Attack is not against a valid player.")
        return

    if attacker.owner != player:
        print("Player does not control this territory.")
        return

    # Simulate dice rolls for attacker and defender
    attacker_dice_roll = [random.randint(1, 6) for _ in range(min(attacker.troops - 1, 3))]  # Up to 3 dice for attacker
    defender_dice_roll = [random.randint(1, 6) for _ in range(min(defender.troops, 2))]  # Up to 2 dice for defender

    # Sort dice rolls in descending order
    attacker_dice_roll.sort(reverse=True)
    defender_dice_roll.sort(reverse=True)

    # Determine number of battles based on the number of dice rolled by attacker and defender
    num_battles = min(len(attacker_dice_roll), len(defender_dice_roll))

    # Compare dice rolls for each battle
    for i in range(num_battles):
        if attacker_dice_roll[i] > defender_dice_roll[i]:
            # Attacker wins the battle, defender loses 1 troop
            defender.troops -= 1
        else:
            # Defender wins the battle, attacker loses 1 troop
            attacker.troops -= 1

    # Check if defender lost all troops
    if defender.troops <= 0:
        defender.troops = max(1, attacker.troops - 1)
        defender.owner = attacker.owner
        attacker.troops = 1

        print(f"{attacker.owner.name} conquered {defender.location}!")
    else:
        print("Defender successfully defended the territory.")

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