import pygame

pygame.init()

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Waves of the Wild")

# Colors
SKY_BLUE = (135, 206, 235)
JUNGLE_GREEN = (34, 139, 34)
DARK_SOIL = (85, 53, 31)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PLATFORM_COLOR = (139, 69, 19)
ORANGE = (255, 140, 0)
WATER_BLUE = (0, 100, 255)

# Floor
FLOOR_HEIGHT = 60

# Game States
TITLE_SCREEN = 0
PLAYING = 1
GAME_OVER_STATE = 2
WIN_STATE = 3

clock = pygame.time.Clock()
