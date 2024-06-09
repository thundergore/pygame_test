import pygame
from settings import WHITE, BLACK, YELLOW, CYAN

def create_paddle_texture(width, height):
    paddle_surface = pygame.Surface((width, height))
    paddle_surface.fill(WHITE)
    for i in range(0, height, 20):
        pygame.draw.line(paddle_surface, BLACK, (0, i), (width, i), 4)
    return paddle_surface

def create_ball_texture(radius):
    ball_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(ball_surface, WHITE, (radius, radius), radius)
    pygame.draw.circle(ball_surface, BLACK, (radius, radius), radius, 4)
    return ball_surface

def create_powerup_texture(size):
    powerup_surface = pygame.Surface((size, size))
    powerup_surface.fill(YELLOW)
    pygame.draw.rect(powerup_surface, BLACK, powerup_surface.get_rect(), 4)
    return powerup_surface

def create_net_texture(size):
    net_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(net_surface, CYAN, (size // 2, size // 2), size // 2, 4)
    return net_surface
