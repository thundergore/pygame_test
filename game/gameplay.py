# game/gameplay.py

import pygame
import random
from game.powerups import spawn_powerup, animate_powerup, POWERUP_LETTERS
from game.sound import play_sound

def add_ball(balls, width, height, ball_radius):
    ball_speed_x, ball_speed_y = 14, 14
    new_ball = pygame.Rect(width // 2, height // 2, ball_radius * 2, ball_radius * 2)
    balls.append({"rect": new_ball, "speed_x": ball_speed_x, "speed_y": ball_speed_y})

def move_balls(balls, paddle, score, lives, screen_height, screen_width, hit_sound, score_sound, game_over_sound):
    for ball in balls[:]:
        ball["rect"].x += ball["speed_x"]
        ball["rect"].y += ball["speed_y"]
        if ball["rect"].top <= 0 or ball["rect"].bottom >= screen_height:
            ball["speed_y"] *= -1
            hit_sound.play()
        if ball["rect"].left <= 0:
            ball["speed_x"] *= -1
            score += 1
            score_sound.play()
        if ball["rect"].colliderect(paddle):
            ball["speed_x"] *= -1
            offset = (ball["rect"].centery - paddle.centery) / (paddle.height // 2)
            ball["speed_y"] += offset * 10
            hit_sound.play()
            if random.random() < 0.2:
                spawn_powerup()
        if ball["rect"].right >= screen_width:
            balls.remove(ball)
            lives -= 1
            hit_sound.play()
            if lives <= 0:
                game_over_sound.play()
    return score, lives

def move_powerups(powerups, screen_height):
    for powerup in powerups[:]:
        powerup["rect"].y += 7
        if powerup["rect"].top > screen_height:
            powerups.remove(powerup)

def claim_powerup(powerups, stored_powerups, mouse_pos, powerup_claim_sound):
    for powerup in powerups:
        if powerup["rect"].collidepoint(mouse_pos):
            if len(stored_powerups) < 2:
                stored_powerups.append(powerup["type"])
                powerup_claim_sound.play()
            powerups.remove(powerup)
            break

def use_powerup(stored_powerups, balls, score, powerup_active, powerup_timers, sounds):
    if stored_powerups:
        active_powerup = stored_powerups.pop(0)
        if active_powerup == "Laser":
            score = laser_powerup(balls, score, sounds["laser_sound"])
        elif active_powerup == "Explosion":
            score = explosion_powerup(balls, score, sounds["explosion_sound"])
        elif active_powerup == "Double Ball":
            double_ball_powerup(balls)
        elif active_powerup == "Slowdown":
            slowdown_powerup(balls, powerup_timers)
        elif active_powerup == "Bouncewall":
            bouncewall_powerup(powerup_timers)
    return powerup_active

def laser_powerup(balls, score, laser_sound):
    laser_sound.play()
    beam_height = 20
    beam_color1 = (255, 255, 0)
    beam_color2 = (0, 0, 255)
    for _ in range(30):  # 30 frames for the animation
        screen.fill((0, 0, 0))
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
    return score

def draw_explosion(pos):
    explosion_text = "BOOM!"
    for _ in range(10):  # Display explosion for a short duration
        screen.fill((0, 0, 0))
        y_offset = render_ascii_art()
        draw_game_elements(y_offset)
        explosion_surface = explosion_font.render(explosion_text, True, random.choice([(255, 0, 0), (255, 255, 0)]))
        screen.blit(explosion_surface, pos)
        pygame.display.flip()
        pygame.time.delay(100)

def explosion_powerup(balls, score, explosion_sound):
    explosion_sound.play()
    score += len(balls)
    balls.clear()
    explosion_animation()
    return score

def explosion_animation():
    explosion_duration = 30
    for i in range(explosion_duration):
        screen.fill((255, 0, 0) if i % 2 == 0 else (255, 165, 0))
        pygame.display.flip()
        pygame.time.delay(100)  # Slower flashing with 100ms delay

def double_ball_powerup(balls):
    new_balls = []
    for ball in balls:
        new_ball = ball["rect"].copy()
        new_balls.append({"rect": new_ball, "speed_x": -ball["speed_x"], "speed_y": -ball["speed_y"]})
    balls.extend(new_balls)

def slowdown_powerup(balls, powerup_timers):
    for ball in balls:
        ball["speed_x"] /= 2
        ball["speed_y"] /= 2
    powerup_timers["slowdown_timer"] = 10  # 10 seconds

def bouncewall_powerup(powerup_timers):
    global PADDLE_HEIGHT, paddle, paddle_texture
    PADDLE_HEIGHT *= 3
    paddle.height = PADDLE_HEIGHT
    paddle_texture = create_paddle_texture(PADDLE_WIDTH, PADDLE_HEIGHT)
    powerup_timers["bouncewall_timer"] = 10  # 10 seconds

def reset_speeds(balls):
    for ball in balls:
        ball["speed_x"] *= 2
        ball["speed_y"] *= 2

def reset_paddle():
    global PADDLE_HEIGHT, paddle, paddle_texture
    PADDLE_HEIGHT = 180
    paddle.height = PADDLE_HEIGHT
    paddle_texture = create_paddle_texture(PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
