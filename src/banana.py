import pygame
import random

class Banana:
    def __init__(self):
        self.image = pygame.image.load("assets/images/gold_banana.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(50, 750)
        self.rect.y = random.randint(50, 500)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
