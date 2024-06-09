# game/controls.py

import pygame

def move_paddle_scroll(paddle, scroll_amount, paddle_speed, screen_height):
    paddle.y += scroll_amount * paddle_speed
    paddle.clamp_ip(pygame.Rect(0, 0, paddle.width, screen_height))

def move_paddle_mouse(paddle, screen_height):
    mouse_y = pygame.mouse.get_pos()[1]
    paddle.y = mouse_y - paddle.height // 2
    paddle.clamp_ip(pygame.Rect(0, 0, paddle.width, screen_height))
