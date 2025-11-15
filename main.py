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
            water_rect.y = SCREEN_HEIGHT - FLOOR_HEIGHT - lake_height

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

    # Jump
    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = jump_power
        on_ground = False

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
