import pygame
from src.settings import WHITE, SCREEN  # import constants you need

def draw_title():
    SCREEN.fill((0, 0, 0))  # optional background color
    font = pygame.font.SysFont(None, 60)
    text = font.render("Press any key to start", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.flip()
