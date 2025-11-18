import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Wave of the Wild: Collidable Lake")

# Colors
SKY_BLUE = (135, 206, 235)
JUNGLE_GREEN = (34, 139, 34)
DARK_SOIL = (85, 53, 31)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WATER_BLUE = (0, 100, 255)

font = pygame.font.SysFont(None, 80)
 
# Floor setup
FLOOR_HEIGHT = 60
jungle_floor = pygame.Rect(0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)

# Cloud setup
# ====== PLATFORM SYSTEM ======
# Platform color for visual placeholder
PLATFORM_COLOR = (139, 69, 19)  # Brown color for platforms

# Platform class for easy management and collision detection
class Platform:
    def __init__(self, x, y, width, height):
        """
        Initialize a platform with position and size
        x, y: Top-left corner position
        width, height: Platform dimensions
        """
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, surface):
        """Draw the platform on the screen"""
        pygame.draw.rect(surface, PLATFORM_COLOR, self.rect)
        # Draw a lighter top edge for visual depth
        pygame.draw.rect(surface, (160, 82, 45), (self.rect.x, self.rect.y, self.rect.width, 5))

# Create platform instances at different heights and positions
# Format: Platform(x, y, width, height)
platforms = [
    Platform(150, 450, 150, 20),   # Low platform on the left
    Platform(400, 380, 120, 20),   # Medium height platform in center
    Platform(600, 300, 130, 20),   # Higher platform on the right
    Platform(250, 250, 100, 20),   # Very high platform for testing
]

# Cloud setup (Initial positions and cloud movement speed)
clouds = [
    [(150, 100, 30), (180, 100, 35), (165, 80, 25)],
    [(500, 50, 25), (520, 50, 30), (510, 30, 20)]
]
cloud_speed = 0.2

# Player setup (tiger) starts on left
tiger_img = pygame.image.load("assets/images/tiger.jpg").convert_alpha()
tiger_img = pygame.transform.scale(tiger_img, (50, 60))
player_width = tiger_img.get_width()
player_height = tiger_img.get_height()
player_x = 50
player_y = SCREEN_HEIGHT - FLOOR_HEIGHT - player_height
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
player_speed = 5

# Jump mechanics
velocity_y = 0
gravity = 0.5
jump_power = -10
on_ground = True

# Energy system
max_energy = 100
current_energy = max_energy
energy_drain = 0.05
energy_gain = 20

# Banana
banana_rect = pygame.Rect(400, 400, 30, 30)

# 💧 Collidable lake
lake_height = 12  # shallow
water_rect = pygame.Rect(250, SCREEN_HEIGHT - FLOOR_HEIGHT - lake_height, 300, lake_height)

# Cloud positions
cloud_positions = [0, 0]

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
            jungle_floor = pygame.Rect(0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)
            water_rect.y =  SCREEN_HEIGHT - FLOOR_HEIGHT - lake_height

            # Ensure tiger stays within the new window width and doesn't fall through floor
            if player_rect.right > SCREEN_WIDTH:
                player_rect.right = SCREEN_WIDTH
            if player_rect.left < 0:
                player_rect.left = 0
            if player_rect.bottom > SCREEN_HEIGHT - FLOOR_HEIGHT:
                player_rect.bottom = SCREEN_HEIGHT - FLOOR_HEIGHT
        
        # Handle jump as a single event instead of continuous key press
        # This prevents the player from jumping repeatedly when holding spacebar
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = jump_power  # Apply upward force
                on_ground = False  # Player is now in the air
            
    # Key states for player movement (left/right)
    # NOTE: We still use get_pressed() for left/right movement because we WANT continuous movement
    keys = pygame.key.get_pressed()

    # Left/right movement with lake collision check
    speed = player_speed
    new_x = player_rect.x
    if keys[pygame.K_LEFT]:
        new_x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_x += player_speed

    # Create a temporary rect to test collision
    temp_rect = pygame.Rect(new_x, player_rect.y, player_width, player_height)
    if temp_rect.colliderect(water_rect):
        speed = 2  # slow when on lake
    else:
        speed = player_speed

    # Apply horizontal movement
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed

    
    # Apply gravity
    velocity_y += gravity
    player_rect.y += velocity_y

    # Collision with floor and lake
    if player_rect.colliderect(jungle_floor):
        player_rect.bottom = jungle_floor.top
        velocity_y = 0
        on_ground = True
    elif player_rect.colliderect(water_rect):
        player_rect.bottom = water_rect.top
        velocity_y = 0
        on_ground = True

    # Energy system
    # Reset on_ground flag before checking collisions
    on_ground = False
    
    # Check collision with jungle floor
    if player_rect.bottom >= SCREEN_HEIGHT - FLOOR_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT - FLOOR_HEIGHT  # Snap player to floor top
        velocity_y = 0  # Stop falling
        on_ground = True  # Player is standing on the floor
    
    # Check collision with all platforms
    for platform in platforms:
        # Only check if player is falling (moving downward)
        if velocity_y > 0:  # Player is moving down
            # Check if player's bottom is touching or passing through platform top
            if player_rect.colliderect(platform.rect):
                # Make sure player is coming from above (not teleporting through from below)
                if player_rect.bottom <= platform.rect.top + 15:  # Allow some tolerance for smooth landing
                    player_rect.bottom = platform.rect.top  # Snap player to platform top
                    velocity_y = 0  # Stop falling
                    on_ground = True  # Player is standing on platform
                    break  # Stop checking other platforms once we've landed
    
    # Engery Logic
    current_energy -= energy_drain
    if current_energy <= 0:
        current_energy = 0
        game_over = True

    # Banana collection
    if player_rect.colliderect(banana_rect):
        current_energy = min(current_energy + energy_gain, max_energy)
        banana_rect.topleft = (-100, -100)

    # Move clouds
    cloud_positions[0] -= cloud_speed
    cloud_positions[1] -= cloud_speed * 1.5
    if cloud_positions[0] <= -SCREEN_WIDTH:
        cloud_positions[0] = 0
    if cloud_positions[1] <= -SCREEN_WIDTH:
        cloud_positions[1] = 0

    # ---------------------------------------------------
    # DRAWING
    # ---------------------------------------------------
    screen.fill(SKY_BLUE)

    # Clouds
    for i, cloud in enumerate(clouds):
        cloud_x = cloud_positions[i]
        for (x, y, r) in cloud:
            pygame.draw.circle(screen, WHITE, (int(x + cloud_x), y), r)
            pygame.draw.circle(screen, WHITE, (int(x + cloud_x + SCREEN_WIDTH), y), r)

    # Floor
    pygame.draw.rect(screen, DARK_SOIL, jungle_floor)
    pygame.draw.rect(screen, JUNGLE_GREEN, (0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, 20))

    # Lake
    pygame.draw.rect(screen, WATER_BLUE, water_rect, border_radius=5)
    pygame.draw.rect(screen, (0, 50, 150), water_rect, width=2, border_radius=5)
    for i in range(2):
        stripe_y = water_rect.y + 1 + i*5
        pygame.draw.line(screen, (170,220,255),
                         (water_rect.x + 5, stripe_y),
                         (water_rect.right - 5, stripe_y), 2)

    # Banana
    # Draw all platforms
    for platform in platforms:
        platform.draw(screen)

    # Draw banana
    pygame.draw.rect(screen, YELLOW, banana_rect)

    # Tiger
    screen.blit(tiger_img, player_rect)

    # Energy bar
    pygame.draw.rect(screen, (100,100,100), (10,10,200,20))
    fill_width = int((current_energy/max_energy)*200)
    pygame.draw.rect(screen, YELLOW, (10,10,fill_width,20))

    # Game over
    if game_over:
        text_surface = font.render("GAME OVER!", True, RED)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
