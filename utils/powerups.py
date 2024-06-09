import pygame
import random
from sounds.sounds import explosion_sound, laser_sound
from settings import WIDTH, HEIGHT, PADDLE_HEIGHT, YELLOW, RED, BALL_RADIUS

def use_powerup():
    if stored_powerups:
        active_powerup = stored_powerups.pop(0)
        if active_powerup == "Rocket":
            rocket_powerup()
        elif active_powerup == "Explosion":
            explosion_powerup()
        elif active_powerup == "Double Ball":
            double_ball_powerup()
        elif active_powerup == "Slowdown":
            slowdown_powerup()
        elif active_powerup == "Bouncewall":
            bouncewall_powerup()

def rocket_powerup():
    global balls, score
    laser_sound.play()
    
    beam_height = 20
    beam_color1 = YELLOW
    beam_color2 = BLUE
    for _ in range(30):
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
            balls.remove(ball)

def explosion_powerup():
    global balls, score
    explosion_sound.play()
    score += len(balls)
    balls = []
    explosion_animation()

def explosion_animation():
    explosion_duration = 30
    for i in range(explosion_duration):
        screen.fill(RED if i % 2 == 0 else YELLOW)
        pygame.display.flip()
        pygame.time.delay(30)

def double_ball_powerup():
    new_balls = []
    for ball in balls:
        new_ball = ball["rect"].copy()
        new_balls.append({"rect": new_ball, "speed_x": -ball["speed_x"], "speed_y": -ball["speed_y"]})
    balls.extend(new_balls)

def slowdown_powerup():
    for ball in balls:
        ball["speed_x"] /= 2
        ball["speed_y"] /= 2
    pygame.time.set_timer(pygame.USEREVENT, 10000)

def bouncewall_powerup():
    global PADDLE_HEIGHT, paddle
    PADDLE_HEIGHT = HEIGHT
    paddle = pygame.Rect(paddle.x, 0, PADDLE_WIDTH, HEIGHT)
    pygame.time.set_timer(pygame.USEREVENT + 1, 10000)

def reset_speeds():
    for ball in balls:
        ball["speed_x"] *= 2
        ball["speed_y"] *= 2

def reset_paddle():
    global PADDLE_HEIGHT, paddle
    PADDLE_HEIGHT = 180
    paddle.height = PADDLE_HEIGHT
    paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
