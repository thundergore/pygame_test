# game/drawing.py

import pygame
from game.powerups import animate_powerup, POWERUP_LETTERS

def render_ascii_art(screen, font, ascii_kian, y_offset=20):
    for line in ascii_kian.splitlines():
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (20, y_offset))
        y_offset += 36
    return y_offset

def draw_game_elements(screen, font, y_offset, paddle_texture, ball_texture, net_texture, balls, powerups, stored_powerups, paddle, powerup_font, score, lives, powerup_active, bouncewall_timer, slowdown_timer, ascii_kian):
    screen.fill((0, 0, 0))
    y_offset = render_ascii_art(screen, font, ascii_kian, y_offset)
    
    score_text = f"Score: {score}"
    score_surface = font.render(score_text, True, (255, 255, 255))
    screen.blit(score_surface, (20, y_offset + 20))
    
    lives_text = f"Lives: {lives}"
    lives_surface = font.render(lives_text, True, (255, 255, 255))
    screen.blit(lives_surface, (screen.get_width() - lives_surface.get_width() - 20, y_offset + 20))
    
    screen.blit(paddle_texture, paddle.topleft)
    
    for ball in balls:
        screen.blit(ball_texture, ball["rect"].topleft)
    for powerup in powerups:
        animated_texture = animate_powerup(powerup)
        screen.blit(animated_texture, (powerup["rect"].x, powerup["rect"].y, animated_texture.get_width(), animated_texture.get_height()))
        powerup_letter = POWERUP_LETTERS[powerup["type"]]
        powerup_letter_surface = powerup_font.render(powerup_letter, True, (0, 0, 0))
        letter_x = powerup["rect"].x + (POWERUP_SIZE - powerup_letter_surface.get_width()) // 2
        letter_y = powerup["rect"].y + (POWERUP_SIZE - powerup_letter_surface.get_height()) // 2
        screen.blit(powerup_letter_surface, (letter_x, letter_y))
    
    draw_stored_powerups(screen, font, y_offset + 60, stored_powerups)
    draw_net(screen, net_texture)
    
    if powerup_active:
        if powerup_active == "Bouncewall":
            timer_text = f"Bouncewall: {bouncewall_timer} seconds"
        elif powerup_active == "Slowdown":
            timer_text = f"Slowdown: {slowdown_timer} seconds"
        timer_surface = font.render(timer_text, True, (255, 255, 255))
        screen.blit(timer_surface, (screen.get_width() // 2 - timer_surface.get_width() // 2, y_offset + 80))
    
    pygame.display.flip()

def draw_stored_powerups(screen, font, y_offset, stored_powerups):
    for i, powerup in enumerate(stored_powerups):
        powerup_text = f"[{powerup}]"
        powerup_surface = font.render(powerup_text, True, (255, 255, 255))
        screen.blit(powerup_surface, (20 + i * 200, y_offset))

def draw_net(screen, net_texture):
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(net_texture, (mouse_pos[0] - net_texture.get_width() // 2, mouse_pos[1] - net_texture.get_height() // 2))
