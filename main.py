# main.py

import pygame
import sys
from assets.load_assets import load_assets
from game.controls import move_paddle_scroll, move_paddle_mouse
from game.drawing import draw_game_elements, render_ascii_art
from game.gameplay import add_ball, move_balls, move_powerups, claim_powerup, use_powerup, reset_speeds, reset_paddle, draw_explosion
from game.leaderboard import load_leaderboard, update_leaderboard, display_leaderboard
from game.sound import play_sound

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
PADDLE_WIDTH, PADDLE_HEIGHT = 30, 180
BALL_RADIUS = 14
POWERUP_SIZE = 30
NET_SIZE = 40
# Colors
WHITE, BLACK, RED, GREEN, BLUE, YELLOW, CYAN, ORANGE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 165, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kian's Powerful, Deadly Pong!")

# Font settings
font = pygame.font.Font(pygame.font.get_default_font(), 32)
game_over_font = pygame.font.Font(pygame.font.get_default_font(), 144)
pause_font = pygame.font.Font(pygame.font.get_default_font(), 72)
explosion_font = pygame.font.Font(pygame.font.get_default_font(), 48)
powerup_font = pygame.font.Font(pygame.font.get_default_font(), 48)

# ASCII Art for the name "Kian"
ascii_kian = """
K I A N ' S  P O W E R F U L ,  D E A D L Y   P O N G! ! !
"""

# Load sounds
hit_sound = pygame.mixer.Sound("resources/hit_sound.wav")
score_sound = pygame.mixer.Sound("resources/score_sound.wav")
game_over_sound = pygame.mixer.Sound("resources/game_over_sound.wav")
powerup_spawn_sound = pygame.mixer.Sound("resources/powerup_spawn.wav")
powerup_claim_sound = pygame.mixer.Sound("resources/powerup_claim.wav")
explosion_sound = pygame.mixer.Sound("resources/explosion_sound.wav")
laser_sound = pygame.mixer.Sound("resources/laser_sound.wav")

# Load background music
pygame.mixer.music.load("resources/background_music.wav")
pygame.mixer.music.play(-1)

# Power-up timers
powerup_timers = {
    "bouncewall_timer": 0,
    "slowdown_timer": 0
}

# Load assets
paddle_texture, ball_texture, powerup_texture, net_texture = load_assets()

# Paddle settings
paddle_speed = 30
paddle = pygame.Rect(
    WIDTH - PADDLE_WIDTH - 20,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)

print(f"Initial paddle position: {paddle.x}, {paddle.y}")

# Ball settings and score
balls = []
score = 0
lives = 10

# Power-up settings
powerups = []
stored_powerups = []

# Control method
control_method = None

# Power-up state
powerup_active = None

# Hide system cursor and grab the mouse cursor
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Load leaderboard
leaderboard = load_leaderboard()

def get_player_name():
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        screen.fill(BLACK)
        name_surface = font.render(f"Enter your name: {name}", True, WHITE)
        screen.blit(name_surface, (WIDTH // 2 - name_surface.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
    return name

def game_over_screen():
    screen.fill(RED)
    game_over_text = "G A M E  O V E R"
    game_over_surface = game_over_font.render(game_over_text, True, WHITE)
    screen.blit(
        game_over_surface,
        (
            WIDTH // 2 - game_over_surface.get_width() // 2,
            HEIGHT // 2 - game_over_surface.get_height() // 2 - 80,
        ),
    )

    end_game_score_text = f"Final Score: {score}"
    end_game_score_surface = font.render(end_game_score_text, True, WHITE)
    screen.blit(
        end_game_score_surface,
        (
            WIDTH // 2 - end_game_score_surface.get_width() // 2,
            HEIGHT // 2 - end_game_score_surface.get_height() // 2 + 80,
        ),
    )

    pygame.display.flip()

    name = get_player_name()
    update_leaderboard(name, score)

    screen.fill(BLACK)
    display_leaderboard(screen, font)

    quit_restart_text = "Quit Y/N?"
    quit_restart_surface = font.render(quit_restart_text, True, WHITE)
    screen.blit(
        quit_restart_surface,
        (
            WIDTH // 2 - quit_restart_surface.get_width() // 2,
            HEIGHT // 2 - quit_restart_surface.get_height() // 2 + 200,
        ),
    )

    pygame.display.flip()
    return "quit_check"

def control_selection_screen():
    screen.fill(BLACK)
    option_1 = "1. Scroll Wheel Control"
    option_2 = "2. Mouse Control"
    option_1_surface = font.render(option_1, True, WHITE)
    option_2_surface = font.render(option_2, True, WHITE)
    screen.blit(option_1_surface, (WIDTH // 2 - option_1_surface.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(option_2_surface, (WIDTH // 2 - option_2_surface.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

def select_control_method():
    global control_method
    control_selected = False
    while not control_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    control_method = "scroll"
                    control_selected = True
                elif event.key == pygame.K_2:
                    control_method = "mouse"
                    control_selected = True

def pause_screen():
    screen.fill(BLACK)
    pause_text = "Quit Y/N?"
    pause_surface = pause_font.render(pause_text, True, WHITE)
    screen.blit(
        pause_surface,
        (
            WIDTH // 2 - pause_surface.get_width() // 2,
            HEIGHT // 2 - pause_surface.get_height() // 2,
        ),
    )
    pygame.display.flip()

# Display control selection screen
control_selection_screen()
select_control_method()

# Game loop
running = True
game_over = False
paused = False
name_captured = False
clock = pygame.time.Clock()
last_update = pygame.time.get_ticks()

while running:
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= 1000:  # 1 second has passed
        if powerup_timers["bouncewall_timer"] > 0:
            powerup_timers["bouncewall_timer"] -= 1
        if powerup_timers["slowdown_timer"] > 0:
            powerup_timers["slowdown_timer"] -= 1
        last_update = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not paused:
                add_ball(balls, WIDTH, HEIGHT, BALL_RADIUS)
            elif event.key == pygame.K_r and game_over:
                game_over = False
                name_captured = False
                score = 0
                lives = 10
                balls.clear()
                powerups.clear()
                stored_powerups.clear()
                add_ball(balls, WIDTH, HEIGHT, BALL_RADIUS)
            elif event.key == pygame.K_l and game_over:
                display_leaderboard(screen, font)
            elif event.key == pygame.K_ESCAPE and not game_over:
                paused = True
                pygame.event.set_grab(False)
                pause_screen()
        elif event.type == pygame.MOUSEWHEEL and control_method == "scroll" and not game_over and not paused:
            move_paddle_scroll(paddle, event.y, paddle_speed, HEIGHT)
        elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
            if event.button == 1 and not game_over:
                claim_powerup(powerups, stored_powerups, event.pos, powerup_claim_sound)
            elif event.button == 3 and not game_over:
                powerup_active = use_powerup(stored_powerups, balls, score, powerup_active, powerup_timers, sounds={
                    "laser_sound": laser_sound,
                    "explosion_sound": explosion_sound
                })
        elif event.type == pygame.USEREVENT:
            reset_speeds(balls)
        elif event.type == pygame.USEREVENT + 1:
            reset_paddle()

    if paused:
        pause_screen()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_n:
                        paused = False
                        pygame.event.set_grab(True)
                        pygame.mouse.set_visible(False)

    if game_over and not name_captured:
        state = game_over_screen()
        if state == "quit_check":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_n:
                            game_over = False
                            name_captured = False
                            score = 0
                            lives = 10
                            balls.clear()
                            powerups.clear()
                            stored_powerups.clear()
                            add_ball(balls, WIDTH, HEIGHT, BALL_RADIUS)
                            pygame.event.set_grab(True)
                            pygame.mouse.set_visible(False)
                            break
                if not game_over:
                    break
    elif not game_over and not paused:
        if control_method == "mouse":
            move_paddle_mouse(paddle, HEIGHT)
        else:
            move_paddle_scroll(paddle, 0, paddle_speed, HEIGHT)  # Ensure the scroll method is used if not mouse
        score, lives = move_balls(balls, paddle, score, lives, HEIGHT, WIDTH, hit_sound, score_sound, game_over_sound)
        move_powerups(powerups, HEIGHT)
        if lives <= 0:
            game_over = True
        draw_game_elements(screen, font, 20, paddle_texture, ball_texture, net_texture, balls, powerups, stored_powerups, paddle, powerup_font, score, lives, powerup_active, powerup_timers["bouncewall_timer"], powerup_timers["slowdown_timer"], ascii_kian)
        print(f"Paddle position during game loop: {paddle.x}, {paddle.y}")

    clock.tick(60)  # FPS
