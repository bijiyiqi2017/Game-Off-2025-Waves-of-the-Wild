import pygame
import sys
import random
import math

# Initialize Pygame
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
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WATER_BLUE = (0, 100, 255)
PLATFORM_COLOR = (139, 69, 19)
DARK_GREEN = (20, 80, 20)
ORANGE = (255, 140, 0)

font = pygame.font.SysFont(None, 80)

# Floor setup
FLOOR_HEIGHT = 60
jungle_floor = pygame.Rect(0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)

# ═══════════════════════════════════════════════════════════════
#  GAME STATES
# ═══════════════════════════════════════════════════════════════
# We use these to track which "screen" the player is on
TITLE_SCREEN = 0
PLAYING = 1
GAME_OVER_STATE = 2
WIN_STATE = 3

current_state = TITLE_SCREEN  # Start at title screen

# ═══════════════════════════════════════════════════════════════
#  TITLE SCREEN ANIMATION VARIABLES
# ═══════════════════════════════════════════════════════════════
# These create the pulsing "press any key" effect
pulse_timer = 0
pulse_alpha = 255  # Controls transparency (0 = invisible, 255 = solid)

# ═══════════════════════════════════════════════════════════════
#  BACKGROUND MUSIC SETUP
# ═══════════════════════════════════════════════════════════════
# Track if music has been loaded to avoid loading multiple times
music_loaded = False
title_music_playing = False

# ═══════════════════════════════════════════════════════════════
#  VOLUME SETTINGS - Adjust these numbers to control volume!
# ═══════════════════════════════════════════════════════════════
# Volume range: 0.0 = silent, 1.0 = maximum volume
title_music_volume = 0.5      # Title screen music
gameplay_music_volume = 0.3    # Gameplay music

# ═══════════════════════════════════════════════════════════════
# Background music (runs once at startup)
# ═══════════════════════════════════════════════════════════════

pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.set_volume(title_music_volume)  # Apply volume setting
music_loaded = True

# Platform class
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, PLATFORM_COLOR, self.rect)
        pygame.draw.rect(surface, (160, 82, 45), (self.rect.x, self.rect.y, self.rect.width, 5))

# Create platforms (highest two now at same height)
platforms = [
    Platform(150, 450, 150, 20),   # Low platform
    Platform(400, 380, 120, 20),   # Medium/goal platform
    Platform(600, 380, 130, 20),   # Lowered to match second highest
    Platform(250, 300, 100, 20),   # Optional platform
]

# Clouds
clouds = [
    [(150, 100, 30), (180, 100, 35), (165, 80, 25)],
    [(500, 50, 25), (520, 50, 30), (510, 30, 20)]
]
cloud_speed = 0.2
cloud_positions = [0, 0]

# Player setup
tiger_img = pygame.image.load("assets/images/tiger.jpg").convert_alpha()
tiger_img = pygame.transform.scale(tiger_img, (50, 60))
player_rect = tiger_img.get_rect()
player_rect.topleft = (50, SCREEN_HEIGHT - FLOOR_HEIGHT - tiger_img.get_height())
player_speed = 5

velocity_y = 0
gravity = 0.5
jump_power = -10
on_ground = True

# Energy
max_energy = 100
current_energy = max_energy
energy_drain = 0.05
energy_gain = 20

# Bananas
banana_rect = pygame.Rect(400, 400, 30, 30)
banana2_rect = pygame.Rect(600, 350, 30, 30)  # On top platform
banana2_active = True

# Lake
lake_height = 12
water_rect = pygame.Rect(250, SCREEN_HEIGHT - FLOOR_HEIGHT - lake_height, 300, lake_height)

clock = pygame.time.Clock()
game_running = True

# ═══════════════════════════════════════════════════════════════
#  TITLE SCREEN FUNCTION
# ═══════════════════════════════════════════════════════════════
def draw_title_screen():
    """
    Draws the game's title screen with animated elements.
    This is the first thing players see!
    """
    global pulse_timer, pulse_alpha, title_music_playing
    
    # ═══════════════════════════════════════════════════════════
    #  START TITLE MUSIC (only once)
    # ═══════════════════════════════════════════════════════════
    if music_loaded and not title_music_playing:
        pygame.mixer.music.play(-1)  # -1 means loop forever
        title_music_playing = True
    
    # Background gradient effect (jungle vibes)
    screen.fill(DARK_GREEN)
    
    # Draw a subtle jungle floor at bottom for atmosphere
    jungle_ground = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
    pygame.draw.rect(screen, (34, 60, 34), jungle_ground)
    pygame.draw.rect(screen, JUNGLE_GREEN, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 30))
    
    # ═══════════════════════════════════════════════════════════
    # Background image
    # ═══════════════════════════════════════════════════════════

    bg_image = pygame.image.load("assets/images/jungle_bg.png")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(bg_image, (0, 0))
    
    # ═══════════════════════════════════════════════════════════
    #  GAME TITLE
    # ═══════════════════════════════════════════════════════════
    title_font = pygame.font.SysFont(None, 90)
    
    # Main title with shadow effect for depth
    title_text = "Waves of the Wild"
    
    # Shadow (drawn first, offset slightly)
    title_shadow = title_font.render(title_text, True, (0, 0, 0))
    shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 3, SCREEN_HEIGHT//3 + 3))
    screen.blit(title_shadow, shadow_rect)
    
    # Main title text
    title_surface = title_font.render(title_text, True, ORANGE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    screen.blit(title_surface, title_rect)
    
    # ═══════════════════════════════════════════════════════════
    #  OPTIONAL: Tiger splash image
    # ═══════════════════════════════════════════════════════════
    # Add a large decorative tiger image in the center:
    #
    # tiger_splash = pygame.image.load("assets/images/tiger_splash.png")
    # tiger_splash = pygame.transform.scale(tiger_splash, (200, 200))
    # tiger_rect = tiger_splash.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    # screen.blit(tiger_splash, tiger_rect)
    
    # ═══════════════════════════════════════════════════════════
    #  PULSING "PRESS ANY KEY" TEXT
    # ═══════════════════════════════════════════════════════════
    # Create smooth pulsing effect using sine wave
    pulse_timer += 0.05
    pulse_alpha = int(155 + 100 * abs(math.sin(pulse_timer)))  # Oscillates between 155-255
    
    instruction_font = pygame.font.SysFont(None, 50)
    instruction_text = instruction_font.render("Press any key to start", True, YELLOW)
    
    # Apply alpha transparency for pulse effect
    instruction_text.set_alpha(pulse_alpha)
    
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT * 0.85))
    screen.blit(instruction_text, instruction_rect)
    
    # ═══════════════════════════════════════════════════════════
    #  CREDITS
    # ═══════════════════════════════════════════════════════════
    credits_font = pygame.font.SysFont(None, 25)
    credits_text = credits_font.render("By Team Waves — Game Off 2025", True, WHITE)
    credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 25))
    screen.blit(credits_text, credits_rect)
    
    pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  WIN SCREEN FUNCTION (CENTERED + RESIZABLE)
# ═══════════════════════════════════════════════════════════════
def draw_win_screen():
    """
    Victory screen shown when player collects the winning banana.
    """
    screen.fill((0, 0, 0))

    # Dynamically scale font based on screen height
    base_font_size = 60
    scale = screen.get_height() / 600
    font_size = max(int(base_font_size * scale), 20)
    win_font = pygame.font.SysFont(None, font_size)

    # Helper to draw centered text
    def draw_text_centered(text, y_ratio):
        text_surface = win_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(screen.get_width()//2, int(screen.get_height()*y_ratio)))
        screen.blit(text_surface, text_rect)

    # Draw all win texts at relative vertical positions
    draw_text_centered("Congrats!", 0.3)
    draw_text_centered("You survived...", 0.5)
    draw_text_centered("Enjoy life with friends & family", 0.9)

    pygame.display.flip()

# ═══════════════════════════════════════════════════════════════
#  MAIN GAME LOOP
# ═══════════════════════════════════════════════════════════════
while game_running:
    # ───────────────────────────────────────────────────────────
    #  EVENT HANDLING
    # ───────────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            
        # Handle window resizing
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            jungle_floor = pygame.Rect(0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT)
            water_rect.y = SCREEN_HEIGHT - FLOOR_HEIGHT - lake_height
            
        # Key press events
        elif event.type == pygame.KEYDOWN:
            # ═══════════════════════════════════════════════════
            #  TITLE SCREEN: Any key starts game
            # ═══════════════════════════════════════════════════
            if current_state == TITLE_SCREEN:
                # Stop title music when transitioning to gameplay
                if title_music_playing:
                    pygame.mixer.music.stop()
                
                # Any key press transitions to gameplay
                current_state = PLAYING
                
                # ─────────────────────────────────────────────
                # Play start sound effect
                # ─────────────────────────────────────────────
                start_sound = pygame.mixer.Sound("assets/sounds/start_sound.wav")
                start_sound.play()

                # ─────────────────────────────────────────────
                #  OPTIONAL: Start gameplay music
                # ─────────────────────────────────────────────

                # if music_loaded:
                #     pygame.mixer.music.load("assets/sounds/gameplay_music.mp3")
                #     pygame.mixer.music.set_volume(gameplay_music_volume)  # Apply volume
                #     pygame.mixer.music.play(-1)  # Loop forever
                #     gameplay_music_playing = True
            
            # ═══════════════════════════════════════════════════
            #  GAMEPLAY: Space bar jumps
            # ═══════════════════════════════════════════════════
            elif current_state == PLAYING:
                if event.key == pygame.K_SPACE and on_ground:
                    velocity_y = jump_power
                    on_ground = False

    # ───────────────────────────────────────────────────────────
    #  RENDER APPROPRIATE SCREEN BASED ON GAME STATE
    # ───────────────────────────────────────────────────────────
    
    # Show title screen first
    if current_state == TITLE_SCREEN:
        draw_title_screen()
        continue  # Skip game logic, just show title screen
    
    # Show win screen if player won
    if current_state == WIN_STATE:
        draw_win_screen()
        continue  # Skip game logic, just show win screen
    
    # ═══════════════════════════════════════════════════════════
    #  GAMEPLAY LOGIC (only runs when current_state == PLAYING)
    # ═══════════════════════════════════════════════════════════
    
    # Player movement
    keys = pygame.key.get_pressed()
    new_x = player_rect.x
    if keys[pygame.K_LEFT]: 
        new_x -= player_speed
    if keys[pygame.K_RIGHT]: 
        new_x += player_speed

    # Check if in water (slower movement)
    temp_rect = pygame.Rect(new_x, player_rect.y, player_rect.width, player_rect.height)
    speed = 2 if temp_rect.colliderect(water_rect) else player_speed

    # Apply movement
    if keys[pygame.K_LEFT]: 
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]: 
        player_rect.x += speed

    # Gravity and jumping
    velocity_y += gravity
    player_rect.y += velocity_y

    # Ground collision
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

    # Energy drain over time
    current_energy -= energy_drain
    if current_energy <= 0:
        current_energy = 0
        current_state = GAME_OVER_STATE

    # Banana #1 collection (restores energy)
    if player_rect.colliderect(banana_rect):
        current_energy = min(current_energy + energy_gain, max_energy)
        banana_rect.topleft = (-100, -100)  # Move offscreen

    # Banana #2 collection (WIN CONDITION!)
    if banana2_active and player_rect.colliderect(banana2_rect):
        banana2_active = False
        banana2_rect.topleft = (-100, -100)
        current_state = WIN_STATE

    # Cloud movement for atmosphere
    cloud_positions[0] -= cloud_speed
    cloud_positions[1] -= cloud_speed * 1.5
    for i in range(2):
        if cloud_positions[i] <= -SCREEN_WIDTH:
            cloud_positions[i] = 0

    # ───────────────────────────────────────────────────────────
    #  DRAWING GAME WORLD
    # ───────────────────────────────────────────────────────────
    screen.fill(SKY_BLUE)

    # Draw clouds
    for i, cloud in enumerate(clouds):
        cx = cloud_positions[i]
        for (x, y, r) in cloud:
            pygame.draw.circle(screen, WHITE, (int(x + cx), y), r)
            pygame.draw.circle(screen, WHITE, (int(x + cx + SCREEN_WIDTH), y), r)

    # Draw ground
    pygame.draw.rect(screen, DARK_SOIL, jungle_floor)
    pygame.draw.rect(screen, JUNGLE_GREEN, (0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, 20))
    
    # Draw water hazard
    pygame.draw.rect(screen, WATER_BLUE, water_rect, border_radius=5)
    pygame.draw.rect(screen, (0, 50, 150), water_rect, width=2, border_radius=5)

    # Draw platforms
    for platform in platforms:
        platform.draw(screen)

    # Draw collectibles
    pygame.draw.rect(screen, YELLOW, banana_rect)
    if banana2_active:
        pygame.draw.rect(screen, YELLOW, banana2_rect)

    # Draw player
    screen.blit(tiger_img, player_rect)

    # Draw energy bar (top left corner)
    pygame.draw.rect(screen, (100, 100, 100), (10, 10, 200, 20))
    fill_width = int((current_energy / max_energy) * 200)
    pygame.draw.rect(screen, YELLOW, (10, 10, fill_width, 20))

    # Draw game over message if needed
    if current_state == GAME_OVER_STATE:
        game_over_surface = font.render("GAME OVER!", True, RED)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(game_over_surface, game_over_rect)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
sys.exit()