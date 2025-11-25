import pygame
from src.settings import *

def draw_win():
    SCREEN.fill((255, 215, 0))  # Gold background
    font = pygame.font.SysFont(None, 70)
    text = font.render("You Win!", True, BLACK)
    SCREEN.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
    pygame.display.flip()
