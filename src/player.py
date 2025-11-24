import pygame
from src.settings import *

class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/images/tiger.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, SCREEN_HEIGHT - FLOOR_HEIGHT - self.rect.height)

        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.on_ground = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def update(self, platforms):
        self.handle_input()

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # ground collision
        if self.rect.bottom >= SCREEN_HEIGHT - FLOOR_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - FLOOR_HEIGHT
            self.velocity_y = 0
            self.on_ground = True

        # platform collision
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
