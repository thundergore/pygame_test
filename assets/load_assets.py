# assets/load_assets.py

import pygame

# Constants
PADDLE_WIDTH = 30
PADDLE_HEIGHT = 180
BALL_RADIUS = 14
POWERUP_SIZE = 30
NET_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def create_paddle_texture(width=PADDLE_WIDTH, height=PADDLE_HEIGHT):
    paddle_surface = pygame.Surface((width, height))
    paddle_surface.fill(WHITE)
    for i in range(0, height, 20):
        pygame.draw.line(paddle_surface, BLACK, (0, i), (width, i), 4)
    return paddle_surface

def create_ball_texture(radius=BALL_RADIUS):
    ball_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(ball_surface, WHITE, (radius, radius), radius)
    pygame.draw.circle(ball_surface, BLACK, (radius, radius), radius, 4)
    return ball_surface

def create_powerup_texture(size=POWERUP_SIZE):
    powerup_surface = pygame.Surface((size, size))
    powerup_surface.fill((255, 255, 0))  # Yellow color
    pygame.draw.rect(powerup_surface, (0, 0, 0), powerup_surface.get_rect(), 4)
    return powerup_surface

def create_net_texture(size=NET_SIZE):
    net_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(net_surface, (0, 255, 255), (size // 2, size // 2), size // 2, 4)
    return net_surface

def load_assets():
    paddle_texture = create_paddle_texture()
    ball_texture = create_ball_texture()
    powerup_texture = create_powerup_texture()
    net_texture = create_net_texture()
    return paddle_texture, ball_texture, powerup_texture, net_texture
