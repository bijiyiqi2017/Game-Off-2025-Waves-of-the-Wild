import pygame
import sys
import random # For future banana respawning

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Wave of the Wild: Energy system")

# Colors
SKY_BLUE = (135, 206, 235)
JUNGLE_GREEN = (34, 139, 34)
DARK_SOIL = (85, 53, 31)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)  # placeholder tiger color
YELLOW = (255, 255, 0)  # Banana and energy bar color
RED = (255, 0, 0) # For GAME OVER! text

font = pygame.font.SysFont(None, 80)

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

# Jump mechanics setup
velocity_y = 0  # Vertical velocity
gravity = 0.5   # Gravity effect
jump_power = -10  # Jump strength (negative because it moves the player up)
on_ground = True  # Flag to check if the player is on the ground

# Energy System Setup

max_energy = 100
current_energy = max_energy
energy_drain = 0.05 # Slow energy drain
energy_gain = 20 # Energy gained per banana group collected

# Single banana for testing
banana_rect = pygame.Rect(400, 400, 30, 30)

# Cloud Movement Variables (for scrolling clouds)
cloud_positions = [0, 0]  # Initial horizontal positions for the cloud layers.

# Game loop
clock = pygame.time.Clock()
game_running = True
game_over = False

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
             # Update floor when window is resized
            jungle_floor = pygame.Rect(0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)
              # ✅ Ensure tiger stays within the new window width
    if player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH
    if player_rect.left < 0:
        player_rect.left = 0
            
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

    # Jumping (only if on the ground)
    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = jump_power  # Apply upward force
        on_ground = False  # Player is in the air

    # Apply gravity (pull player down)
    velocity_y += gravity
    player_rect.y += velocity_y

    # Collision with the floor (stop falling when touching the ground)
    if player_rect.bottom >= SCREEN_HEIGHT - FLOOR_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT - FLOOR_HEIGHT  # Prevent player from sinking below floor
        velocity_y = 0  # Stop falling
        on_ground = True  # Player is now on the ground
    
    # Engery Logic
    current_energy -= energy_drain
    if current_energy <= 0:
        current_energy = 0
        game_over = True
        
    # Banana Collection
    if player_rect.colliderect(banana_rect)    :
        current_energy = min(current_energy + energy_gain, max_energy) # Increase Energy
        banana_rect.topleft = (-100, -100) # Remove banana after collection
        
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

    # Draw banana
    pygame.draw.rect(screen, YELLOW, banana_rect)
    
    # Draw player placeholder (tiger)
    pygame.draw.rect(screen, ORANGE, player_rect)

    # Draw energy bar
    pygame.draw.rect(screen, (100, 100, 100), (10, 10, 200, 20)) # Background
    fill_width = int((current_energy / max_energy) * 200)
    pygame.draw.rect(screen, YELLOW, (10, 10, fill_width, 20)) # Filled portion
    
    # Draw GAME OVER! Text
    if game_over:
        text_surface = font.render("GAME OVER!", True, RED)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)
        
    # Update the screen
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

