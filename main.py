import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wave in the Wild: Parallax Clouds")

# Colors
SKY_BLUE = (135, 206, 235)
JUNGLE_GREEN = (34, 139, 34)
DARK_SOIL = (85, 53, 31)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)  # placeholder tiger color

# Floor setup
FLOOR_HEIGHT = 60
jungle_floor = pygame.Rect(0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)

# Cloud setup (Initial positions and cloud movement speed)
clouds = [
    [(150, 100, 30), (180, 100, 35), (165, 80, 25)],  # cloud 1
    [(500, 50, 25), (520, 50, 30), (510, 30, 20)]    # cloud 2
]
cloud_speed = 0.2  # Speed of cloud movement

# Player setup (placeholder tiger)
player_width = 50
player_height = 60
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - FLOOR_HEIGHT - player_height
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
player_speed = 5

# Cloud Movement Variables (for scrolling clouds)
cloud_positions = [0, 0]  # Initial horizontal positions for the cloud layers.

# Game loop
clock = pygame.time.Clock()
game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Key states for player movement (left/right)
    keys = pygame.key.get_pressed()

    # Left/Right Movement (Boundary checks to keep the player on screen)
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed  # Move player to the left
        if player_rect.x < 0:  # Prevent the player from moving off-screen to the left
            player_rect.x = 0
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed  # Move player to the right
        if player_rect.x > SCREEN_WIDTH - player_width:  # Prevent player from moving off-screen to the right
            player_rect.x = SCREEN_WIDTH - player_width

    # Move clouds to the left (parallax)
    cloud_positions[0] -= cloud_speed  # Cloud 1 (far background)
    cloud_positions[1] -= cloud_speed * 1.5  # Cloud 2 (closer background)

    # Reset clouds once they move off-screen to create an infinite effect
    if cloud_positions[0] <= -SCREEN_WIDTH:
        cloud_positions[0] = 0
    if cloud_positions[1] <= -SCREEN_WIDTH:
        cloud_positions[1] = 0

    # Draw sky (background)
    screen.fill(SKY_BLUE)

    # Draw clouds with parallax effect (moving at different speeds)
    for i, cloud in enumerate(clouds):
        cloud_x = cloud_positions[i]  # Get the current offset for each cloud layer
        for (x, y, r) in cloud:
            # Create the illusion of infinite scrolling (draw the clouds twice for seamless loop)
            pygame.draw.circle(screen, WHITE, (int(x + cloud_x), y), r)
            pygame.draw.circle(screen, WHITE, (int(x + cloud_x + SCREEN_WIDTH), y), r)  # Second copy for infinite effect

    # Draw jungle floor (stationary)
    pygame.draw.rect(screen, DARK_SOIL, jungle_floor)  # soil layer
    pygame.draw.rect(screen, JUNGLE_GREEN, (0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, 20))  # grass/top

    # Draw player placeholder (tiger)
    pygame.draw.rect(screen, ORANGE, player_rect)

    # Update the screen
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
