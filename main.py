import pygame
import sys
import random
import math

# -----------------------------
# INITIALIZATION
# -----------------------------
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Wave of the Wild")

# Colors
SKY_BLUE = (135, 206, 235)
JUNGLE_GREEN = (34, 139, 34)
DARK_SOIL = (85, 53, 31)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WATER_BLUE = (0, 100, 255)
PLATFORM_COLOR = (139, 69, 19)
DARK_GREEN = (20, 80, 20)
ORANGE = (255, 140, 0)

# Energy HUD colors
TEXT_COLOR = (200, 50, 50)
GLOW_COLOR = (60, 160, 220)

font = pygame.font.SysFont(None, 80)

# Floor setup
FLOOR_HEIGHT = 60
jungle_floor = pygame.Rect(0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)

# ═══════════════════════════════════════════════════════════════
# GAME STATES
# ═══════════════════════════════════════════════════════════════
TITLE_SCREEN = 0
PLAYING = 1
GAME_OVER_STATE = 2
WIN_STATE = 3

current_state = TITLE_SCREEN  # Start at title screen

# ═══════════════════════════════════════════════════════════════
# TITLE SCREEN ANIMATION VARIABLES
# ═══════════════════════════════════════════════════════════════
pulse_timer = 0
pulse_alpha = 255

# ═══════════════════════════════════════════════════════════════
# BACKGROUND MUSIC SETUP
# ═══════════════════════════════════════════════════════════════
music_loaded = False
title_music_playing = False
title_music_volume = 0.5
gameplay_music_volume = 0.3

pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.set_volume(title_music_volume)
music_loaded = True

# WIN SOUND EFFECT
win_sound = pygame.mixer.Sound("assets/sounds/win.mp3")
win_sound.set_volume(0.7)

level_up_sound = pygame.mixer.Sound("assets/sounds/level-up.mp3")



# ═══════════════════════════════════════════════════════════════
# PLATFORM CLASS
# ═══════════════════════════════════════════════════════════════
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, PLATFORM_COLOR, self.rect)
        pygame.draw.rect(surface, (160, 82, 45), (self.rect.x, self.rect.y, self.rect.width, 5))

platforms = [
    Platform(500, 255, 150, 20),
    Platform(80, 230, 150, 20),
    Platform(150, 450, 150, 20),
    Platform(400, 380, 120, 20),
    Platform(600, 380, 130, 20),
    Platform(250, 300, 100, 20),
]

# CLOUDS
clouds = [
    [(150, 100, 30), (180, 100, 35), (165, 80, 25)],
    [(500, 50, 25), (520, 50, 30), (510, 30, 20)]
]
cloud_speed = 0.2
cloud_positions = [0, 0]

# PLAYER SETUP
tiger_img = pygame.image.load("assets/images/tiger.jpg").convert_alpha()
tiger_img = pygame.transform.scale(tiger_img, (50, 60))
player_rect = tiger_img.get_rect()
player_rect.topleft = (50, SCREEN_HEIGHT - FLOOR_HEIGHT - tiger_img.get_height())
player_speed = 5
velocity_y = 0
gravity = 0.5
jump_power = -10
on_ground = True



# ENERGY SYSTEM
max_energy = 100
current_energy = max_energy
energy_drain = 0.25
energy_burst_active = False
energy_burst_count = 0
burst_frame_cooldown = 0
energy_burst_text = ""
energy_burst_text_timer = 0
energy_burst_value = 4  # Each burst adds 4 energy

# BANANAS
# banana_rect = pygame.Rect(400, 400, 30, 30)
banana_img = pygame.image.load("assets/images/one_banana.jpg").convert_alpha()
banana_img = pygame.transform.scale(banana_img, (30, 30))  
banana_rect = banana_img.get_rect()
banana_rect.topleft = (400, 400)

# banana_win_rect = pygame.Rect(500, 200, 30, 20)
# banana_win_active = True
# WIN BANANA IMAGE (Goal)
gold_banana_img = pygame.image.load("assets/images/gold_bananas.png").convert_alpha()
gold_banana_img = pygame.transform.scale(gold_banana_img, (40, 40))
banana_win_rect = gold_banana_img.get_rect()
banana_win_rect.center = (500, 200)
banana_win_active = True

banana_respawn_delay = 0
BANANA_RESPAWN_TIME = 180  # 3 seconds

def banana_spawn():
    banana_rect.x = random.randint(50, SCREEN_WIDTH - 50)
    banana_rect.y = random.randint(100, SCREEN_HEIGHT - FLOOR_HEIGHT - 50)

# LAKE
lake_height = 12
water_rect = pygame.Rect(250, SCREEN_HEIGHT - FLOOR_HEIGHT - lake_height, 300, lake_height)

# CLOCK AND FLAGS
clock = pygame.time.Clock()
game_running = True

# ═══════════════════════════════════════════════════════════════
# SCREEN DRAW FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def draw_title_screen():
    global pulse_timer, pulse_alpha, title_music_playing

    if music_loaded and not title_music_playing:
        pygame.mixer.music.play(-1)
        title_music_playing = True

    screen.fill(DARK_GREEN)
    jungle_ground = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
    pygame.draw.rect(screen, (34, 60, 34), jungle_ground)
    pygame.draw.rect(screen, JUNGLE_GREEN, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 30))

    bg_image = pygame.image.load("assets/images/jungle_bg.png")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(bg_image, (0, 0))

    title_font = pygame.font.SysFont(None, 90)
    title_text = "Waves of the Wild"
    title_shadow = title_font.render(title_text, True, (0, 0, 0))
    shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 3, SCREEN_HEIGHT//3 + 3))
    screen.blit(title_shadow, shadow_rect)

    title_surface = title_font.render(title_text, True, ORANGE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    screen.blit(title_surface, title_rect)

    pulse_timer += 0.05
    pulse_alpha = int(155 + 100 * abs(math.sin(pulse_timer)))

    instruction_font = pygame.font.SysFont(None, 50)
    instruction_text = instruction_font.render("Press any key to start", True, YELLOW)
    instruction_text.set_alpha(pulse_alpha)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT * 0.85))
    screen.blit(instruction_text, instruction_rect)

    credits_font = pygame.font.SysFont(None, 25)
    credits_text = credits_font.render("By Team Waves — Game Off 2025", True, WHITE)
    credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 25))
    screen.blit(credits_text, credits_rect)

    pygame.display.flip()

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

def draw_game_over_screen():
    screen.fill((0, 0, 0))
    text_surface = font.render("GAME OVER!", True, RED)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
# MAIN GAME LOOP
# ═══════════════════════════════════════════════════════════════
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
            if current_state == TITLE_SCREEN:
                if title_music_playing:
                    pygame.mixer.music.stop()
                current_state = PLAYING
                start_sound = pygame.mixer.Sound("assets/sounds/start_sound.wav")
                start_sound.play()
            elif current_state == PLAYING:
                if event.key == pygame.K_SPACE and on_ground:
                    velocity_y = jump_power
                    on_ground = False

    # Render based on state
    if current_state == TITLE_SCREEN:
        draw_title_screen()
        continue
    if current_state == GAME_OVER_STATE:
        draw_game_over_screen()
        continue
    if current_state == WIN_STATE:
        draw_win_screen()
        continue

    # -----------------------------
    # GAMEPLAY LOGIC
    # -----------------------------
    keys = pygame.key.get_pressed()
    new_x = player_rect.x
    if keys[pygame.K_LEFT]:
        new_x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_x += player_speed

    speed = 2 if pygame.Rect(new_x, player_rect.y, player_rect.width, player_rect.height).colliderect(water_rect) else player_speed
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed

    velocity_y += gravity
    player_rect.y += velocity_y

    on_ground = False
    if player_rect.bottom >= SCREEN_HEIGHT - FLOOR_HEIGHT:
        player_rect.bottom = SCREEN_HEIGHT - FLOOR_HEIGHT
        velocity_y = 0
        on_ground = True

    for platform in platforms:
        if velocity_y > 0 and player_rect.colliderect(platform.rect):
            if player_rect.bottom <= platform.rect.top + 15:
                player_rect.bottom = platform.rect.top
                velocity_y = 0
                on_ground = True
                break

    current_energy -= energy_drain
    if current_energy <= 0:
        current_energy = 0
        current_state = GAME_OVER_STATE

    if player_rect.colliderect(banana_rect) and not energy_burst_active:
        level_up_sound.play()
        energy_burst_active = True
        energy_burst_count = 5
        burst_frame_cooldown = 0
        energy_burst_text = "Wave of Energy!"
        energy_burst_text_timer = 180
        banana_rect.topleft = (-200, -200)
        banana_respawn_delay = BANANA_RESPAWN_TIME

    if banana_win_active and player_rect.colliderect(banana_win_rect):
        banana_win_active = False
        #banana_win_rect.topleft = (-100, -100)
        banana_win_rect.center = (-100, -100)

        current_state = WIN_STATE
        
        if music_loaded:
            pygame.mixer.music.stop()
        win_sound.play()

    if energy_burst_active:
        if burst_frame_cooldown <= 0:
            current_energy = min(current_energy + energy_burst_value, max_energy)
            energy_burst_count -= 1
            burst_frame_cooldown = 10
            if energy_burst_count <= 0:
                energy_burst_active = False
        else:
            burst_frame_cooldown -= 1

    if banana_respawn_delay > 0:
        banana_respawn_delay -= 1
    elif banana_rect.x < 0:
        banana_spawn()

    cloud_positions[0] -= cloud_speed
    cloud_positions[1] -= cloud_speed * 1.5
    for i in range(2):
        if cloud_positions[i] <= -SCREEN_WIDTH:
            cloud_positions[i] = 0

    # -----------------------------
    # DRAW GAME WORLD
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

    # pygame.draw.rect(screen, YELLOW, banana_rect)
    screen.blit(banana_img, banana_rect)
    # if banana_win_active:
        # pygame.draw.rect(screen, YELLOW, banana_win_rect)
    if banana_win_active:
        screen.blit(gold_banana_img, banana_win_rect)

    screen.blit(tiger_img, player_rect)

    if energy_burst_active:
        glow_rect = pygame.Rect(15, 15, int(current_energy * 2), 30)
        pygame.draw.rect(screen, GLOW_COLOR, glow_rect, border_radius=8)

    bar_bg = pygame.Rect(20, 20, max_energy * 2, 30)
    bar_fill = pygame.Rect(20, 20, int(current_energy * 2), 30)
    pygame.draw.rect(screen, (80, 80, 80), bar_bg, border_radius=8)
    pygame.draw.rect(screen, (50, 200, 50), bar_fill, border_radius=8)

    if energy_burst_text_timer > 0:
        y_pos = 80
        msg_font = pygame.font.SysFont(None, 60)
        for glow_size in [2, 4, 6]:
            glow_surf = msg_font.render(energy_burst_text, True, GLOW_COLOR)
            glow_surf.set_alpha(80)
            glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            glow_rect.inflate_ip(glow_size, glow_size)
            screen.blit(glow_surf, glow_rect)
        text_surf = msg_font.render(energy_burst_text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        screen.blit(text_surf, text_rect)
        energy_burst_text_timer -= 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
