import pygame
import sys
import os
import json
import random

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
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kian's Powerful, Deadly Pong!")

# Font settings
font = pygame.font.Font(pygame.font.get_default_font(), 32)  # Larger font and size
game_over_font = pygame.font.Font(pygame.font.get_default_font(), 144)  # Larger font for game over text
pause_font = pygame.font.Font(pygame.font.get_default_font(), 72)  # Font for pause message
explosion_font = pygame.font.Font(pygame.font.get_default_font(), 48)  # Font for explosion text
powerup_font = pygame.font.Font(pygame.font.get_default_font(), 48)  # Font for power-up text

# ASCII Art for the name "Kian"
ascii_kian = """
K I A N ' S  P O W E R F U L ,  D E A D L Y   P O N G! ! !
"""

# Load sounds
hit_sound = pygame.mixer.Sound("sound/hit_sound.wav")
score_sound = pygame.mixer.Sound("sound/score_sound.wav")
game_over_sound = pygame.mixer.Sound("sound/game_over_sound.wav")
powerup_spawn_sound = pygame.mixer.Sound("sound/powerup_spawn.wav")
powerup_claim_sound = pygame.mixer.Sound("sound/powerup_claim.wav")
explosion_sound = pygame.mixer.Sound("sound/explosion_sound.wav")
laser_sound = pygame.mixer.Sound("sound/laser_sound.wav")

# Load background music
pygame.mixer.music.load("sound/background_music.wav")
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Leaderboard file path
LEADERBOARD_FILE = "leaderboard.json"

# Power-up types
POWERUPS = ["Laser", "Explosion", "Double Ball", "Slowdown", "Bouncewall"]
POWERUP_LETTERS = {
    "Laser": "L",
    "Explosion": "E",
    "Double Ball": "D",
    "Slowdown": "S",
    "Bouncewall": "B"
}

# Create paddle texture
def create_paddle_texture(width, height):
    paddle_surface = pygame.Surface((width, height))
    paddle_surface.fill(WHITE)
    for i in range(0, height, 20):
        pygame.draw.line(paddle_surface, BLACK, (0, i), (width, i), 4)
    return paddle_surface

# Create ball texture
def create_ball_texture(radius):
    ball_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(ball_surface, WHITE, (radius, radius), radius)
    pygame.draw.circle(ball_surface, BLACK, (radius, radius), radius, 4)
    return ball_surface

# Create power-up texture
def create_powerup_texture(size):
    powerup_surface = pygame.Surface((size, size))
    powerup_surface.fill(YELLOW)
    pygame.draw.rect(powerup_surface, BLACK, powerup_surface.get_rect(), 4)
    return powerup_surface

# Create net texture
def create_net_texture(size):
    net_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(net_surface, CYAN, (size // 2, size // 2), size // 2, 4)
    return net_surface

# Load assets function
def load_assets():
    global paddle_texture, ball_texture, powerup_texture, net_texture
    paddle_texture = create_paddle_texture(PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_texture = create_ball_texture(BALL_RADIUS)
    powerup_texture = create_powerup_texture(POWERUP_SIZE)
    net_texture = create_net_texture(NET_SIZE)

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

# Power-up settings
powerups = []
active_powerups = []
stored_powerups = []

# Control method
control_method = None

# Power-up timers
bouncewall_timer = 0
slowdown_timer = 0
powerup_active = None

# Hide system cursor and grab the mouse cursor
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

def add_ball():
    ball_speed_x, ball_speed_y = 14, 14
    new_ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    balls.append({"rect": new_ball, "speed_x": ball_speed_x, "speed_y": ball_speed_y})

def move_paddle_scroll(scroll_amount):
    paddle.y += scroll_amount * paddle_speed
    paddle.clamp_ip(screen.get_rect())

def move_paddle_mouse():
    mouse_y = pygame.mouse.get_pos()[1]
    paddle.y = mouse_y - PADDLE_HEIGHT // 2
    paddle.clamp_ip(screen.get_rect())

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
            if random.random() < 0.2:
                spawn_powerup()
        if ball["rect"].right >= WIDTH:
            balls.remove(ball)
            lives -= 1
            hit_sound.play()
            if lives <= 0:
                game_over_sound.play()

def move_powerups():
    for powerup in powerups[:]:
        powerup["rect"].y += 7
        if powerup["rect"].top > HEIGHT:
            powerups.remove(powerup)

def animate_powerup(powerup):
    if "animation" not in powerup:
        powerup["animation"] = {
            "scale": 1,
            "direction": 1
        }
    scale = powerup["animation"]["scale"]
    direction = powerup["animation"]["direction"]
    if scale >= 1.2:
        direction = -1
    elif scale <= 1:
        direction = 1
    scale += direction * 0.02
    powerup["animation"]["scale"] = scale
    powerup["animation"]["direction"] = direction
    return pygame.transform.scale(powerup_texture, (int(POWERUP_SIZE * scale), int(POWERUP_SIZE * scale)))

def spawn_powerup():
    powerup_type = random.choice(POWERUPS)
    new_powerup = {
        "type": powerup_type,
        "rect": pygame.Rect(random.randint(0, WIDTH - POWERUP_SIZE), 0, POWERUP_SIZE, POWERUP_SIZE)
    }
    powerups.append(new_powerup)
    powerup_spawn_sound.play()

def claim_powerup(mouse_pos):
    for powerup in powerups:
        if powerup["rect"].collidepoint(mouse_pos):
            if len(stored_powerups) < 2:
                stored_powerups.append(powerup["type"])
                powerup_claim_sound.play()
            powerups.remove(powerup)
            break

def use_powerup():
    if stored_powerups:
        active_powerup = stored_powerups.pop(0)
        if active_powerup == "Laser":
            laser_powerup()
        elif active_powerup == "Explosion":
            explosion_powerup()
        elif active_powerup == "Double Ball":
            double_ball_powerup()
        elif active_powerup == "Slowdown":
            slowdown_powerup()
        elif active_powerup == "Bouncewall":
            bouncewall_powerup()

def laser_powerup():
    global balls, score
    laser_sound.play()
    beam_height = 20
    beam_color1 = YELLOW
    beam_color2 = BLUE
    for _ in range(30):  # 30 frames for the animation
        screen.fill(BLACK)
        y_offset = render_ascii_art()
        draw_game_elements(y_offset)
        pygame.draw.rect(screen, beam_color1, (0, paddle.centery - beam_height // 2, WIDTH, beam_height))
        pygame.draw.rect(screen, beam_color2, (0, paddle.centery - beam_height // 2, WIDTH, beam_height), 5)
        pygame.display.flip()
        pygame.time.delay(50)
        beam_color1, beam_color2 = beam_color2, beam_color1
    for ball in balls[:]:
        if paddle.top <= ball["rect"].centery <= paddle.bottom:
            score += 1
            ball_pos = ball["rect"].topleft
            balls.remove(ball)
            draw_explosion(ball_pos)

def draw_explosion(pos):
    explosion_text = "BOOM!"
    for _ in range(10):  # Display explosion for a short duration
        screen.fill(BLACK)
        y_offset = render_ascii_art()
        draw_game_elements(y_offset)
        explosion_surface = explosion_font.render(explosion_text, True, random.choice([RED, YELLOW]))
        screen.blit(explosion_surface, pos)
        pygame.display.flip()
        pygame.time.delay(100)

def explosion_powerup():
    global balls, score
    explosion_sound.play()
    score += len(balls)
    balls = []
    explosion_animation()

def explosion_animation():
    explosion_duration = 30
    for i in range(explosion_duration):
        screen.fill(RED if i % 2 == 0 else ORANGE)
        pygame.display.flip()
        pygame.time.delay(100)  # Slower flashing with 100ms delay

def double_ball_powerup():
    new_balls = []
    for ball in balls:
        new_ball = ball["rect"].copy()
        new_balls.append({"rect": new_ball, "speed_x": -ball["speed_x"], "speed_y": -ball["speed_y"]})
    balls.extend(new_balls)

def slowdown_powerup():
    global slowdown_timer, powerup_active
    for ball in balls:
        ball["speed_x"] /= 2
        ball["speed_y"] /= 2
    slowdown_timer = 10  # 10 seconds
    powerup_active = "Slowdown"
    pygame.time.set_timer(pygame.USEREVENT, 10000)  # Reset after 10 seconds

def bouncewall_powerup():
    global PADDLE_HEIGHT, paddle, bouncewall_timer, powerup_active, paddle_texture
    PADDLE_HEIGHT *= 3
    paddle.height = PADDLE_HEIGHT
    paddle_texture = create_paddle_texture(PADDLE_WIDTH, PADDLE_HEIGHT)
    bouncewall_timer = 10  # 10 seconds
    powerup_active = "Bouncewall"
    pygame.time.set_timer(pygame.USEREVENT + 1, 10000)  # Reset after 10 seconds

def reset_speeds():
    global powerup_active
    for ball in balls:
        ball["speed_x"] *= 2
        ball["speed_y"] *= 2
    powerup_active = None

def reset_paddle():
    global PADDLE_HEIGHT, paddle, powerup_active, paddle_texture
    PADDLE_HEIGHT = 180
    paddle.height = PADDLE_HEIGHT
    paddle_texture = create_paddle_texture(PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    powerup_active = None

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
    for powerup in powerups:
        animated_texture = animate_powerup(powerup)
        screen.blit(animated_texture, (powerup["rect"].x, powerup["rect"].y, animated_texture.get_width(), animated_texture.get_height()))
        powerup_letter = POWERUP_LETTERS[powerup["type"]]
        powerup_letter_surface = powerup_font.render(powerup_letter, True, BLACK)
        screen.blit(powerup_letter_surface, powerup["rect"].topleft)
    draw_stored_powerups(y_offset + 60)
    draw_net()
    if powerup_active:
        if powerup_active == "Bouncewall":
            timer_text = f"Bouncewall: {bouncewall_timer} seconds"
        elif powerup_active == "Slowdown":
            timer_text = f"Slowdown: {slowdown_timer} seconds"
        timer_surface = font.render(timer_text, True, WHITE)
        screen.blit(timer_surface, (WIDTH // 2 - timer_surface.get_width() // 2, y_offset + 80))
    pygame.display.flip()

def draw_game_elements(y_offset):
    score_text = f"Score: {score}"
    score_surface = font.render(score_text, True, WHITE)
    screen.blit(score_surface, (20, y_offset + 20))
    lives_text = f"Lives: {lives}"
    lives_surface = font.render(lives_text, True, WHITE)
    screen.blit(lives_surface, (WIDTH - lives_surface.get_width() - 20, y_offset + 20))
    screen.blit(paddle_texture, paddle.topleft)
    for ball in balls:
        screen.blit(ball_texture, ball["rect"].topleft)
    for powerup in powerups:
        animated_texture = animate_powerup(powerup)
        screen.blit(animated_texture, (powerup["rect"].x, powerup["rect"].y, animated_texture.get_width(), animated_texture.get_height()))
        powerup_letter = POWERUP_LETTERS[powerup["type"]]
        powerup_letter_surface = powerup_font.render(powerup_letter, True, BLACK)
        screen.blit(powerup_letter_surface, powerup["rect"].topleft)
    draw_stored_powerups(y_offset + 60)
    draw_net()

def draw_stored_powerups(y_offset):
    for i, powerup in enumerate(stored_powerups):
        powerup_text = f"[{powerup}]"
        powerup_surface = font.render(powerup_text, True, WHITE)
        screen.blit(powerup_surface, (20 + i * 200, y_offset))

def draw_net():
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(net_texture, (mouse_pos[0] - NET_SIZE // 2, mouse_pos[1] - NET_SIZE // 2))

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

# Load assets at the start of the game
load_assets()

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
        if bouncewall_timer > 0:
            bouncewall_timer -= 1
        if slowdown_timer > 0:
            slowdown_timer -= 1
        last_update = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not paused:
                add_ball()
            elif event.key == pygame.K_r and game_over:
                game_over = False
                name_captured = False
                score = 0
                lives = 10
                balls.clear()
                powerups.clear()
                stored_powerups.clear()
                add_ball()
            elif event.key == pygame.K_l and game_over:
                display_leaderboard()
            elif event.key == pygame.K_ESCAPE and not game_over:
                paused = True
                pygame.event.set_grab(False)
                pause_screen()
        elif event.type == pygame.MOUSEWHEEL and control_method == "scroll" and not game_over and not paused:
            move_paddle_scroll(event.y)
        elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
            if event.button == 1 and not game_over:
                claim_powerup(event.pos)
            elif event.button == 3 and not game_over:
                use_powerup()
        elif event.type == pygame.USEREVENT:
            reset_speeds()
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
                            add_ball()
                            pygame.event.set_grab(True)
                            pygame.mouse.set_visible(False)
                            break
                if not game_over:
                    break
    elif not game_over and not paused:
        if control_method == "mouse":
            move_paddle_mouse()
        move_balls()
        move_powerups()
        if lives <= 0:
            game_over = True
        draw(20)

    clock.tick(60)  # FPS
