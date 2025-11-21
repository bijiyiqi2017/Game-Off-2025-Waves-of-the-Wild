import pygame
import sys
import random

# -----------------------------
# INITIALIZATION
# -----------------------------
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Wave of the Wild: Energy Burst Demo")

# Colors
SKY_BLUE = (135, 206, 235)
JUNGLE_GREEN = (34, 139, 34)
DARK_SOIL = (85, 53, 31)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WATER_BLUE = (0, 100, 255)
PLATFORM_COLOR = (139, 69, 19)

# Energy HUD colors
TEXT_COLOR = (200, 50, 50)  # Red for main text
GLOW_COLOR = (60, 160, 220)   # Softer red glow

font = pygame.font.SysFont(None, 80)

# Floor setup
FLOOR_HEIGHT = 60
jungle_floor = pygame.Rect(0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)

# -----------------------------
# PLATFORM CLASS
# -----------------------------
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, PLATFORM_COLOR, self.rect)
        pygame.draw.rect(surface, (160, 82, 45), (self.rect.x, self.rect.y, self.rect.width, 5))

# Create platforms
platforms = [
    Platform(500, 255, 150, 20),
    Platform(80, 230, 150, 20),
    Platform(150, 450, 150, 20),
    Platform(400, 380, 120, 20),
    Platform(600, 380, 130, 20),
    Platform(250, 300, 100, 20),
]

# -----------------------------
# CLOUDS
# -----------------------------
clouds = [
    [(150, 100, 30), (180, 100, 35), (165, 80, 25)],
    [(500, 50, 25), (520, 50, 30), (510, 30, 20)]
]
cloud_speed = 0.2
cloud_positions = [0, 0]

# -----------------------------
# PLAYER SETUP
# -----------------------------
tiger_img = pygame.image.load("assets/images/tiger.jpg").convert_alpha()
tiger_img = pygame.transform.scale(tiger_img, (50, 60))
player_rect = tiger_img.get_rect()
player_rect.topleft = (50, SCREEN_HEIGHT - FLOOR_HEIGHT - tiger_img.get_height())
player_speed = 5

velocity_y = 0
gravity = 0.5
jump_power = -10
on_ground = True

# -----------------------------
# ENERGY SYSTEM
# -----------------------------
max_energy = 100
current_energy = max_energy
energy_drain = 0.25 

# Energy burst variables
energy_burst_active = False
energy_burst_count = 0
burst_frame_cooldown = 0
energy_burst_text = ""
energy_burst_text_timer = 0

# -----------------------------
# BANANAS
# -----------------------------
banana_rect = pygame.Rect(400, 400, 30, 30)
banana_win_rect = pygame.Rect(500, 200, 30, 20 )
banana_win_active = True
energy_burst_value = 4  # Each burst adds 4 energy (5 bursts = 20)

# Banana respawn delay
banana_respawn_delay = 0
BANANA_RESPAWN_TIME = 180  # 3 seconds

def banana_spawn():
    banana_rect.x = random.randint(50, SCREEN_WIDTH - 50)
    banana_rect.y = random.randint(100, SCREEN_HEIGHT - FLOOR_HEIGHT - 50)

# -----------------------------
# LAKE
# -----------------------------
lake_height = 12
water_rect = pygame.Rect(250, SCREEN_HEIGHT - FLOOR_HEIGHT - lake_height, 300, lake_height)

# -----------------------------
# CLOCK AND FLAGS
# -----------------------------
clock = pygame.time.Clock()
game_running = True
game_over = False
game_win = False

# -----------------------------
# WIN SCREEN FUNCTION
# -----------------------------
def draw_win_screen():
    screen.fill((0, 0, 0))
    base_font_size = 60
    scale = screen.get_height() / 600
    font_size = max(int(base_font_size * scale), 20)
    win_font = pygame.font.SysFont(None, font_size)

    def draw_text_centered(text, y_ratio):
        text_surface = win_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(screen.get_width()//2, int(screen.get_height()*y_ratio)))
        screen.blit(text_surface, text_rect)

    draw_text_centered("Congrats!", 0.3)
    draw_text_centered("You survived...", 0.5)
    draw_text_centered("Enjoy life with friends & family", 0.9)
    pygame.display.flip()

# -----------------------------
# GAME LOOP
# -----------------------------
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            jungle_floor = pygame.Rect(0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)
            water_rect.y = SCREEN_HEIGHT - FLOOR_HEIGHT - lake_height
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = jump_power
                on_ground = False

    if game_win:
        draw_win_screen()
        continue

    # -----------------------------
    # PLAYER MOVEMENT
    # -----------------------------
    keys = pygame.key.get_pressed()
    new_x = player_rect.x
    if keys[pygame.K_LEFT]: new_x -= player_speed
    if keys[pygame.K_RIGHT]: new_x += player_speed

    temp_rect = pygame.Rect(new_x, player_rect.y, player_rect.width, player_rect.height)
    speed = 2 if temp_rect.colliderect(water_rect) else player_speed

    if keys[pygame.K_LEFT]: player_rect.x -= speed
    if keys[pygame.K_RIGHT]: player_rect.x += speed

    velocity_y += gravity
    player_rect.y += velocity_y

    on_ground = False
    if player_rect.bottom >= SCREEN_HEIGHT - FLOOR_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT - FLOOR_HEIGHT
        velocity_y = 0
        on_ground = True

    # Platform collisions
    for platform in platforms:
        if velocity_y > 0 and player_rect.colliderect(platform.rect):
            if player_rect.bottom <= platform.rect.top + 15:
                player_rect.bottom = platform.rect.top
                velocity_y = 0
                on_ground = True
                break

    # -----------------------------
    # ENERGY DRAIN
    # -----------------------------
    current_energy -= energy_drain
    if current_energy <= 0:
        current_energy = 0
        game_over = True

    # -----------------------------
    # BANANA COLLISIONS
    # -----------------------------
    # Banana #1 = trigger energy burst
    if player_rect.colliderect(banana_rect) and not energy_burst_active:
        energy_burst_active = True
        energy_burst_count = 5
        burst_frame_cooldown = 0

        # Wave of Energy message
        energy_burst_text = "Wave of Energy!"
        energy_burst_text_timer = 180  # 3 seconds
        banana_rect.topleft = (-200, -200)
        banana_respawn_delay = BANANA_RESPAWN_TIME

    # Banana #2 = WIN TRIGGER
    if banana_win_active and player_rect.colliderect(banana_win_rect):
        banana_win_active = False
        banana_win_rect.topleft = (-100, -100)
        game_win = True

    # -----------------------------
    # ENERGY BURSTS
    # -----------------------------
    if energy_burst_active:
        if burst_frame_cooldown <= 0:
            current_energy = min(current_energy + energy_burst_value, max_energy)
            energy_burst_count -= 1
            burst_frame_cooldown = 10  # frames between bursts

            if energy_burst_count <= 0:
                energy_burst_active = False
        else:
            burst_frame_cooldown -= 1

    # -----------------------------
    # BANANA RESPAWN
    # -----------------------------
    if banana_respawn_delay > 0:
        banana_respawn_delay -= 1
    elif banana_rect.x < 0:
        banana_spawn()

    # -----------------------------
    # CLOUD MOVEMENT
    # -----------------------------
    cloud_positions[0] -= cloud_speed
    cloud_positions[1] -= cloud_speed * 1.5
    for i in range(2):
        if cloud_positions[i] <= -SCREEN_WIDTH:
            cloud_positions[i] = 0

    # -----------------------------
    # DRAWING
    # -----------------------------
    screen.fill(SKY_BLUE)

    for i, cloud in enumerate(clouds):
        cx = cloud_positions[i]
        for (x, y, r) in cloud:
            pygame.draw.circle(screen, WHITE, (int(x + cx), y), r)
            pygame.draw.circle(screen, WHITE, (int(x + cx + SCREEN_WIDTH), y), r)

    pygame.draw.rect(screen, DARK_SOIL, jungle_floor)
    pygame.draw.rect(screen, JUNGLE_GREEN, (0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, 20))
    pygame.draw.rect(screen, WATER_BLUE, water_rect, border_radius=5)
    pygame.draw.rect(screen, (0, 50, 150), water_rect, width=2, border_radius=5)

    for platform in platforms:
        platform.draw(screen)

    pygame.draw.rect(screen, YELLOW, banana_rect)
    if banana_win_active:
        pygame.draw.rect(screen, YELLOW, banana_win_rect)

    screen.blit(tiger_img, player_rect)

    # -----------------------------
    # ENERGY BAR
    # -----------------------------
    if energy_burst_active:
        glow_rect = pygame.Rect(15, 15, int(current_energy * 2), 30)
        pygame.draw.rect(screen, GLOW_COLOR, glow_rect, border_radius=8)

    bar_bg = pygame.Rect(20, 20, max_energy * 2, 30)
    bar_fill = pygame.Rect(20, 20, int(current_energy * 2), 30)
    pygame.draw.rect(screen, (80, 80, 80), bar_bg, border_radius=8)
    pygame.draw.rect(screen, (50, 200, 50), bar_fill, border_radius=8)

    # -----------------------------
    # ENERGY BURST TEXT (STATIONARY)
    # -----------------------------
    if energy_burst_text_timer > 0:
        y_pos = 80  # stationary

        msg_font = pygame.font.SysFont(None, 60)

        # Glow layers
        for glow_size in [2, 4, 6]:
            glow_surf = msg_font.render(energy_burst_text, True, GLOW_COLOR)
            glow_surf.set_alpha(80)
            glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            glow_rect.inflate_ip(glow_size, glow_size)
            screen.blit(glow_surf, glow_rect)

        # Main text
        text_surf = msg_font.render(energy_burst_text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        screen.blit(text_surf, text_rect)

        energy_burst_text_timer -= 1

    # -----------------------------
    # GAME OVER
    # -----------------------------
    if game_over:
        text_surface = font.render("GAME OVER!", True, RED)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
