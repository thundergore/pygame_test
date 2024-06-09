import pygame
import sys
import os
import json

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
PADDLE_WIDTH, PADDLE_HEIGHT = 30, 180
BALL_RADIUS = 14
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Font settings
font = pygame.font.Font(pygame.font.get_default_font(), 32)  # Larger font and size
game_over_font = pygame.font.Font(pygame.font.get_default_font(), 144)  # Larger font for game over text

# ASCII Art for the name "Kian"
ascii_kian = """
K I A N ' S   D E A D L Y   P O N G! ! !
"""

# Load sounds
hit_sound = pygame.mixer.Sound("hit_sound.wav")
score_sound = pygame.mixer.Sound("score_sound.wav")
game_over_sound = pygame.mixer.Sound("game_over_sound.wav")

# Load background music
pygame.mixer.music.load("background_music.wav")
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Leaderboard file path
LEADERBOARD_FILE = "leaderboard.json"

# Create paddle texture
def create_paddle_texture(width, height):
    # Create a surface for the paddle texture
    paddle_surface = pygame.Surface((width, height))
    
    # Fill with a base color
    paddle_surface.fill(WHITE)
    
    # Draw stripes on the paddle
    for i in range(0, height, 20):
        pygame.draw.line(paddle_surface, BLACK, (0, i), (width, i), 4)
    
    return paddle_surface

# Create ball texture
def create_ball_texture(radius):
    # Create a surface for the ball texture
    ball_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    
    # Draw a filled circle
    pygame.draw.circle(ball_surface, WHITE, (radius, radius), radius)
    
    # Add a border
    pygame.draw.circle(ball_surface, BLACK, (radius, radius), radius, 4)
    
    return ball_surface

# Load assets function
def load_assets():
    global paddle_texture, ball_texture
    paddle_texture = create_paddle_texture(PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_texture = create_ball_texture(BALL_RADIUS)

# Render ASCII art
def render_ascii_art():
    y_offset = 20  # Start drawing ASCII art at this y-offset
    for line in ascii_kian.splitlines():
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (20, y_offset))  # Adjust x-offset as needed
        y_offset += 36  # Move to the next line
    return y_offset

# Paddle settings
paddle_speed = 30
paddle = pygame.Rect(
    WIDTH - PADDLE_WIDTH - 20,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)

# Ball settings and score
balls = []
score = 0
lives = 10

def add_ball():
    # New ball at the center with random initial direction
    ball_speed_x, ball_speed_y = 14, 14
    new_ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    balls.append({"rect": new_ball, "speed_x": ball_speed_x, "speed_y": ball_speed_y})

# Initially start with one ball - optional
# add_ball()

def move_paddle():
    mouse_y = pygame.mouse.get_pos()[1]
    paddle.y = mouse_y - PADDLE_HEIGHT // 2
    paddle.clamp_ip(screen.get_rect())  # Keep the paddle within the screen boundaries

# Modify the existing functions to include sound effects
def move_balls():
    global lives, score
    for ball in balls[:]:
        ball["rect"].x += ball["speed_x"]
        ball["rect"].y += ball["speed_y"]
        if ball["rect"].top <= 0 or ball["rect"].bottom >= HEIGHT:
            ball["speed_y"] *= -1
            hit_sound.play()
        if ball["rect"].left <= 0:
            ball["speed_x"] *= -1
            score += 1
            score_sound.play()
        if ball["rect"].colliderect(paddle):
            ball["speed_x"] *= -1
            offset = (ball["rect"].centery - paddle.centery) / (PADDLE_HEIGHT // 2)
            ball["speed_y"] += offset * 10
            hit_sound.play()
        if ball["rect"].right >= WIDTH:
            balls.remove(ball)
            lives -= 1
            hit_sound.play()
            if lives <= 0:
                game_over_sound.play()

def draw(y_offset):
    screen.fill(BLACK)
    y_offset = render_ascii_art()  # Draw the ASCII art at the top of the screen
    score_text = f"Score: {score}"
    score_surface = font.render(score_text, True, WHITE)
    screen.blit(score_surface, (20, y_offset + 20))
    lives_text = f"Lives: {lives}"
    lives_surface = font.render(lives_text, True, WHITE)
    screen.blit(lives_surface, (WIDTH - lives_surface.get_width() - 20, y_offset + 20))
    screen.blit(paddle_texture, paddle.topleft)
    for ball in balls:
        screen.blit(ball_texture, ball["rect"].topleft)
    pygame.display.flip()

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE) and os.path.getsize(LEADERBOARD_FILE) > 0:
        try:
            with open(LEADERBOARD_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as file:
        json.dump(leaderboard, file)

leaderboard = load_leaderboard()

def update_leaderboard(name, new_score):
    leaderboard.append({"name": name, "score": new_score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    if len(leaderboard) > 20:
        leaderboard.pop()
    save_leaderboard(leaderboard)

def display_leaderboard():
    screen.fill(BLACK)
    title_surface = font.render("Leaderboard", True, WHITE)
    screen.blit(
        title_surface,
        (WIDTH // 2 - title_surface.get_width() // 2, 50),
    )
    for i, entry in enumerate(leaderboard[:20]):
        score_surface = font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, WHITE)
        screen.blit(
            score_surface,
            (WIDTH // 2 - score_surface.get_width() // 2, 100 + i * 30),
        )
    pygame.display.flip()

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
    display_leaderboard()

    restart_text = "Press R to Restart"
    restart_surface = font.render(restart_text, True, WHITE)
    screen.blit(
        restart_surface,
        (
            WIDTH // 2 - restart_surface.get_width() // 2,
            HEIGHT // 2 - restart_surface.get_height() // 2 + 200,
        ),
    )

    pygame.display.flip()

# Load assets at the start of the game
load_assets()

# Game loop
running = True
game_over = False
name_captured = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                add_ball()
            elif event.key == pygame.K_r and game_over:
                game_over = False
                name_captured = False
                score = 0
                lives = 10
                balls.clear()
                add_ball()
            elif event.key == pygame.K_l and game_over:
                display_leaderboard()

    if game_over and not name_captured:
        game_over_screen()
        name_captured = True
    elif not game_over:
        move_paddle()
        move_balls()
        if lives <= 0:
            game_over = True
        draw(20)

    clock.tick(60)  # FPS
