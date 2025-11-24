import pygame
from src.settings import *
from src.player import Player
from src.platforms import Platform
from src.title_screen import draw_title
from src.win_screen import draw_win
from src.game_over_screen import draw_game_over

class Game:
    def __init__(self):
        self.state = TITLE_SCREEN
        self.player = Player()
        self.platforms = [
            Platform(500, 255, 150, 20),
            Platform(80, 230, 150, 20),
            Platform(150, 450, 150, 20),
        ]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == TITLE_SCREEN and event.type == pygame.KEYDOWN:
                    self.state = PLAYING

                if self.state == PLAYING:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.player.jump()

                if self.state in (WIN_STATE, GAME_OVER_STATE) and event.type == pygame.KEYDOWN:
                    self.__init__()

            # State logic
            if self.state == TITLE_SCREEN:
                draw_title()
            elif self.state == PLAYING:
                self.update_game()
                self.draw_game()
            elif self.state == GAME_OVER_STATE:
                draw_game_over()
            elif self.state == WIN_STATE:
                draw_win()

            clock.tick(60)

    def update_game(self):
        self.player.update(self.platforms)

    def draw_game(self):
        SCREEN.fill(SKY_BLUE)
        for p in self.platforms:
            p.draw(SCREEN)
        SCREEN.blit(self.player.image, self.player.rect)
        pygame.display.flip()
