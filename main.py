import pygame
import sys
from settings import *
from assets.load_assets import load_assets
from utils.leaderboard import load_leaderboard, save_leaderboard, update_leaderboard, display_leaderboard, get_player_name
from utils.draw_elements import draw, draw_game_elements, render_ascii_art
from utils.powerups import use_powerup, rocket_powerup, explosion_powerup, double_ball_powerup, slowdown_powerup, bouncewall_powerup, reset_speeds, reset_paddle
from utils.controls import control_selection_screen, select_control_method, move_paddle_scroll, move_paddle_mouse
from sounds.sounds import hit_sound, score_sound, game_over_sound, powerup_spawn_sound, powerup_claim_sound, explosion_sound, laser_sound

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

font = pygame.font.Font(pygame.font.get_default_font(), 32)
game_over_font = pygame.font.Font(pygame.font.get_default_font(), 144)

load_assets()

balls = []
powerups = []
stored_powerups = []
leaderboard = load_leaderboard()

control_method = None

def add_ball():
    ball_speed_x, ball_speed_y = 14, 14
    new_ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    balls.append({"rect": new_ball, "speed_x": ball_speed_x, "speed_y": ball_speed_y})

running = True
game_over = False
name_captured = False
clock = pygame.time.Clock()

control_selection_screen(screen, font)
control_method = select_control_method()

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
                powerups.clear()
                stored_powerups.clear()
                add_ball()
            elif event.key == pygame.K_l and game_over:
                display_leaderboard(screen, font, leaderboard)
        elif event.type == pygame.MOUSEWHEEL and control_method == "scroll" and not game_over:
            move_paddle_scroll(event.y, paddle)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not game_over:
                claim_powerup(event.pos, powerups, stored_powerups)
            elif event.button == 3 and not game_over:
                use_powerup()
        elif event.type == pygame.USEREVENT:
            reset_speeds(balls)
        elif event.type == pygame.USEREVENT + 1:
            reset_paddle(paddle)

    if game_over and not name_captured:
        game_over_screen()
        name_captured = True
    elif not game_over:
        if control_method == "mouse":
            move_paddle_mouse(paddle)
        move_balls(balls, paddle, powerups, stored_powerups, score, lives)
        move_powerups(powerups)
        if lives <= 0:
            game_over = True
        draw(screen, font, paddle, balls, powerups, stored_powerups, score, lives, render_ascii_art)

    clock.tick(60)
