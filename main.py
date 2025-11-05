import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jungle Floor with Clouds")

# Colors
SKY_BLUE = (135, 206, 235)
JUNGLE_GREEN = (34, 139, 34)
DARK_SOIL = (85, 53, 31)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)  # placeholder tiger color

# Floor setup
FLOOR_HEIGHT = 60
jungle_floor = pygame.Rect(0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)

# Cloud positions (x, y, radius)
clouds = [
    [(150, 100, 30), (180, 100, 35), (165, 80, 25)],  # cloud 1
    [(500, 50, 25), (520, 50, 30), (510, 30, 20)]    # cloud 2
]

# Player setup (placeholder tiger)
player_width = 50
player_height = 60
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - FLOOR_HEIGHT - player_height
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
player_speed = 5

# Movement will be implemented later
# Placeholder comment for left/right movement

# Game loop
clock = pygame.time.Clock()
game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Key states
    keys = pygame.key.get_pressed()

    # Placeholder for left/right movement (implement later)
    # if keys[pygame.K_LEFT]:
    
    # if keys[pygame.K_RIGHT]: 
    
    # Draw sky
    screen.fill(SKY_BLUE)

    # Draw clouds
    for cloud in clouds:
        for (x, y, r) in cloud:
            pygame.draw.circle(screen, WHITE, (x, y), r)

    # Draw jungle floor
    pygame.draw.rect(screen, DARK_SOIL, jungle_floor)  # soil layer
    pygame.draw.rect(screen, JUNGLE_GREEN, (0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, 20))  # grass/top

    # Draw player placeholder
    pygame.draw.rect(screen, ORANGE, player_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
