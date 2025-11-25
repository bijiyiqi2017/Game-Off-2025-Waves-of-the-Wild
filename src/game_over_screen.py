import pygame
from src.settings import *

def draw_game_over():
    SCREEN.fill(RED)
    font = pygame.font.SysFont(None, 70)
    text = font.render("Game Over", True, BLACK)
    SCREEN.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
    pygame.display.flip()
