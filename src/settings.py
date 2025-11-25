import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Waves of the Wild")

# Colors
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Platform color
PLATFORM_COLOR = GREEN

# Game states
TITLE_SCREEN = "title_screen"
PLAYING = "playing"
WIN_STATE = "win_state"
GAME_OVER_STATE = "game_over_state"

# Clock
clock = pygame.time.Clock()
