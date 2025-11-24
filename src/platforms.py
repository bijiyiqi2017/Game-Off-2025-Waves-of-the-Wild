import pygame
from src.settings import PLATFORM_COLOR

class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, PLATFORM_COLOR, self.rect)
