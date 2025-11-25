import pygame
from src.settings import *

class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/images/tiger.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 400
        self.vel_y = 0
        self.jumping = False
        self.gravity = 0.5

    def jump(self):
        if not self.jumping:
            self.vel_y = -12
            self.jumping = True

    def update(self, platforms):
        # Apply gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Platform collision
        self.jumping = True
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.jumping = False
