import pygame
from settings import BLACK, WHITE, PADDLE_WIDTH
from assets.textures import create_net_texture

def render_ascii_art(font, screen):
    ascii_kian = """
    K I A N ' S   D E A D L Y   P O N G! ! !
    """
    y_offset = 20
    for line in ascii_kian.splitlines():
        text_surface = font.render(line, True, WHITE)
        screen.blit(text_surface, (20, y_offset))
        y_offset += 36
    return y_offset

def draw(screen, font, paddle, balls, powerups, stored_powerups, score, lives, render_ascii_art):
    screen.fill(BLACK)
    y_offset = render_ascii_art()
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
    draw_stored_powerups(screen, font, y_offset + 60, stored_powerups)
    draw_net(screen)
    pygame.display.flip()

def draw_game_elements(screen, font, y_offset, paddle, balls, powerups, stored_powerups):
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
    draw_stored_powerups(screen, font, y_offset + 60, stored_powerups)
    draw_net(screen)

def draw_stored_powerups(screen, font, y_offset, stored_powerups):
    for i, powerup in enumerate(stored_powerups):
        powerup_text = f"[{powerup}]"
        powerup_surface = font.render(powerup_text, True, WHITE)
        screen.blit(powerup_surface, (20 + i * 200, y_offset))

def draw_net(screen):
    mouse_pos = pygame.mouse.get_pos()
    net_texture = create_net_texture(40)
    screen.blit(net_texture, (mouse_pos[0] - NET_SIZE // 2, mouse_pos[1] - NET_SIZE // 2))
