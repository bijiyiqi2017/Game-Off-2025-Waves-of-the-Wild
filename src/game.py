import os
import pygame
from src.settings import *
from src.player import Player
from src.platforms import Platform
from src.banana import Banana
from src.title_screen import draw_title
from src.win_screen import draw_win
from src.game_over_screen import draw_game_over

# -----------------------
# Project root directory
# -----------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

def asset_path(*paths):
    return os.path.join(PROJECT_ROOT, *paths)

# -----------------------
# Initialize pygame & mixer
# -----------------------
pygame.init()
pygame.mixer.init()

# Load sounds
jump_sound = pygame.mixer.Sound(asset_path("assets", "sounds", "jump.mp3"))
collect_sound = pygame.mixer.Sound(asset_path("assets", "sounds", "eat.mp3"))
win_sound = pygame.mixer.Sound(asset_path("assets", "sounds", "win.mp3"))
start_sound = pygame.mixer.Sound(asset_path("assets", "sounds", "start_sound.wav"))
bg_music = pygame.mixer.Sound(asset_path("assets", "sounds", "background_music.mp3"))

class Game:
    def __init__(self):
        self.state = TITLE_SCREEN
        self.player = Player()
        self.platforms = [
            Platform(0, 550, 800, 50),  # ground
            Platform(500, 255, 150, 20),
            Platform(80, 230, 150, 20),
            Platform(150, 450, 150, 20)
        ]
        self.bananas = [Banana() for _ in range(5)]
        self.score = 0
        self.energy = 100

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == TITLE_SCREEN and event.type == pygame.KEYDOWN:
                    self.state = PLAYING
                    start_sound.play()
                    bg_music.play(-1)

                if self.state == PLAYING:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.player.jump()
                        jump_sound.play()

                if self.state in (WIN_STATE, GAME_OVER_STATE) and event.type == pygame.KEYDOWN:
                    self.__init__()

            if self.state == TITLE_SCREEN:
                draw_title()
            elif self.state == PLAYING:
                self.update_game()
                self.draw_game()
            elif self.state == WIN_STATE:
                draw_win()
            elif self.state == GAME_OVER_STATE:
                draw_game_over()

            clock.tick(60)

    def update_game(self):
        self.player.update(self.platforms)
        self.check_banana_collision()

        self.energy -= 0.05
        if self.energy <= 0:
            self.state = GAME_OVER_STATE

        if self.score >= 5:
            win_sound.play()
            self.state = WIN_STATE

    def check_banana_collision(self):
        for banana in self.bananas:
            if self.player.rect.colliderect(banana.rect):
                collect_sound.play()
                self.score += 1
                self.energy = min(100, self.energy + 20)
                banana.reset_position()

    def draw_game(self):
        SCREEN.fill(SKY_BLUE)
        for p in self.platforms:
            p.draw(SCREEN)
        for b in self.bananas:
            b.draw(SCREEN)
        SCREEN.blit(self.player.image, self.player.rect)

        self.draw_hud()
        pygame.display.flip()

    def draw_hud(self):
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Bananas: {self.score}", True, YELLOW)
        energy_text = font.render(f"Energy: {int(self.energy)}", True, RED)
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(energy_text, (10, 50))
